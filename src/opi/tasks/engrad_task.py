import typing

from opi.input.simple_keywords import Task, SimpleKeyword, Solvent
from opi.tasks.method_settings import DFTSettings
from opi.tasks.task_base import SimpleTask, TaskSettings, TaskResults


class EngradSettings(TaskSettings):
    _name: str = "engrad"
    task_keyword: typing.Annotated[SimpleKeyword, Task] = Task.ENGRAD


class EngradTask(SimpleTask):
    def __init__(self,
                 method: str | SimpleKeyword,
                 basis_set: str | SimpleKeyword | None = None,
                 solvation_model: str | SimpleKeyword | None = None,
                 solvent: str | Solvent | None = None,
                 task: str | SimpleKeyword | None = None):
        self._method_settings = DFTSettings(
            method=method, basis_set=basis_set, solvation_model=solvation_model, solvent=solvent
        )
        self._task_settings = (
            EngradSettings(task_keyword=task)
        ) if task else EngradSettings()

        self._results_type = EngradResults


class EngradResults(TaskResults):
    @property
    @TaskResults.output_parse
    def final_energy(self) -> float:
        final_energy = self.output.get_final_energy()

        if final_energy is None:
            raise ValueError("Could not get final energy from ORCA Output")

        return final_energy

    @property
    @TaskResults.output_parse
    def gradient(self) -> list[float]:
        gradient = self.output.get_gradient()

        if gradient is None:
            raise ValueError("Could not get gradient from ORCA Output")

        return gradient

    @property
    def primary_property(self) -> tuple[float, list[float]]:
        return self.final_energy, self.gradient