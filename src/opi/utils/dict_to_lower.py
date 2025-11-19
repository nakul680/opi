from typing import Any


def dict_to_lower(
    obj: dict[str, Any],
) -> dict[str, Any] | list[dict[str, Any]]:
    """
    Recursively convert all key values in a dictionary to lowercase.

    Parameters
    ----------
    obj: dict
        Dictionary to convert to lowercase.

    Returns
    -------
    dict
        Dictionary converted to lowercase.

    """
    if isinstance(obj, dict):
        return {k.lower(): dict_to_lower(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [dict_to_lower(item) for item in obj]
    else:
        return obj
