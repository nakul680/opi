import typing

from opi.input import Input
from opi.input.simple_keywords import Task, SimpleKeyword, Solvent
from opi.input.simple_keywords.opt import OptThreshold, Opt
from opi.input.structures import Structure
from opi.tasks.method_settings import DFTSettings
from opi.tasks.task_base import TaskSettings, TaskResults, SimpleTask


class OptSettings(TaskSettings):
    _name:str = "opt"
    task_keyword: typing.Annotated[SimpleKeyword, Task] = Task.OPT
    opt_threshold: typing.Annotated[SimpleKeyword, OptThreshold] | None = None
    optrigid: bool = False
    opt_h: bool = False
    lopt:bool = False
    opt_maxiter: typing.Annotated[int, "BlockGeom", "maxiter"] | None = None

    def map_to_input(self, input_object: Input) -> Input:
        input_object = super().map_to_input(input_object)

        if self.optrigid:
            input_object.add_simple_keywords(Opt.RIGIDBODYOPT)

        opt_map = {
            (True, True): Opt.L_OPTH,
            (True, False): Opt.OPTH,
            (False, True): Opt.L_OPT,
        }

        keyword = opt_map.get((self.opt_h, self.lopt))
        if keyword:
            input_object.add_simple_keywords(keyword)

        return input_object


class OptTask(SimpleTask):
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
            OptSettings(task_keyword=task)
        ) if task else OptSettings()

        self._results_type = OptResults


class OptResults(TaskResults):
    @property
    @TaskResults.output_parse
    def final_energy(self) -> float:
        final_energy = self.output.get_final_energy()

        if final_energy is None:
            raise ValueError("Could not get final energy from ORCA Output")

        return final_energy


    @property
    @TaskResults.output_parse
    def structure(self) -> Structure:
        structure = self.output.get_structure()
        if structure is None:
            raise ValueError("Could not get structure from ORCA Output")

        return structure


    @property
    def primary_property(self) -> tuple[float, Structure]:
        return self.final_energy, self.structure




