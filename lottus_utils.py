from dataclasses import dataclass, field, asdict

from lottus import Option, Window


@dataclass
class HttpOption:
    option: str
    display: str
    value: str

    def __str__(self) -> str:
        return f"HttpOption{str(asdict(self))}"


@dataclass
class HttpWindow:
    message: str
    title: str
    options: list[HttpOption] = field(default_factory=list)

    def __str__(self) -> str:
        return f"HttpWindow{str(asdict(self))}"


def create_window(window: Window) -> HttpWindow:
    """ """

    return HttpWindow(message=window.message,
                      title=window.title,
                      options=[create_option(o) for o in window.options] if window.options else []) if window else None


def create_option(option: Option) -> HttpOption:
    """
    """

    return HttpOption(option=option.identifier, display=option.display, value=option.value) if option else None
