"""
    lottus app
    ----------

    This module implements the central lottus application object
    :copyright: Ben Chambule
    :license: MIT
"""

import abc

class Lottus(object):
    """
        Represents the Lottus running application. 

        Attributes
        ----------
        - initial_window: the first window that will be showed to client
        - windows: the windows that will be showed to the client
        - session_manager: the session manager 
        - window_cache: the cache management for the windows
        - mapped_windows: the windows that were mapped with the 'window' decorator
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
        session_nr = request['session_nr']
        request_str = request['request_str']
        cell_nr = request['cell_nr']

        session = self.session_manager.get(session_nr, cell_nr)

        window = None

        if session is None:
            session = create_session(session_nr, cell_nr, self.initial_window)

            if self.initial_window in self.mapped_windows:
                window, session = self.get_mapped_window(self.initial_window, session, request)
                if self.window_cache:
                    self.window_cache.cache(window, session_nr)
            else:
                window = self.get_window(self.initial_window)
        else:
            window, session = self.process_window(session, request)
            
        session['window'] = window['name']
        self.session_manager.save(session)

        return window

    def process_window(self, session, request):
        """
            Process the request and returns a window and the new session
            :param session `dict`: the session of the current request
            :param request `dict`: the actual request
        """
        actual_window_name = session['window']
        window = None
        actual_window = None

        if self.window_cache is not None:
            actual_window = self.window_cache.get(actual_window_name, request['session_nr'])

            if actual_window is None:
                actual_window = self.window_cache.get(actual_window_name)

        if actual_window is None and actual_window_name in self.mapped_windows:
            actual_window, old_session = self.get_mapped_window(actual_window_name, session, request)

        if actual_window is None:
            actual_window = self.get_window(actual_window_name)

        options = actual_window['options']
        window_type = actual_window['type']
        active = actual_window['active']
        required = actual_window['required'] if 'required' in actual_window else None

        session_nr = request['session_nr']
        request_str = request['request_str']
        cell_nr = request['cell_nr']

        if required is not None:
            if 'window' in required:
                if 'in_options' in required and required['in_options'] == True:
                    selected_option = self.get_selected_option(actual_window, request)

                    if selected_option:
                        if 'value' in selected_option:
                            session['variables'][required['var']] = selected_option['value']
                        else:
                            session['variables'][required['var']] = selected_option['option']
                    else:
                        actual_window['message'] = "Please select a valid option"
                        window = actual_window
                else:
                    session['variables'][required['var']] = request_str
                
                window = self.get_window(required['window'])
            else:
                create_error_window("Error processing your request")
        else:
            selected_option = self.get_selected_option(actual_window, request)

            if selected_option is None:
                actual_window['message'] = "Please select a valid option"
                window = actual_window
            else:
                if selected_option['window'] in self.mapped_windows:
                    window, session = self.get_mapped_window(selected_option['window'], session, request)

                    if self.window_cache is not None:
                        self.window_cache.cache(window, session_nr)
                else:
                    window = self.get_window(selected_option['window'])

        return window, session

    def get_selected_option(self, window, request):
        """
            Returns the selected option based on current request. None if the selected option is invalid
            :param window `dict`: the window upon which the option must be selected
            :param request `dict`: the request with the choice
        """
        options = window['options']

        return next((s for s in options if s['option'] == request['request_str']), None)

    def get_window(self, window_name):
        """
            Returns the window with the name `window_name` from the windows `dict`
            :param window_name `str`: the name of the window that must be returned. 
            None if window couldn't be found
        """
        return self.windows[window_name] if window_name in self.windows else None
        
    def get_mapped_window(self, window_name, session, request):
        """
            Returns the window and a session from the mapped_window `dict`
            :param window_name `str`: the name of the window that must be returned.
            :param session `dict`: the current session that will be passed to the window's processor
            :param request `dict`: the current request that will be passed to the window's processor
        """
        if window_name in self.mapped_windows:
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
    def get(self, window_name, session_nr = None):
        """
            Returns the window previously cached based on the window_name and/or session_nr
            :param window_name `str`: the name of the window that must be retrieved from the cache
            :param session_nr: the identifier of the session 
        """
        pass

    @abc.abstractmethod
    def cache(self, window, session_nr = None):
        """
            Adds the window the cache. If session_nr is provided then the window will be cached
            and will be attached to the session_nr, meaning that every session will have it's 
            own cached version of the window.
            :param window `dict`: the window to be cached
            :param session_nr: the identifier of the session
        """
        pass

    @abc.abstractmethod
    def delete(self, session_nr, window_name = None):
        """
            Deletes all cached windows of the session_nr. If window_name is provided only the window
            with name window_name will be deleted.
            :param session_nr: the identifier of the session
            :param window_name `str`: the name of the window to be deleted
        """
        pass


class SessionManager(object):
    """
        Represents the session manager for lottus session
    """
    @abc.abstractmethod
    def get(self, session_nr, cell_nr):
        """
            Returns session based on the session identifier and cell identifier
            :param session_nr: the session identifier
            :param cell_nr: the cell identifier
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


def create_session(session_nr, cell_nr, window_name = None, variables = None):
    """
        Returns a session `dict` to be used by lottus
        :param session_nr: the session identifier
        :param cell_nr: the cell identifier
        :param window_name `str`: the current window name
        :param variables `dict`: the variables of the session
    """
    return {
        'session_nr': session_nr, 
        'variables': variables,
        'cell_nr': cell_nr,
        'window': window_name
    }


def create_request(session_nr, cell_nr, request_str):
    """
        Returns a request `dict` to be used by lottus
        :param session_nr: the session identifier
        :param cell_nr: the cell identifier
        :param request_str: the string with the request from the client
    """
    return {'session_nr': session_nr, 'cell_nr': cell_nr, 'request_str': request_str}


def create_window(name, title, message, options=None, required=None, active=True, window_type="FORM"):
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
        'name': name, 
        'message': message,
        'title': title,
        'options': options,
        'active': active,
        'type': window_type
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
        'option': option,
        'display': display,
        'window': window,
        'active': active
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
        'var': variable,
        'window': window,
        'in_options': in_options,
        'type': var_type,
        'length': var_length
    }


def create_error_window(message):
    """
        Returns an error window
        :param message `str`: the message to be showed to the client
    """
    return create_window(name='ERROR', message=message, title='ERROR', window_type='MESSAGE')


def window_response(window):
    """
    """
    return {
        'message': window['message'] if 'message' in window else None,
        'title': window['title'] if 'title' in window else None,
        'options': [option_response(x) for x in window['options']] if 'options' in window else []
    } if window else None


def option_response(option):
    """
    """
    return {
        'option': option['option'],
        'value': option['display']
    } if option else None