import typing
from pathlib import Path

from opi.input.simple_keywords import SimpleKeyword, SolvationModel, Solvent, Task
from opi.input.structures import BaseStructureFile, Structure
from opi.tasks.method_settings import DFTSettings
from opi.tasks.task_base import SimpleTask, TaskResults, TaskSettings


class SinglePointSettings(TaskSettings):
    _name: str = "singlepoint"
    task_keyword: typing.Annotated[SimpleKeyword, Task] = Task.SP


class SinglePointTask(SimpleTask):
    def __init__(
        self,
        method: str | SimpleKeyword,
        basis_set: str | SimpleKeyword,
        solvation_model: str | SolvationModel,
        solvent: str | Solvent,
        task: str | SimpleKeyword | None = None,
    ):
        self._method_settings = DFTSettings(
            method=method, basis_set=basis_set, solvation_model=solvation_model, solvent=solvent
        )
        self._task_settings = (
            SinglePointSettings(task_keyword=task) if task else SinglePointSettings()
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

        return typing.cast(SinglePointResults, single_point_result)


class SinglePointResults(TaskResults):
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
