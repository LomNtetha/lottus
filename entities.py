import enum
from typing import Any, List


class WindowType(str, enum.Enum):
    """

    """

    FORM = "FORM"
    MESSAGE = "MESSAGE"


class Required:
    """

    """

    def __init__(self, variable: str, window: str, in_options: bool, var_type: str, length: int):
        """

        :param variable:
        :param window:
        :param in_options:
        :param var_type:
        :param length:
        """

        self._window = window
        self._variable = variable
        self._in_options = in_options
        self._var_type = var_type
        self._length = length

    @property
    def window(self) -> str:
        """

        :return:
        """

        return self._window

    @property
    def variable(self) -> str:
        """

        :return:
        """

        return self._variable

    @property
    def in_options(self) -> bool:
        """

        :return:
        """

        return self._in_options

    @property
    def var_type(self) -> str:
        """

        :return:
        """

        return self.var_type

    @property
    def length(self) -> int:
        """

        :return:
        """

        return self.length


class Request:
    """

    """

    def __init__(self, identifier: str, phone: str, command: str):
        """

        :param identifier:
        :param phone:
        :param command:
        """

        self._identifier = identifier
        self._phone = phone
        self._command = command

    @property
    def identifier(self) -> str:
        """

        :return:
        """

        return self._identifier

    @property
    def phone(self) -> str:
        """

        :return:
        """

        return self._phone

    @property
    def command(self) -> str:
        """

        :return:
        """

        return self._command


class Option:
    """

    """

    def __init__(self, identifier: str, display: str, window: str = None, value: str = None, active: bool = True):
        """

        :param identifier:
        :param display:
        :param window:
        :param value:
        :param active:
        """

        self._identifier = identifier
        self._display = display
        self._window = window
        self._value = value
        self._active = active

    @property
    def identifier(self) -> str:
        """

        :return:
        """

        return self._identifier

    @property
    def display(self) -> str:
        """

        :return:
        """

        return self._display

    @property
    def window(self) -> str:
        """

        :return:
        """

        return self._window

    @property
    def value(self) -> str:
        """

        :return:
        """

        return self._value

    @property
    def active(self) -> bool:
        """

        :return:
        """

        return self._active


class GeneratedOption:
    """

    """

    def __init__(self, identifier: str, display: str, window: str, value: str):
        """

        :param identifier:
        :param display:
        :param window:
        :param value:
        """

        self._identifier = identifier
        self._display = display
        self._window = window
        self._value = value

    @property
    def identifier(self) -> str:
        """

        :return:
        """

        return self._identifier

    @property
    def display(self) -> str:
        """

        :return:
        """

        return self._display

    @property
    def window(self) -> str:
        """

        :return:
        """

        return self._window

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

        return GeneratedOption(identifier=option.identifier,
                               display=option.display,
                               window=option.window,
                               value=option.value)


class Window:
    """

    """

    def __init__(self, name: str, title: str, message: str, options: List[Option] = [],
                 window_type: WindowType = WindowType.FORM, required: Required = Required, active: bool = True):
        """

        :param name:
        :param title:
        :param message:
        :param options:
        :param window_type:
        :param required:
        :param active:
        """

        self._name = name
        self._title = title
        self._message = message
        self._options = options
        self._window_type = window_type
        self._required = required
        self._active = active

    @property
    def name(self) -> str:
        """

        :return:
        """

        return self._name

    @property
    def title(self) -> str:
        """

        :return:
        """

        return self._title

    @property
    def message(self) -> str:
        """

        :return:
        """

        return self._message

    @property
    def options(self) -> List[Option]:
        """

        :return:
        """

        return self._options if self._options else []

    @property
    def window_type(self) -> WindowType:
        """

        :return:
        """

        return self._window_type

    @property
    def required(self) -> Required:
        """

        :return:
        """

        return self._required

    @property
    def active(self) -> bool:
        """

        :return:
        """

        return self._active


class GeneratedWindow:
    """

    """

    def __init__(self, session_identifier: str, name: str, title: str, message: str,
                 options: List[GeneratedOption] = [], window_type: WindowType = WindowType.FORM):
        """

        :param session_identifier:
        :param name:
        :param title:
        :param message:
        :param options:
        :param window_type:
        """

        self._session_identifier = session_identifier
        self._name = name
        self._title = title
        self._message = message
        self._options = options
        self._window_type = window_type

    @property
    def session_identifier(self) -> str:
        """

        :return:
        """

        return self._session_identifier

    @property
    def name(self) -> str:
        """

        :return:
        """

        return self._name

    @property
    def title(self) -> str:
        """

        :return:
        """

        return self._title

    @property
    def message(self) -> str:
        """

        :return:
        """

        return self._message

    @property
    def options(self) -> List[GeneratedOption]:
        """

        :return:
        """

        return self._options if self._options else []

    @property
    def window_type(self) -> WindowType:
        """

        :return:
        """

        return self._window_type

    @classmethod
    def fromWindow(cls, window: Window, session_identifier: Any):
        """

        :param window:
        :param session_identifier:
        :return:
        """

        return GeneratedWindow(session_identifier=session_identifier,
                               message=window.message,
                               title=window.title,
                               window_type=window.window_type,
                               name=window.name,
                               options=[GeneratedOption.fromOption(op) for op in
                                        window.options] if window.options else [])


class Tag:
    """

    """

    def __init__(self, name, value):
        """

        :param name:
        :param value:
        """

        self._name = name
        self._value = value

    @property
    def name(self) -> str:
        """

        :return:
        """

        return self._name

    @property
    def value(self) -> str:
        """

        :return:
        """

        return self._value


class Session:
    """

    """

    def __init__(self, identifier, phone, current_window) -> None:
        """

        :param identifier:
        :param phone:
        :param current_window:
        """

        self.__identifier = identifier
        self.__phone = phone
        self.__current_window = current_window

    @property
    def identifier(self) -> str:
        """

        :return:
        """

        return self.__identifier

    @property
    def phone(self) -> str:
        """

        :return:
        """

        return self.__phone

    @property
    def current_window(self) -> GeneratedWindow:
        """

        :return:
        """
        return self.__current_window

    def set_current_window(self, current_window: GeneratedWindow):
        """

        :param current_window:
        :return:
        """
        self.__current_window = current_window

