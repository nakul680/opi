import typing
from pathlib import Path

from opi.input.simple_keywords import BasisSet, Method, SimpleKeyword, SolvationModel, Solvent
from opi.input.structures import Structure
from opi.tasks.task_base import Task, TaskParams, TaskResults


class SinglePointParams(TaskParams):
    method: typing.Annotated[SimpleKeyword, Method]
    basis_set: typing.Annotated[SimpleKeyword, BasisSet]
    solvation_model: typing.Annotated[SimpleKeyword, SolvationModel]
    solvent: typing.Annotated[str, Solvent]


class SinglePointTask(Task):
    def __init__(
        self,
        method: str | SimpleKeyword,
        basis_set: str | SimpleKeyword,
        solvation_model: str | SolvationModel,
        solvent: str | Solvent,
    ):
        self._task_parameters = SinglePointParams(
            method=method, basis_set=basis_set, solvation_model=solvation_model, solvent=solvent
        )
        self._results_type = SinglePointResults

    @property
    def task_parameters(self) -> SinglePointParams:
        return self._task_parameters

    def __getattr__(self, name):
        """Delegate attribute access to _task_parameters."""
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        try:
            return getattr(self._task_parameters, name)
        except AttributeError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Delegate attribute setting to _task_parameters."""
        # Allow setting private attributes and special attributes normally
        if name.startswith('_') or name in ('task_parameters', 'run'):
            super().__setattr__(name, value)
        else:
            # Check if _task_parameters exists and has this attribute
            if hasattr(self, '_task_parameters') and hasattr(self._task_parameters, name):
                setattr(self._task_parameters, name, value)
            else:
                super().__setattr__(name, value)

    def run(
        self,
        basename: str,
        struct: Structure,
        working_dir: Path = Path("RUN"),
        ncores: int | None = None,
        memory: int | None = None,
        moinp: Path | None = None,
    ) -> "SinglePointResults":
        single_point_result = super().run(
            basename=basename,
            struct=struct,
            working_dir=working_dir,
            ncores=ncores,
            memory=memory,
            moinp=moinp,
        )

        return single_point_result


class SinglePointResults(TaskResults):
    @property
    def status(self) -> bool:
        return self.output.terminated_normally() and self.output.scf_converged()

    @property
    @TaskResults.output_parse
    def final_energy(self) -> float:
        final_energy = self.output.get_final_energy()

        if final_energy is None:
            raise ValueError("Could not get final energy from ORCA Output")

        return final_energy

    @property
    def primary_property(self) -> float:
        return float(self.final_energy)
