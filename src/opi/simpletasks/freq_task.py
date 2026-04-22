import typing
from functools import cached_property

from opi.input.simple_keywords import Task, SimpleKeyword, Solvent
from opi.simpletasks.base_task import TaskSettings, TaskResults, SimpleTask
from opi.simpletasks.method_settings import MethodSettings


class FreqSettings(TaskSettings):
    _name: str = "freq"
    task_keyword: typing.Annotated[SimpleKeyword, Task] =  Task.FREQ


class FreqTask(SimpleTask):
    _task_settings: FreqSettings

    def __init__(self, method: str | SimpleKeyword, basis_set: str | SimpleKeyword | None = None,
                 solvation_model: str | SimpleKeyword | None = None, solvent: str | Solvent | None = None,
                 task_settings: FreqSettings | None = None, method_settings: MethodSettings | None = None):
        self._task_settings_type = FreqSettings
        super().__init__(method, basis_set, solvation_model, solvent, task_settings, method_settings)

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
        return float(self.free_energy_delta)

