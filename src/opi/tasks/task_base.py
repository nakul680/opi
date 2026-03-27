import shutil
import typing
from abc import ABC, abstractmethod
from functools import cached_property, wraps
from pathlib import Path

from pydantic import BaseModel, ConfigDict, model_validator, field_validator

from opi.core import Calculator
from opi.input import Input
from opi.input.blocks import Block
from opi.input.simple_keywords import SolvationModel, Solvent
from opi.input.structures import Structure
from opi.output.core import Output


class TaskParams(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    def map_to_input(self, input_object: Input) -> Input:
        hints = typing.get_type_hints(self.__class__, include_extras=True)

        for field_name, field_type in hints.items():
            value = getattr(self, field_name)

            args = typing.get_args(field_type)
            metadata = args[1:]

            match metadata:
                case (validator,):
                    if validator == SolvationModel:
                        solvent = getattr(self, "solvent", None)
                        if not solvent:
                            raise ValueError("Solvent not set")
                        new_keyword = value(solvent)
                        input_object.add_simple_keywords(new_keyword)
                    elif validator == Solvent:
                        continue
                    else:
                        input_object.add_simple_keywords(value)
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


    @field_validator('*', mode='before')
    @classmethod
    def validate_each_field(cls, value, info):
        field_name = info.field_name
        hints = typing.get_type_hints(cls, include_extras=True)

        if field_name not in hints:
            return value

        hint = hints[field_name]
        args = typing.get_args(hint)
        metadata = args[1:] if len(args) > 1 else ()

        match metadata:
            case (validator, ):
                return validator.find_keyword(value)

            case (validator, key):
                block_cls = Block.get_subclass_by_name(validator)
                instance = block_cls.model_validate({key: value})
                return getattr(instance, key)

        return value

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: dict) -> dict:
        hints = typing.get_type_hints(cls, include_extras=True)

        for field_name, hint in hints.items():
            value = data.get(field_name)
            if field_name not in data:
                continue

            args = typing.get_args(hint)
            metadata = args[1:]

            match metadata:
                case (validator,):
                    keyword = validator.find_keyword(data[field_name])
                    data[field_name] = keyword

                case (validator, key):
                    block_cls = Block.get_subclass_by_name(validator)
                    instance = block_cls.model_validate({key: value})
                    data[field_name] = getattr(instance, key)

        return data


class Task(ABC):
    _results_type: type["TaskResults"]

    @property
    @abstractmethod
    def task_parameters(self) -> TaskParams :
        pass

    @property
    def input_object(self) -> Input:
        inp = Input()
        inp = self.task_parameters.map_to_input(input_object=inp)
        return inp

    def run(
        self,
        basename: str,
        struct: Structure,
        working_dir: Path = Path("RUN"),
        ncores: int | None = None,
        memory: int | None = None,
        moinp: Path | None = None,
    ) -> "TaskResults":

        # > recreate the working dir
        shutil.rmtree(working_dir, ignore_errors=True)
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


    def change_parameter(self, param: str, value: typing.Any) -> None:
        setattr(self.task_parameters, param, value)


class TaskResults(ABC):
    def __init__(self, calc_object: Calculator):
        self.calc_object = calc_object
        self._parsed = False

    @staticmethod
    def output_parse(
        func: typing.Callable[["TaskResults"], typing.Any],
    ) -> typing.Callable[["TaskResults"], typing.Any]:
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
