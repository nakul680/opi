import shutil
import typing
from abc import ABC, abstractmethod
from functools import cached_property, wraps
from pathlib import Path

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from opi.core import Calculator
from opi.input import Input
from opi.input.blocks import Block
from opi.input.simple_keywords import (
    BasisSet,
    Method,
    SimpleKeyword,
    SimpleKeywordBox,
    SolvationModel,
    Solvent,
)
from opi.input.structures import BaseStructureFile, Structure
from opi.output.core import Output


class Settings(BaseModel):
    """
    TODO:
    - add checking for Solvent and SolvationModel now that they are optional.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)
    _name: str

    def __str__(self) -> str:
        """
        String representation of `Settings`. Mostly for debugging purposes.

        Returns
        -------
        str
            String representation of `Settings`.

        """
        lines = [f"{self._name.title()} Settings:"]
        for field_name, value in self.model_dump().items():
            lines.append(f"  {field_name}: {value}")
        return "\n".join(lines)

    @staticmethod
    def _get_field_metadata(hint: typing.Any) -> tuple:
        """
        Function to return the metadata of the type annotation of a field.
        The type hints are first retrieved after which the metadata is extracted and then returned.

        Parameters
        ----------
        hint: Type hint / annotation of field

        Returns
        -------
        tuple
            Tuple of metadata about the field.

        """
        origin = typing.get_origin(hint)
        args = typing.get_args(hint)
        if origin is typing.Union:
            non_none_args = [arg for arg in args if arg is not type(None)]
            if non_none_args:
                return Settings._get_field_metadata(non_none_args[0])
        return args[1:] if len(args) > 1 else ()

    @staticmethod
    def _resolve_field_value(
        value: typing.Any, metadata: tuple[type["SimpleKeywordBox"]] | tuple[str, str]
    ) -> typing.Any:
        """
        Function to translate user input into OPI compatible types. This is done using the metadata of the type
        annotation associated with the field. There are two cases:

        Case 1
        ------
        Metadata has only one value. In this case the field is a simple keyword. Here the class associated with the input
        option (eg: `Dft`) ,  will be checked to see if the user-given input option exists , and if it does , returns
        the enum member associated with the input option.

        Case 2
        ------
        Metadata has two values, validator class and key. In this case the field is a block option. The associated block
        class is first fetched, and then the attribute of the block is set to the user-given input option. This is then
        validated by the block itself using Pydantic features. The validation function of the block translates user input
        to OPI compatible types, which is then returned.


        Parameters
        ----------
        value: typing.Any
            User input value.
        metadata: tuple
            Tuple of metadata about the field.

        Returns
        -------
        typing.Any
            User input value translated to OPI compatible types.

        """
        match metadata:
            case (validator,):
                return validator.find_keyword(value)

            case (validator, key):
                block_cls = Block.get_subclass_by_name(validator)
                instance = block_cls.model_validate({key: value})
                return getattr(instance, key)

            case _:
                return value

    def _get_simple_keyword(self, validator: type[SimpleKeywordBox], value) -> SimpleKeyword:
        if validator == SolvationModel:
            solvent = getattr(self, "solvent", None)
            new_keyword = value(solvent)
        else:
            new_keyword = value

        return new_keyword

    def map_to_input(self, input_object: Input) -> Input:
        """
        Function to map all information held in `Settings` class to an `Input` class object. The function receives an
        `Input` object , which may or may not be already populated, after which the function uses the type hints of
        every field defined in the class to either fetch a `SimpleKeyword` from the appropriate Enum, and adds it to
        `Input.simple_keywords`, or initializes the appropriate block with the attribute set to user defined value, and
        adds it to `Input.blocks`.

        The modified `Input` object is then returned.

        Parameters
        ----------
        input_object: Input
            `Input` object to be modified

        Returns
        -------
        Input
            Modified `Input` object.
        """
        hints = typing.get_type_hints(self.__class__, include_extras=True)

        for field_name, field_type in hints.items():
            value = getattr(self, field_name)
            if value is None:
                continue

            metadata = self._get_field_metadata(field_type)

            match metadata:
                case (validator,):
                    if validator == Solvent:
                        continue

                    new_keyword = self._get_simple_keyword(validator, value)
                    if new_keyword:
                        input_object.add_simple_keywords(new_keyword)

                case (validator, key):
                    block_type = Block.get_subclass_by_name(validator)
                    block_class = block_type(**{key: value})

                    block_exists, *_ = input_object.has_blocks(block_type)
                    if not block_exists:
                        input_object.add_blocks(block_class)
                    else:
                        existing_block = next(iter(input_object.get_blocks(block_type).values()))
                        new_block = existing_block + block_class
                        input_object.add_blocks(new_block, overwrite=True)

        return input_object

    @field_validator("*", mode="before")
    @classmethod
    def validate_fields(cls, value: typing.Any, info):
        """
        This field validator handles validation upon reassignment of values of class attributes.

        This validator is applied to all fields and is executed prior to Pydantics internal validation, which is useful
        for handling reassignment of values or custom preprocessing logic.

        The method does the following:
        1. Retrieves type hints, including metadata and checks whether current field has corresponding type hint.
        2. Extracts field specific metadata from type hint.
        3. Resolves incoming value using metadata.

        Parameters
        ----------
        value: Any
            User input value.
        info
            Object containing contextual information about field being validated.

        Returns
        -------
        Any
            User input value processed and converted to OPI compatible types.
        """
        if value is None:
            return value

        hints = typing.get_type_hints(cls, include_extras=True)

        if info.field_name not in hints:
            return value

        hint = hints[info.field_name]
        metadata = cls._get_field_metadata(hint)
        return cls._resolve_field_value(value, metadata)

    @model_validator(mode="before")
    @classmethod
    def cross_validate(cls, data: dict[str, typing.Any]) -> dict[str, typing.Any]:
        """
        Function to process and validate user input, this validator handles validation upon model initialization. Since
        `self.validate_field()` already exists, this function will be reserved only for cross validation.

        Parameters
        ----------
        data: dict
            User input data.

        Returns
        -------
        dict
            Cross-validated user input data

        """
        if not isinstance(data, dict):
            return data

        return data


class TaskSettings(Settings):
    task_keyword: typing.Annotated[SimpleKeyword, SimpleKeywordBox]


class MethodSettings(Settings):
    method: typing.Annotated[SimpleKeyword, Method]
    basis_set: typing.Annotated[SimpleKeyword, BasisSet] | None = None
    solvation_model: typing.Annotated[SimpleKeyword, SolvationModel] | None = None
    solvent: typing.Annotated[str, Solvent] | None = None


class SimpleTask(ABC):
    _results_type: type["TaskResults"]
    _task_settings: TaskSettings
    _method_settings: MethodSettings

    @property
    def task_settings(self) -> TaskSettings:
        return self._task_settings

    @property
    def method_settings(self) -> MethodSettings:
        return self._method_settings

    @property
    def input_object(self) -> Input:
        """
        Creates configured `Input` object. First it initializes an empty instance of `Input` , and then passes it as
        to corresponding `TaskSettings` and `MethodSettings` objects to be configured by user-defined data stored in those
        objects.

        Returns
        -------
        `Input`
            `Input` object configured by user-defined data.

        """
        inp = Input()
        inp = self._task_settings.map_to_input(input_object=inp)
        inp = self.method_settings.map_to_input(input_object=inp)
        return inp

    def __getattr__(self, name: str) -> typing.Any:
        """
        Dynamically resolve attribute access by delegating to internal settings objects.

        This method is called when an attribute is not found on the instance through
        the normal lookup process. It attempts to retrieve the attribute from the
        internal `_task_settings` and `_method_settings` objects, in that order.

        Parameters
        ----------
        name: str
            Attribute name.

        Returns
        --------
        Any
            Attribute value.
        """
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        try:
            return getattr(self._task_settings, name)
        except AttributeError:
            pass

        try:
            return getattr(self._method_settings, name)
        except AttributeError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: typing.Any) -> None:
        """
        Dynamically assign attributes, delegating to internal settings objects when appropriate.

        This method overrides the default attribute assignment behavior to route
        assignments to `_task_settings` or `_method_settings` if the attribute
        exists. Otherwise, the attribute is set directly on the instance.

        Parameters
        ----------
        name : str
            The name of the attribute to assign.
        value : Any
            The value to assign to the attribute.
        """
        # Allow setting private attributes and special attributes normally
        if name.startswith("_") or name in ("task_settings", "run"):
            super().__setattr__(name, value)
        else:
            # Check if _task_settings exists and has this attribute
            if hasattr(self, "_task_settings") and hasattr(self._task_settings, name):
                setattr(self._task_settings, name, value)
            elif hasattr(self, "_method_settings") and hasattr(self._method_settings, name):
                setattr(self._method_settings, name, value)
            else:
                super().__setattr__(name, value)

    def run(
        self,
        basename: str,
        struct: Structure | BaseStructureFile,
        working_dir: Path = Path("RUN"),
        ncores: int | None = None,
        memory: int | None = None,
        moinp: Path | None = None,
        strict: bool = False
    ) -> "TaskResults":
        """
        Execute the computational task with the given structure and settings.

        This method prepares the working directory, configures the calculation
        input parameters, and runs the calculation using an external calculator.
        The results are returned as an instance of the configured results type.

        Parameters
        ----------
        basename : str
            Base name for the calculation.
        struct : Structure or BaseStructureFile
            The input structure for the calculation.
        working_dir : pathlib.Path, optional
            Directory in which the calculation will be executed.
            If it exists, it will be removed and recreated. Defaults to "RUN".
        ncores : int, optional
            Number of CPU cores to use for the calculation. Overrides the default
            value in the input object if provided.
        memory : int, optional
            Amount of memory to allocate for the calculation. Overrides the default
            value in the input object if provided.
        moinp : pathlib.Path, optional
            Path to a molecular orbital input file. Overrides the default if provided.
        strict : bool, optional
            Controls whether working directory will be created/overwritten. Defaults to False.

        Returns
        -------
        TaskResults
            An instance of the configured results type containing the results
            of the calculation.
        """
        if strict:
            # Must already exist
            if not working_dir.exists():
                raise ValueError(f"Working directory {working_dir.resolve()} does not exist (strict mode)")

            # Must be empty
            if any(working_dir.iterdir()):
                raise ValueError(f"Working directory {working_dir.resolve()} is not empty (strict mode)")

        else:
            # Non-strict: recreate directory
            if working_dir.exists():
                shutil.rmtree(working_dir)
            working_dir.mkdir()

        inp = self.input_object

        if ncores is not None:
            inp.ncores = ncores

        if memory is not None:
            inp.memory = memory

        if moinp is not None:
            inp.moinp = moinp

        calc = Calculator(basename, working_dir=working_dir)
        calc.structure = struct
        calc.input = inp

        calc.write_and_run()

        return self._results_type(calc_object=calc)

    def _restart(
        self,
        previous_results: "TaskResults",
        basename: str | None = None,
        struct: Structure | BaseStructureFile | None = None,
        working_dir: Path | None = None,
        ncores: int | None = None,
        memory: int | None = None,
        moinp: Path | None = None,
        use_previous_orbitals: bool = False,
    ) -> "TaskResults":
        """
        TODO:
        - finish restart implementation (low on priority list)
        Parameters
        ----------
        previous_results
        basename
        struct
        working_dir
        ncores
        memory
        moinp
        use_previous_orbitals

        Returns
        -------

        """
        prev_calc = previous_results.calc_object

        basename = basename if basename else prev_calc.basename
        struct = struct if struct else prev_calc.structure
        working_dir = working_dir if working_dir else prev_calc.working_dir
        ncores = ncores if ncores else prev_calc.input.ncores
        memory = memory if memory else prev_calc.input.memory

        if use_previous_orbitals:
            prev_gbw = prev_calc.working_dir / f"{prev_calc.basename}.gbw"
            if not prev_gbw.exists():
                raise FileNotFoundError(f"GBW file not found: {prev_gbw}")
            moinp = prev_gbw
        else:
            moinp = moinp if moinp else prev_calc.input.moinp

        return self.run(basename, struct, working_dir, ncores, memory, moinp)


class TaskResults(ABC):
    def __init__(self, calc_object: Calculator):
        self.calc_object = calc_object
        self._parsed = False

    @staticmethod
    def output_parse(
        func: typing.Callable[["TaskResults"], typing.Any],
    ) -> typing.Callable[["TaskResults"], typing.Any]:
        """
        Decorator to ensure output parsing is performed before accessing results.

        This decorator wraps methods of a `TaskResults` instance and guarantees
        that the associated output has been parsed before the method is executed.
        Parsing is performed lazily and only once per instance.

        Parameters
        ----------
        func : Callable[[TaskResults], Any]
            The method to wrap. It must be a method of `TaskResults` that relies
            on parsed output data.

        Returns
        -------
        Callable[[TaskResults], Any]
            A wrapped method that ensures `self.output.parse()` has been called
            before delegating to the original function.
        """

        @wraps(func)
        def wrapper(self: "TaskResults"):
            if not self._parsed:
                self.output.parse()
                self._parsed = True
            return func(self)

        return wrapper

    @cached_property
    def output(self) -> Output:
        if not self.calc_object:
            raise ValueError("calc_object not set")

        return self.calc_object.get_output()

    @cached_property
    def status(self) -> bool:
        return self.output.terminated_normally() and self.output.scf_converged()

    @cached_property
    @abstractmethod
    def primary_property(self) -> typing.Any:
        pass

    def __getattr__(self, name):
        """
        First tries to get attribute from the object itself.
        If not found, tries to get it from self.output.
        """
        # Check if 'output' exists to avoid infinite recursion
        if name == 'output':
            raise AttributeError(f"'{type(self).__name__}' object has no attribute 'output'")

        # Try to get the attribute from self.output
        try:
            return getattr(self.output, name)
        except AttributeError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

