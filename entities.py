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

    @window.setter
    def window(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._window = value

    @property
    def variable(self) -> str:
        """

        :return:
        """

        return self._variable

    @variable.setter
    def variable(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._variable = value

    @property
    def in_options(self) -> bool:
        """

        :return:
        """

        return self._in_options

    @in_options.setter
    def in_options(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._in_options = value

    @property
    def var_type(self) -> str:
        """

        :return:
        """

        return self.var_type

    @var_type.setter
    def var_type(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._var_type = value

    @property
    def length(self) -> int:
        """

        :return:
        """

        return self.length

    @length.setter
    def length(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._length = value


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

    @identifier.setter
    def identifier(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._identifier = value

    @property
    def phone(self) -> str:
        """

        :return:
        """

        return self._phone

    @phone.setter
    def phone(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._phone = value

    @property
    def command(self) -> str:
        """

        :return:
        """

        return self._command

    @command.setter
    def command(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._command = value


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

    @identifier.setter
    def identifier(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._identifier = value

    @property
    def display(self) -> str:
        """

        :return:
        """

        return self._display

    @display.setter
    def display(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._display = value

    @property
    def window(self) -> str:
        """

        :return:
        """

        return self._window

    @window.setter
    def window(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._window = value

    @property
    def value(self) -> str:
        """

        :return:
        """

        return self._value

    @value.setter
    def value(self, val) -> None:
        """

        :param val:
        :return:
        """
        self._value = val

    @property
    def active(self) -> bool:
        """

        :return:
        """

        return self._active

    @active.setter
    def active(self, value) -> None:
        self._active = value


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

    @identifier.setter
    def identifier(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._identifier = value

    @property
    def display(self) -> str:
        """

        :return:
        """

        return self._display

    @display.setter
    def display(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._display = value

    @property
    def window(self) -> str:
        """

        :return:
        """

        return self._window

    @window.setter
    def window(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._window = value

    @property
    def value(self) -> str:
        """

        :return:
        """

        return self._value

    @value.setter
    def value(self, val):
        self._value = val

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

    @name.setter
    def name(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._name = value

    @property
    def title(self) -> str:
        """

        :return:
        """

        return self._title

    @title.setter
    def title(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._title = value

    @property
    def message(self) -> str:
        """

        :return:
        """

        return self._message

    @message.setter
    def message(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._message = value

    @property
    def options(self) -> List[Option]:
        """

        :return:
        """

        return self._options if self._options else []

    @options.setter
    def options(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._options = value

    @property
    def window_type(self) -> WindowType:
        """

        :return:
        """

        return self._window_type

    @window_type.setter
    def window_type(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._window_type = value

    @property
    def required(self) -> Required:
        """

        :return:
        """

        return self._required

    @required.setter
    def required(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._required = value

    @property
    def active(self) -> bool:
        """

        :return:
        """

        return self._active

    @active.setter
    def active(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._active = value


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

    @session_identifier.setter
    def session_identifier(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._session_identifier = value

    @property
    def name(self) -> str:
        """

        :return:
        """

        return self._name

    @name.setter
    def name(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._name = value

    @property
    def title(self) -> str:
        """

        :return:
        """

        return self._title

    @title.setter
    def title(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._title = value

    @property
    def message(self) -> str:
        """

        :return:
        """

        return self._message

    @message.setter
    def message(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._message = value

    @property
    def options(self) -> List[GeneratedOption]:
        """

        :return:
        """

        return self._options if self._options else []

    @options.setter
    def options(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._options = value

    @property
    def window_type(self) -> WindowType:
        """

        :return:
        """

        return self._window_type

    @window_type.setter
    def window_type(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._window_type = value

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

    @name.setter
    def name(self, value) -> None:
        """

        :param value:
        :return:
        """
        self._name = value

    @property
    def value(self) -> str:
        """

        :return:
        """

        return self._value

    @value.setter
    def value(self, val) -> None:
        """

        :param val:
        :return:
        """
        self._value = val


class Session:
    """

    """

    def __init__(self, identifier, phone, current_window: str, tags: List[Tag] = []) -> None:
        """

        :param identifier:
        :param phone:
        :param current_window:
        """

        self.__identifier = identifier
        self.__phone = phone
        self.__current_window = current_window
        self.__tags = tags

    @property
    def identifier(self) -> str:
        """

        :return:
        """

        return self.__identifier

    @identifier.setter
    def identifier(self, value) -> None:
        """

        :param value:
        :return:
        """
        self.__identifier = value

    @property
    def phone(self) -> str:
        """

        :return:
        """

        return self.__phone

    @phone.setter
    def phone(self, value) -> None:
        """

        :param value:
        :return:
        """
        self.__phone = value

    @property
    def current_window(self) -> GeneratedWindow:
        """

        :return:
        """
        return self.__current_window

    @current_window.setter
    def current_window(self, value) -> None:
        """

        :param value:
        :return:
        """
        self.__current_window = value

    @property
    def tags(self) -> List[Tag]:
        """

        :return:
        """
        return self.__tags

    @tags.setter
    def tags(self, value) -> None:
        """

        :param value:
        :return:
        """
        self.__tags = value

    def add_tag(self, tag: Tag) -> None:
        self.__tags.append(tag)

    def get_tag(self, name) -> Tag:
        for t in self.__tags:
            if t.name == name:
                return t

        return None
