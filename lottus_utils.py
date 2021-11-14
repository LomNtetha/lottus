from typing import List

from entities import Option, Window


class HttpOption:
    """

    """

    def __init__(self, option: str, display: str, value: str):
        """

        :param option:
        :param display:
        :param value:
        """
        self._option = option
        self._display = display
        self._value = value

    @property
    def option(self) -> str:
        """

        :return:
        """

        return self._option

    @property
    def display(self) -> str:
        """

        :return:
        """

        return self._display

    @property
    def value(self) -> str:
        """

        :return:
        """

        return self._value

    @classmethod
    def fromOption(cls, option: Option):
        """

        :param option:
        :return:
        """

        return HttpOption(option=option.identifier, display=option.display, value=option.value) if option else None


class HttpWindow:
    """

    """

    def __init__(self, message, title, options: List[HttpOption] = []):
        """

        :param message:
        :param title:
        :param options:
        """

        self._message = message
        self._title = title
        self._options = options

    @property
    def message(self) -> str:
        """

        :return:
        """

        return self._message

    @property
    def title(self) -> str:
        """

        :return:
        """

        return self._title

    @property
    def options(self) -> List[HttpOption]:
        """

        :return:
        """

        return self._options

    @classmethod
    def fromWindow(cls, window: Window):
        """

        :param window:
        :return:
        """

        return HttpWindow(message=window.message,
                          title=window.title,
                          options=[HttpOption.fromOption(o) for o in
                                   window.options] if window.options else []) if window else None



