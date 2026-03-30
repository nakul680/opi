import typing
from pathlib import Path

from opi.input.simple_keywords import BasisSet, Method, SimpleKeyword, SolvationModel, Solvent
from opi.input.structures import Structure, BaseStructureFile
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


    def run(
        self,
        basename: str,
        struct: Structure | BaseStructureFile,
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

        return typing.cast(SinglePointResults ,single_point_result)


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
