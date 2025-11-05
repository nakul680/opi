from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block
from opi.input.blocks.util import NumList

__all__ = ("BlockCasscf",)


class BlockCasscf(Block):
    """Class to model %casscf block in ORCA"""

    _name: str = "casscf"
    nel: int | None = None  # number of active space electrons
    norb: int | None = None # number of active orbitals
    mult: int | NumList | None = None # multiplicities
    irrep: int | NumList | None = None # irrep for each mult block
    nroots: int | NumList | None = None #
    bweight: float | NumList | None = None  # define weights for multiplicity blocks
    weights: float | None = None  # define custo weighting scheme for multiplicity blocks and roots
    hessroot: int | None = None   #
    iroot: int | None = None      # root for given imult
    jroot: int | None = None
    imult: int | None = None      # multiplicity block
    followiroot: bool | None = None
    followirootno: bool | None = None
    followirootmix: bool | None = None
    followiroottdens: bool | None = None
    orbstep: (
        Literal[
            "diis",
            "kdiis",
            "soscf",
            "superci",
            "superci_pt",
            "superci_ptno",
            "nr",
            "trah",
        ]
        | None
    ) = None   # orbital optimization method
    cistep: (
        Literal[
            "csfci",
            "accci",
            "cipsi",
            "ice",
            "dmrgci",
            "qmcci",
            "molmpsci",
            "mccas",
            "detci",
            "treecsf",
        ]
        | None
    ) = None  #
    trafostep: Literal["exact", "rimo", "ri"] | None = None
    switchconv: float | None = None  # define gradient at which to switch
    switchiter: int | None = None    # iteration at which the switch takes place
    switchstep: int | None = None
    parametrization: Literal["cayley", "expk"] | None = None
    etol: float | None = None  # convergence criteria for energy
    gtol: float | None = None  # convergence criteria for g
    printlevel: int | None = None  # amount of output during AH iteration
    printgstate: int | None = None # optional printing of state-specific orbital gradients
    printndo: int | None = None
    printwf: int | None = None     # print settings for wave functions
    actorbs: int | None = None
    actconstraints: Literal["unchanged", "canonorbs", "locorbs", "natorbs"] | None = None #
    locmet: Literal["pipekmezey", "pm", "fosterboys", "fb", "iaoibo", "iaoboys", "ahfb"] | None = (
        None
    )  # choose localization method
    nevpt2: int | None = None
    ptmethod: (
        Literal[
            "sc",
            "fic",
            "pc",
            "dlpno",
            "dlpno_nevpt2",
            "fic_nevpt2",
            "sc_nevpt2",
            "fic_caspt2",
            "fic_caspt2k",
            "fic_caspt2s",
        ]
        | None
    ) = None
    freezeactive: float | None = None  # damping options
    dthresh: float | None = None  # thresh for critical occupation
    buildhessian: int | None = None
    resethessian: int | None = None
    maxdampiter: int | None = None
    gradscaling: float | None = None # damping option
    convrate: float | None = None
    freezeie: float | None = None  # damping option
    freezegrad: float | None = None # damping option
    superdiis: bool | None = None
    maxiter: int | None = None  # maximum number of macro-iterations
    maxmicroiter: int | None = None # maximum number of micro-iterations
    maxdiis: int | None = None  # max no. of DIIS vectors to keep
    diisthresh: float | None = None # overlap criteria for linear dependancy
    resetfreq: int | None = None  # reset frequency for direct SCF
    switchdens: float | None = None # approximate active Fock when density is considered unchanged
    doipea: bool | None = None
    donto: bool | None = None
    ntothresh: float | None = None  # threshold for printing occupation numbers
    nntostates: int | None = None
    ntostates: int | None = None    # states to consider for NTO analysis
    dondo: bool | None = None       # generate NAtural Difference Density Orbitals
    nndostates: int | None = None
    ndostates: int | None = None    # states to consider for NDO analysis
    dotransdens: bool | None = None
    inistateenerrange: float | None = None
    docd: bool | None = None  #
    dodipolelength: bool | None = None
    dodipolevelocity: bool | None = None
    dohighermoments: bool | None = None
    dofullsemiclassical: bool | None = None
    decomposefosclength: bool | None = None
    decomposefoscvelocity: bool | None = None
    dotransient: int | None = None
    cas_ewin: NumList | None = None

    @field_validator("mult", "irrep", "nroots", "bweight", mode="before")
    @classmethod
    def numlist_fromlist(cls, inp: int | list[int] | NumList) -> int | NumList:
        """
        Parameters
        ----------
        inp : int | list[int] | NumList
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp

    @field_validator("cas_ewin", mode="before")
    @classmethod
    def qcas_ewin_init(cls, inp: list[float] | NumList) -> NumList:
        """
        Parameters
        ----------
        inp : list[float] | NumList
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp
