from opi.output.models.json_loadable import JSONLoadable


class OutResults(JSONLoadable):
    dgsolv: list[list[list[float]]]