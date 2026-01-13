import inspect
import shutil
import tempfile
from pathlib import Path
from typing import Set, get_args, get_origin

import pytest
from pydantic import BaseModel

from opi.output.core import Output
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.output.models.json.property.property_results import PropertyResults

GBWRESULTS_ATTR = {
    "pairstotalssciso",
    "qel",
    "electrostref",
    "corrdt",
    "densa",
    "calculation_timings",
    "e0",
    "nsomo",
    "natural_orbitals",
    "adexatomic_mulliken",
    "correnergy",
    "single_point_data",
    "diskflag",
    "rsolv",
    "casscfenergies",
    "enthalpyh",
    "numofnucs",
    "spin_spin_coupling",
    "mbis_population_analysis",
    "aeigenvalues",
    "denstype",
    "corrss",
    "numofauxjbasisfuncts",
    "pressure",
    "block",
    "converged",
    "finalenergy",
    "irrep",
    "s2brokensym",
    "method",
    "doep1",
    "npopval",
    "doatomicpolar",
    "adlddispfrag_loewdin",
    "dispweak",
    "adldcorratomic_loewdin",
    "numofauxcbasisfuncts",
    "version",
    "coordinates",
    "thresh",
    "sigmaval",
    "corrst",
    "efg_tensor",
    "totalenergy",
    "dft_energy",
    "g_rmc",
    "numofenergies",
    "state",
    "chemical_shift",
    "refenergy",
    "thermochemistry_energies",
    "numofnucpairssd",
    "absorption_spectrum",
    "s2highspin",
    "shighspin",
    "nbondordersprint",
    "innerenergyu",
    "dispcontr",
    "nbetael",
    "hessian",
    "g_dso",
    "numofauxjkbasisfuncts",
    "enhighspin",
    "za",
    "largeprint",
    "bbcorren",
    "numofalphacorrel",
    "niter",
    "finalen",
    "surfacearea",
    "bva",
    "spin",
    "mulliken_population_analysis",
    "adexfrag_loewdin",
    "numofbasisfuncts",
    "ecorr",
    "doatomicquad",
    "refint",
    "rotenergy",
    "numofnucpairs",
    "ndomo",
    "sum",
    "va",
    "adlddispatomic_loewdin",
    "multiplicity",
    "numofnucpairsfc",
    "g_elec",
    "quadrupole_moment",
    "pairsinfo",
    "totint",
    "adlddispatomic_mulliken",
    "densb",
    "epsilon",
    "fragments",
    "scf",
    "qrot",
    "ccsdtenergyx",
    "quaddiagonalized",
    "multp1",
    "cpcmdielenergy",
    "sumnondisstrong",
    "corrcbs",
    "adldcorrfrag_loewdin",
    "doep2",
    "states",
    "root",
    "dipoleeleccontrib",
    "g_tot",
    "mult",
    "qfac",
    "adexfrag_mulliken",
    "orientation",
    "zpe",
    "dogradients",
    "isotropicpolar",
    "dipole_moment",
    "bondthresh",
    "exc",
    "vdw",
    "freq",
    "broken_symmetry",
    "nroots",
    "hirshfeld_population_analysis",
    "qvib",
    "calculation_status",
    "natoms",
    "numoffreqs",
    "temperature",
    "bondorders",
    "multiplicities",
    "g_tensor",
    "energy_extrapolation",
    "adldcorrfrag_mulliken",
    "vibenergy",
    "triplesenergy",
    "freqscalingfactor",
    "ntotalroots",
    "i",
    "numofbetacorrel",
    "eexchange",
    "numofcorrel",
    "solvent",
    "gtoint",
    "nghostatoms",
    "nnatoorbs",
    "numofroots",
    "dohighermoments",
    "isotropicquadmoment",
    "corrint",
    "stoteigen",
    "nvmo",
    "numofmultiplicities",
    "enbrokensym",
    "numofnucpairsdso",
    "quadeleccontrib",
    "pointgroup",
    "adldcorratomic_mulliken",
    "corrds",
    "vdw_correction",
    "charge",
    "freeenergyg",
    "elem",
    "chelpg_population_analysis",
    "cipsi_energies",
    "geometry",
    "modes",
    "quadnuccontrib",
    "grad",
    "numofactiveorbs",
    "ncorelessecp",
    "doatomicdipole",
    "pfac",
    "denslevel",
    "islinear",
    "status",
    "numofelectrons",
    "calculation_info",
    "dipolemagnitude",
    "rawcartesian",
    "a_tensor",
    "scfgrad",
    "atomiccharges",
    "g_matrix",
    "numofnucpairspso",
    "numofactiveel",
    "elems",
    "elenergy",
    "abcorren",
    "numoffragments",
    "nuc",
    "density_name",
    "cartesians",
    "level",
    "diagonalizedtensor",
    "delta_g_iso",
    "spindegeneracy",
    "numofatoms",
    "isotope",
    "delta_g",
    "excitationenergies",
    "mdci_led",
    "ntotalel",
    "polarizability",
    "loewdin_population_analysis",
    "numoffcelectrons",
    "refrac",
    "mdci_adex",
    "units",
    "deritype",
    "type",
    "mode",
    "roci_energy",
    "quadtotal",
    "stot",
    "aacorren",
    "dipoletotal",
    "scfcbs",
    "veigenvalues",
    "occunso",
    "totalmass",
    "transenergy",
    "araw",
    "dcorr",
    "energies",
    "nalphael",
    "v",
    "aiso",
    "qa",
    "totalnumofroots",
    "g_pso",
    "dipolenuccontrib",
    "exchangeref",
    "nblocks",
    "energy",
    "representation",
    "prop",
    "doep3",
    "mdci_adld",
    "nel",
    "pal_flags",
    "numofel",
    "na",
    "gradnorm",
    "components",
    "gstep",
    "scfenergies",
    "relcorrection",
    "eembed",
    "viso",
    "npoints",
    "numofcorrelectrons",
    "relcorr",
    "occuno",
    "g_iso",
    "mayer_population_analysis",
    "ntrans",
    "adlddispfrag_mulliken",
    "numofcabsbasisfuncts",
    "correnergies",
    "nuclear_gradient",
    "progname",
    "totalcbs",
    "entropys",
    "atno",
    "ecnl",
    "pairsdistances",
    "solvation_details",
    "ecd_spectrum",
    "adexatomic_loewdin",
    "sumnondisweak",
    "vdw_atomic",
    "surfacetype",
    "fa",
    "geometries",
}
PROPRESULTS_ATTR = {
    "author",
    "number",
    "td_dft",
    "s_matrix",
    "type",
    "exponents",
    "citations",
    "orbwin",
    "shell",
    "orbitalenergy",
    "basis",
    "mos",
    "mocoefficients",
    "date",
    "version",
    "elementnumber",
    "nuclearcharge",
    "coords",
    "volume",
    "journal",
    "occupancy",
    "coordinateunits",
    "f_matrix",
    "doi",
    "mullikencharge",
    "atoms",
    "h_matrix",
    "basisauxjk",
    "pages",
    "orbitallabels",
    "loewdincharge",
    "rn231",
    "multiplicity",
    "j_matrix",
    "idx",
    "coefficients",
    "k_matrix",
    "pointgroup",
    "charge",
    "orbitalsymlabel",
    "year",
    "basisauxj",
    "elementlabel",
    "title",
    "rn232",
    "git",
    "origin",
    "molecularorbitals",
    "basename",
    "orca_header",
    "basisauxc",
    "xy",
    "hftyp",
    "iroot",
    "molecule",
    "energyunit",
    "orbitalsymmetry",
    "x",
}
JSON_DIR = Path(__file__).parent.parent / "json_files"


def add_gbw_jsons(output_object: Output, gbw_jsons):
    for gbw_json in gbw_jsons:
        output_object.gbw_json_files.append(gbw_json)

    output_object.parse(read_gbw_json=True)


def get_all_attributes(
    model: type[BaseModel], visited: Set[type] = None, prefix: str = ""
) -> Set[str]:
    """
    Recursively get all attribute names from a Pydantic model, including nested custom types.
    Attribute names include their parent class prefix (e.g., "A.attr1.attr2").

    Args:
        model: The Pydantic model class to extract attributes from
        visited: Set of already visited types to avoid infinite recursion
        prefix: Current prefix for nested attributes (e.g., "A.attr1.")

    Returns:
        Set of all attribute names with parent prefixes (e.g., {"attr1", "A.attr1.attr2"})
    """
    if visited is None:
        visited = set()

    # Avoid infinite recursion for self-referential models
    if model in visited:
        return set()
    visited.add(model)

    attributes = set()

    # Iterate through all fields in the model
    for field_name, field_info in model.model_fields.items():
        # Add the field name with current prefix
        full_name = f"{prefix}.{field_name}" if prefix else field_name
        attributes.add(full_name)

        # Get the field type
        field_type = field_info.annotation

        # Create prefix for nested attributes - continue the chain
        nested_prefix = f"{prefix}.{field_name}" if prefix else f"{model.__name__}{field_name}"

        # Handle Optional, List, Dict, etc.
        origin = get_origin(field_type)
        if origin is not None:
            # For generic types, get the actual type arguments
            type_args = get_args(field_type)
            for arg in type_args:
                # Recursively check if the type argument is a Pydantic model
                if inspect.isclass(arg) and issubclass(arg, BaseModel):
                    nested_attrs = get_all_attributes(arg, visited.copy(), nested_prefix)
                    attributes.update(nested_attrs)
                # Handle nested generics (e.g., List[Optional[Model]])
                elif get_origin(arg) is not None:
                    inner_args = get_args(arg)
                    for inner_arg in inner_args:
                        if inspect.isclass(inner_arg) and issubclass(inner_arg, BaseModel):
                            nested_attrs = get_all_attributes(
                                inner_arg, visited.copy(), nested_prefix
                            )
                            attributes.update(nested_attrs)
        # Handle direct Pydantic models
        elif inspect.isclass(field_type) and issubclass(field_type, BaseModel):
            nested_attrs = get_all_attributes(field_type, visited.copy(), nested_prefix)
            attributes.update(nested_attrs)

    return attributes


def collect_non_none_attrs(
    obj,
    *,
    depth: int = -1,
    prefix: str | None = None,
    max_list_length: int = 5,
    _visited=None,
):
    """
    Collect a set of attribute paths whose values are not None.
    - Accepts a single object or a list of objects
    - Recursively traverses objects with __dict__
    """
    if obj is None or depth == 0:
        return set()

    if _visited is None:
        _visited = set()

    result = set()

    # ----------------------------
    # Case 1: top-level list input
    # ----------------------------
    if isinstance(obj, list):
        for item in obj[:max_list_length]:
            if item is None:
                continue

            result |= collect_non_none_attrs(
                item,
                depth=depth,
                prefix=prefix,
                max_list_length=max_list_length,
                _visited=_visited,
            )
        return result

    # ----------------------------
    # Cycle detection
    # ----------------------------
    if id(obj) in _visited:
        return set()
    _visited.add(id(obj))

    # ----------------------------
    # Non-object primitives
    # ----------------------------
    if not hasattr(obj, "__dict__"):
        return set()

    base = prefix or obj.__class__.__name__

    for key, value in obj.__dict__.items():
        if value is None:
            continue

        path = f"{base}.{key}"
        result.add(path)

        # Nested object
        if hasattr(value, "__dict__"):
            result |= collect_non_none_attrs(
                value,
                depth=depth - 1 if depth > 0 else -1,
                prefix=path,
                max_list_length=max_list_length,
                _visited=_visited,
            )

        elif isinstance(value, list):
            for item in value[:max_list_length]:
                if item is None:
                    continue

                if hasattr(item, "__dict__"):
                    result |= collect_non_none_attrs(
                        item,
                        depth=depth - 1 if depth > 0 else -1,
                        prefix=path,
                        max_list_length=max_list_length,
                        _visited=_visited,
                    )

        elif isinstance(value, dict):
            for item in value.values():
                if item is None:
                    continue

                if hasattr(item, "__dict__"):
                    result |= collect_non_none_attrs(
                        item,
                        depth=depth - 1 if depth > 0 else -1,
                        prefix=path,
                        max_list_length=max_list_length,
                        _visited=_visited,
                    )

    return result


def make_output_object(basename: str):
    # Look for basename.json in JSON_DIR and all subdirectories
    json_files = list(JSON_DIR.rglob(f"{basename}.*"))
    # Separate GBW json and property json
    gbw_json = next(
        f for f in json_files if f.suffix == ".json" and not f.name.endswith(".property.json")
    )
    property_json = next(f for f in json_files if f.name.endswith(".property.json"))

    temp_dir = Path(tempfile.mkdtemp())

    # Copy files into temp directory
    shutil.copy(gbw_json, temp_dir / gbw_json.name)
    shutil.copy(property_json, temp_dir / property_json.name)

    output_object = Output(basename=basename, working_dir=temp_dir, version_check=False)
    add_gbw_jsons(output_object, [gbw_json])

    # if json_files:
    #     # Optionally: pick the first match
    #     output_object.parse(read_gbw_json=True)
    # else:
    #     output_object.parse(read_gbw_json=False)

    return output_object


@pytest.mark.output
def test_attributes():
    created = set()
    gbw_attr = get_all_attributes(GbwResults, prefix="GbwResults")
    prop_attr = get_all_attributes(PropertyResults, prefix="PropertyResults")
    output_attr = gbw_attr.union(prop_attr)
    print(len(output_attr))
    for file in JSON_DIR.rglob("*.json"):
        basename = file.stem
        basename = basename.split(".", 1)[0]

        if basename in created:
            continue

        created.add(basename)

        output_object = make_output_object(basename)
        object_prop_attr = collect_non_none_attrs(output_object.results_properties)
        object_gbw_attr = collect_non_none_attrs(output_object.results_gbw)

        object_attr = object_gbw_attr.union(object_prop_attr)
        print(
            f"{len(output_attr.intersection(object_attr))},{output_attr.intersection(object_attr)}"
        )
        output_attr = output_attr - object_attr

        continue

    print(f"{len(output_attr)},{output_attr}")
