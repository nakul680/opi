from pygments.lexers import functional

from opi.input.simple_keywords import SimpleKeyword


class LibxcKeyword(SimpleKeyword):
    """
    Class to model LibXC keywords.

    Attributes
    ----------
    functional: SimpleKeyword
        DFT functional used.
    """
    functional: SimpleKeyword

    def __init__(self, functional: SimpleKeyword):
        super().__init__(f"LibXC({functional.keyword})")
        self.functional = functional


    def __call__(self, functional: SimpleKeyword | str) -> SimpleKeyword:
        if isinstance(functional, str):
            functional = SimpleKeyword(functional)
        elif not isinstance(functional, SimpleKeyword):
            raise TypeError(
                f"Functional '{functional}' must be a SimpleKeyword or str, got {type(functional).__name__}")

        return SimpleKeyword(f"LibXC({functional.keyword})")
