"""
    lottus
    ----------

    This module implements the central lottus application object
    :copyright: Ben Chambule
    :license: MIT
"""

import abc
import enum

from flask.globals import session

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


class Lottus(object):
    """
        Represents the Lottus running application. 

        Attributes
        ----------
        - initial_window: the first window that will be showed to client
        - windows: the windows that will be showed to the client
        - session_manager: the session manager 
        - window_cache: the cache management for the windows
        - mapped_windows: the windows that were mapped with the Constants.WINDOW decorator
    """
    def __init__(self, initial_window, windows, session_manager, window_cache = None):
        """
            Initializes the Lottus application

            :param initial_window `str`: indicates the starting point of the application. The first window
            that will be showed to the client. 
            :param windows `dict`: a dictionary of windows
            :param session_manager `SessionManager`: the session manager of Lottus
            :param window_cache `WindowCache`: the cache management for the windows
        """
        self.initial_window = initial_window
        self.windows = windows
        self.session_manager = session_manager
        self.window_cache = window_cache
        self.mapped_windows = {}

    def process_request(self, request):
        """
            Processes the request and returns the window generated
            :param request: a `dict` request
        """
        session_id = request[Constants.SESSION.value]
        phone = request[Constants.PHONE.value]

        session = self.session_manager.get(session_id, phone)

        window = None

        if session is None:
            session = create_session(session_id, phone, True, self.initial_window)

            if self.initial_window in self.mapped_windows:
                window, session = self.get_window(self.initial_window, session, request)
                if self.window_cache:
                    self.window_cache.cache(window, session_id)
            else:
                window = self.get_window(self.initial_window, session, request)
        else:
            session[Constants.IS_NEW.value] = False
            window, session = self.process_window(session, request)
 
        session[Constants.WINDOW.value] = window[Constants.NAME.value]
        self.session_manager.save(session)

        return window

    def process_window(self, session, request):
        """
            Process the request and returns a window and the new session
            :param session `dict`: the session of the current request
            :param request `dict`: the actual request
        """
        actual_window_name = session[Constants.WINDOW.value]
        window = None
        actual_window = None

        if self.window_cache is not None:
            actual_window = self.window_cache.get(actual_window_name, request[Constants.SESSION.value])

            if actual_window is None:
                actual_window = self.window_cache.get(actual_window_name)

        if actual_window is None and actual_window_name in self.mapped_windows:
            actual_window, session = self.get_window(actual_window_name, session, request)

        print(f"actual window - {actual_window} - {type(actual_window)}")

        options = actual_window[Constants.OPTIONS.value]
        window_type = actual_window[Constants.TYPE.value]
        active = actual_window[Constants.ACTIVE.value]
        required = actual_window[Constants.REQUIRED.value] if Constants.REQUIRED.value in actual_window else None

        session_id = request[Constants.SESSION.value]
        command = request[Constants.COMMAND.value]
        phone = request[Constants.PHONE.value]

        if required is not None:
            if Constants.WINDOW.value in required:
                if Constants.IN_OPTIONS.value in required and required[Constants.IN_OPTIONS.value] == True:
                    selected_option = self.get_selected_option(actual_window, request)

                    if selected_option:
                        if Constants.VALUE.value in selected_option:
                            session[Constants.VARIABLES.value][required[Constants.VAR.value]] = selected_option[Constants.VALUE.value]
                        else:
                            session[Constants.VARIABLES.value][required[Constants.VAR.value]] = selected_option[Constants.OPTION.value]
                    else:
                        actual_window[Constants.MESSAGE.value] = "Please select a valid option"
                        window = actual_window
                else:
                    session[Constants.VARIABLES.value][required[Constants.VAR.value]] = command
                
                window, session = self.get_window(required[Constants.WINDOW.value, session, request])
            else:
                create_error_window("Error processing your request")
        else:
            selected_option = self.get_selected_option(actual_window, request)

            if selected_option is None:
                actual_window[Constants.MESSAGE.value] = "Please select a valid option"
                window = actual_window
            else:
                if selected_option[Constants.WINDOW.value] in self.mapped_windows:
                    window, session = self.get_window(selected_option[Constants.WINDOW.value], session, request)

                    if self.window_cache is not None:
                        self.window_cache.cache(window, session_id)
                else:
                    window = self.get_window(selected_option[Constants.WINDOW.value], session, request)

        return window, session

    def get_selected_option(self, window, request):
        """
            Returns the selected option based on current request. None if the selected option is invalid
            :param window `dict`: the window upon which the option must be selected
            :param request `dict`: the request with the choice
        """
        options = window[Constants.OPTIONS.value] if window[Constants.OPTIONS.value] else []

        return next((o for o in options if o[Constants.OPTION.value] == request[Constants.COMMAND.value]), None)
        
    def get_window(self, window_name, session, request):
        """
            Returns the window and a session from the mapped_window `dict`
            :param window_name `str`: the name of the window that must be returned.
            :param session `dict`: the current session that will be passed to the window's processor
            :param request `dict`: the current request that will be passed to the window's processor
        """
        if self.windows and window_name in self.windows:
            window = self.windows[window_name]

        elif self.mapped_windows and window_name in self.mapped_windows:
            processor = self.mapped_windows[window_name]
            window, session = processor(session, request)

        return window, session

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
            :param window_name `str`: the window_name
            :param f `function`: the function to be mapped to window_name
        """
        self.mapped_windows[window_name] = f


class WindowCache(object):
    """
        Represents the cache object for lottus windows
    """
    @abc.abstractmethod
    def get(self, window_name, session_id = None):
        """
            Returns the window previously cached based on the window_name and/or session_id
            :param window_name `str`: the name of the window that must be retrieved from the cache
            :param session_id: the identifier of the session 
        """
        pass

    @abc.abstractmethod
    def cache(self, window, session_id = None):
        """
            Adds the window the cache. If session_id is provided then the window will be cached
            and will be attached to the session_id, meaning that every session will have it's 
            own cached version of the window.
            :param window `dict`: the window to be cached
            :param session_id: the identifier of the session
        """
        pass

    @abc.abstractmethod
    def delete(self, session_id, window_name = None):
        """
            Deletes all cached windows of the session_id. If window_name is provided only the window
            with name window_name will be deleted.
            :param session_id: the identifier of the session
            :param window_name `str`: the name of the window to be deleted
        """
        pass


class SessionManager(object):
    """
        Represents the session manager for lottus session
    """
    @abc.abstractmethod
    def get(self, session_id, phone):
        """
            Returns session based on the session identifier and cell identifier
            :param session_id: the session identifier
            :param phone: the cell identifier
        """
        pass
    
    @abc.abstractmethod
    def save(self, session):
        """
            Saves the session
            :param session `dict`: the session to be saved
        """
        pass

    @abc.abstractmethod
    def finish(self, session):
        """
            Terminates the session
            :param session `dict`: the session to be saved
        """
        pass


def create_session(session_id, phone, is_new, window_name = None, variables = None):
    """
        Returns a session `dict` to be used by lottus
        :param session_id: the session identifier
        :param phone: the cell identifier
        :param window_name `str`: the current window name
        :param variables `dict`: the variables of the session
    """
    return {
        Constants.SESSION.value: session_id, 
        Constants.VARIABLES.value: variables,
        Constants.PHONE.value: phone,
        Constants.WINDOW.value: window_name,
        Constants.IS_NEW.value: is_new
    }


def create_request(session_id, phone, command):
    """
        Returns a request `dict` to be used by lottus
        :param session_id: the session identifier
        :param phone: the cell identifier
        :param command: the string with the request from the client
    """
    return {Constants.SESSION.value: session_id, Constants.PHONE.value: phone, Constants.COMMAND.value: command}


def create_window(name, title, message, options=None, required=None, active=True, window_type=Constants.FORM.value):
    """
        Returns a window `dict` to be used by lottus
        :param name `str`: name of the window
        :param title `str`: title of the window
        :param message `str`: message of the window
        :param options `list`: list of `dict` options from which the client must choose
        :param required `dict`: the variable that will be created and stored in the session
        :param active `bool`: indicates whether the window will be showed to the client
        :param window_type `str`: indicates whether the will is a FORM or a MESSAGE
    """
    return {
        Constants.NAME.value: name, 
        Constants.MESSAGE.value: message,
        Constants.TITLE.value: title,
        Constants.OPTIONS.value: options,
        Constants.ACTIVE.value: active,
        Constants.TYPE.value: window_type
    }


def create_option(option, display, window, active=True):
    """
        Returns an option `dict` to be used by lottus
        :param option `str`: the value of the option
        :param option `str`: the value that will be displayed
        :param window `str`: the name of the window that this option points to
        :param active `bool`: indicates wheter the option will be showed to the client
    """
    return {
        Constants.OPTION.value: option,
        Constants.DISPLAY.value: display,
        Constants.WINDOW.value: window,
        Constants.ACTIVE.value: active
    }


def create_required(variable, window, in_options=False, var_type='numeric', var_length='11'):
    """
        Returns the required `dict` to be used by lottus
        :param variable `str`: the variable of that will be stored in the session
        :param window `str`: the name of the window that this required object points to
        :param in_options `bool`: indicates whether the value to be stored will be found in the options list
        :param var_type `str`: indicates the type of the variable
        :param var_length `str`: indicates the length of the variable
    """
    return {
        Constants.VAR.value: variable,
        Constants.WINDOW.value: window,
        Constants.IN_OPTIONS.value: in_options,
        Constants.TYPE.value: var_type,
        Constants.LENGTH.value: var_length
    }


def create_error_window(message):
    """
        Returns an error window
        :param message `str`: the message to be showed to the client
    """
    return create_window(name=Constants.ERROR.value, message=message, title=Constants.ERROR.value, window_type=Constants.MESSAGE.value)


def window_response(window):
    """
    """
    return {
        Constants.MESSAGE.value: window[Constants.MESSAGE.value] if Constants.MESSAGE.value in window else None,
        Constants.TITLE.value: window[Constants.TITLE.value] if Constants.TITLE.value in window else None,
        Constants.OPTIONS.value: [option_response(x) for x in window[Constants.OPTIONS.value]] if Constants.OPTIONS.value in window else []
    } if window else None


def option_response(option):
    """
    """
    return {
        Constants.OPTION.value: option[Constants.OPTION.value],
        Constants.VALUE.value: option[Constants.DISPLAY.value]
    } if option else None