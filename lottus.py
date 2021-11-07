"""
    lottus
    ----------

    This module implements the central lottus application object
    :copyright: Ben Chambule
    :license: MIT
"""

import abc
import enum
from typing import List
from dataclasses import dataclass, asdict


class WindowType(str, enum.Enum):
    FORM = "FORM"
    MESSAGE = "MESSAGE"


class Constants(enum.Enum):
    PHONE = "phone"
    SESSION = "session"
    COMMAND = "command"
    WINDOW = "window"
    NAME = "name"
    OPTIONS = "options"
    TYPE = "type"
    ACTIVE = "active"
    REQUIRED = "required"
    IN_OPTIONS = "in_options"
    VARIABLES = "variables"
    VALUE = "value"
    MESSAGE = "message"
    VAR = "var"
    OPTION = "option"
    DISPLAY = "display"
    TITLE = "title"
    LENGTH = "length"
    FORM = "FORM"
    ERROR = "ERROR"
    IS_NEW = "is_new"


@dataclass
class Required:
    variable: str
    window: str
    in_options: str
    var_type: str
    length: str


@dataclass
class Request:
    identifier: str
    phone: str
    command: str

    def __str__(self) -> str:
        return f"Request({str(asdict(self))}"


@dataclass
class Option:
    identifier: str
    display: str
    window: str = None
    value: str = None
    active: bool = True

    def __str__(self) -> str:
        return f"Option({str(asdict(self))}"


@dataclass
class Window:
    name: str
    title: str
    message: str
    options: List[Option]
    window_type: WindowType = WindowType.FORM
    required: Required = None
    active: bool = True

    def __str__(self) -> str:
        return f"Window{str(asdict(self))}"


@dataclass
class Session:
    identifier: str
    phone: str
    is_new: bool
    actual_command: str
    window: Window = None
    variables: List[str] = None

    def add_variable(self) -> None:
        pass

    def __str__(self) -> str:
        return f"Session{str(asdict(self))}"


class SessionManager(object):
    """
        Represents the session manager for lottus session
    """

    @abc.abstractmethod
    def get(self, session_id, phone) -> Session:
        """
            Returns session based on the session identifier and cell identifier
            :param session_id: the session identifier
            :param phone: the cell identifier
        """
        pass

    @abc.abstractmethod
    def save(self, session: Session):
        """
            Saves the session
        """
        pass

    @abc.abstractmethod
    def finish(self, session: Session):
        """
            Terminates the session
        """
        pass


class Lottus:
    """
        Represents the Lottus running application. 

        Attributes
        ----------
        - initial_window: the first window that will be showed to client
        - windows: the windows that will be showed to the client
        - session_manager: the session manager
        - mapped_windows: the windows that were mapped with the Constants.WINDOW decorator
    """

    def __init__(self, initial_window: str, windows: List[Window], session_manager: SessionManager):
        """
            Initializes the Lottus application
        """

        self.windows = {}
        for window in windows if windows else []:
            if window.active:
                self.windows[window.name] = window

        self.initial_window = initial_window

        self.session_manager = session_manager
        self.mapped_windows = {}

    def process_request(self, request: Request) -> Window:
        """
            Processes the request and returns the window generated
        """

        session = self.session_manager.get(request.identifier, request.phone)

        if session is None:
            session = Session(identifier=request.identifier, phone=request.phone, actual_command=request.command,
                              is_new=True)

            if self.initial_window in self.mapped_windows:
                session = self.process_session(session, self.initial_window)
            else:
                session = self.process_session(session, self.initial_window)
        else:
            session.is_new = False
            session.actual_command = request.command

            if session.window.window_type == WindowType.MESSAGE:
                # TODO: throw exception
                pass
            session = self.process_window(session)

        if session.window.window_type == WindowType.MESSAGE:
            self.session_manager.finish(session)
        else:
            self.session_manager.save(session)

        return session.window

    def process_window(self, session: Session) -> Session:
        """
            Process the request and returns a window and the new session
        """

        window = None

        if not window:
            if session.window.name in self.mapped_windows:
                session = self.process_session(session)
            else:
                selected_option = self.get_selected_option(session.window, session.actual_command)

                if not selected_option:
                    session.window.message = "Please select a valid option"
                elif selected_option:
                    session = self.process_session(session, window_name=selected_option.window)
                else:
                    session = self.process_session(session)

        else:
            session.window = window

        return session

    @staticmethod
    def get_selected_option(window: Window, command: str) -> Option:
        """
            Returns the selected option based on current request. None if the selected option is invalid
        """

        return next((o for o in window.options if o.identifier == command), None)

    def process_session(self, session: Session, window_name: str = None) -> Session:
        """
            :param session:
            :param window_name:
        """

        # TODO: throw exception when window is not found
        if window_name:
            if self.windows and window_name in self.windows:
                window = self.windows[window_name]
                session.window = window

            elif self.mapped_windows and window_name in self.mapped_windows:
                processor = self.mapped_windows[window_name]
                session = processor(session)
        elif session.window:
            if self.windows and session.window.name in self.windows:
                window = self.windows[session.window.name]
                session.window = window

            elif self.mapped_windows and session.window.name in self.mapped_windows:
                processor = self.mapped_windows[session.window.name]
                session = processor(session)

        return session

    def window(self, window_name):
        """
            A decorator that is used to register a new processor for a window_name
        """

        def decorator(f):
            self.add_window_rule(window_name, f)
            return f

        return decorator

    def add_window_rule(self, window_name, f):
        """
            Maps the window to the function
        """

        self.mapped_windows[window_name] = f

    def __str__(self) -> str:
        return f"Lottus({dict([('initial_window', self.initial_window), ('windows', self.windows), ('mapped_windows', self.mapped_windows)])})"
