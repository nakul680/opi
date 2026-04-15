import typing
from functools import cached_property

from opi.input.simple_keywords import Task, SimpleKeyword, Solvent
from opi.tasks.method_settings import DFTSettings
from opi.tasks.task_base import TaskSettings, TaskResults, SimpleTask


class FreqSettings(TaskSettings):
    _name: str = "freq"
    task_keyword: typing.Annotated[SimpleKeyword, Task] =  Task.FREQ


class FreqTask(SimpleTask):
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
            FreqSettings(task_keyword=task)
        ) if task else FreqSettings()

        self._results_type = FreqResults


class FreqResults(TaskResults):
    @cached_property
    def status(self) -> bool:
        return self.output.terminated_normally()

    @cached_property
    @TaskResults.output_parse
    def free_energy_delta(self) -> float:
        free_energy_delta = self.output.get_free_energy_delta()

        if not free_energy_delta:
            raise ValueError("Could not get free energy delta from ORCA output")

        return free_energy_delta

    @property
    def primary_property(self) -> float:
        return self.free_energy_delta

