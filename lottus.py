import abc

class Lottus(object):
    """
    """
    def __init__(self, initial_window, windows, session_context, window_cache = None):
        """
        """
        self.initial_window = initial_window
        self.windows = windows
        self.session_context = session_context
        self.window_cache = window_cache
        self.mapped_windows = {}

    def process_request(self, request):
        """
        """
        session_nr = request['session_nr']
        request_str = request['request_str']
        cell_nr = request['cell_nr']

        session = self.session_context.get(session_nr, cell_nr)

        window = None

        if session is None:
            session = self.session_context.create(session_nr, cell_nr)

            if self.initial_window in self.mapped_windows:
                window, session = self.get_mapped_window(self.initial_window, session, request)
                if self.window_cache:
                    self.window_cache.cache(window, session_nr)
            else:
                window = self.get_window(self.initial_window)
        else:
            window, session = self.process_window(session, request)
            
        session['window'] = window['name']
        self.session_context.save(session)

        return window

    def process_window(self, session, request):
        """
        """
        actual_window_name = session['window']
        window = None
        actual_window = None

        if self.window_cache is not None:
            actual_window = self.window_cache.get(actual_window_name, request['session_nr'])

            if actual_window is None:
                actual_window = self.window_cache.get(actual_window_name)

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
        """
        options = window['options']

        return next((s for s in options if s['option'] == request['request_str']), None)

    def get_window(self, window_name):
        """
        """
        return self.windows[window_name] if window_name in self.windows else None
        
    def get_mapped_window(self, window_name, session, request):
        """
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
        """
        self.mapped_windows[window_name] = f


class WindowCache(object):
    @abc.abstractmethod
    def get(self, window, session_nr = None):
        """
        """
        pass

    @abc.abstractmethod
    def cache(self, window, session_nr = None):
        """
        """
        pass


class SessionContext(object):
    @abc.abstractmethod
    def get(self, session_nr, cell_nr):
        """
        """
        pass
    
    @abc.abstractmethod
    def save(self, session):
        """
        """
        pass

    @abc.abstractmethod
    def create(self, session_nr, cell_nr):
        """
        """
        pass

    @abc.abstractmethod
    def finish(self, session):
        """
        """
        pass

def create_session(session_nr, cell_nr, window = None, variables = None):
    """
    """
    return {
        'session_nr': session_nr, 
        'variables': variables,
        'cell_nr': cell_nr,
        'window': window
    }

def create_request(session_nr, cell_nr, request_str):
    """
    """
    return {'session_nr': session_nr, 'cell_nr': cell_nr, 'request_str': request_str}


def create_window(name, title, message, options=None, active=True, window_type="FORM"):
    """
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
    """
    return {
        'option': option,
        'display': display,
        'window': window,
        'active': active
    }

def create_required(variable, window, in_options=False, var_type='numeric', var_length='11'):
    """
    """
    return {
        'var': variable,
        'window': window,
        'in_options': in_options,
        'type': var_type,
        'length': var_length
    }

def create_error_window(message):
    return create_window(name='ERROR', message=message, title='ERROR', window_type='END')