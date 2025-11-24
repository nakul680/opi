from typing import Any


def dict_to_lower(obj: dict[str, Any] | list[Any] | Any) -> dict[str, Any] | list[Any] | Any:
    """
    Recursively convert all key values in a dictionary to lowercase.

    This function iterates through dictionaries and values in the dictionary
    - If `obj` is a dictionary, all keys are converted to lowercase.
    - If `obj` is a list, each element is passed to this function recursively.
    - All other values are returned unchanged

    Parameters
    ----------
    obj: dict | list | Any
        The object to convert to lowercase. Can be a dictionary, a list of dictionaries or any other type.

    Returns
    -------
    dict | list | Any
        Processed object with all key values converted to lowercase.

    """
    if isinstance(obj, dict):
        return {k.lower() if isinstance(k, str) else k: dict_to_lower(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [dict_to_lower(item) for item in obj]
    else:
        return obj
