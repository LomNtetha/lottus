from context import LottusContext
from entities import GeneratedWindow, Session, Request
from providers import SessionProvider, GeneratedWindowProvider


class Lottus(object):
    """
        Represents the Lottus running application. 

        Attributes
        ----------
        - initial_window: the first window that will be showed to client
        - windows: the windows that will be showed to the client
        - session_manager: the session manager
        - mapped_windows: the windows that were mapped with the Constants.WINDOW decorator
    """

    def __init__(self,
                 initial_window: str, session_provider: SessionProvider, window_provider: GeneratedWindowProvider):
        """

        :param initial_window:
        :param session_provider:
        :param window_provider:
        """

        if not initial_window or not isinstance(initial_window, str):
            raise ValueError("Invalid argument initial window")

        if not session_provider or not isinstance(session_provider, SessionProvider):
            raise ValueError("Invalid argument session provider")

        if not window_provider or not isinstance(window_provider, GeneratedWindowProvider):
            raise ValueError("window provider cannot be empty nor null")

        self.__session_provider = session_provider
        self.__initial_processor = initial_window
        self.__processors = {}
        self.__window_manager = window_provider

    def process_request(self, request: Request) -> GeneratedWindow:
        """

        :param request:
        :return:
        """

        if not request or not isinstance(request, Request):
            raise ValueError("Invalid argument request")

        if not request.identifier:
            raise ValueError("identifier cannot be null")

        if not request.command:
            raise ValueError("command cannot be null")

        if not request.phone:
            raise ValueError("phone cannot be null")

        session = self.__session_provider.get(identifier=request.identifier, phone=request.phone)

        if not session:
            session = Session(identifier=request.identifier, phone=request.phone, current_window=None)

        lottus_context = LottusContext(self.__initial_processor, current_session=session, processors=self.__processors)

        window = lottus_context.process_command(request.command)

        session.set_current_window(window)
        self.__session_provider.save(session)
        self.__window_manager.save(window)

        return window

    def processor(self, processor_name):
        """

        :param processor_name:
        :return:
        """

        def decorator(f):
            self.add_processor_rule(processor_name, f)
            return f

        return decorator

    def add_processor_rule(self, window_name, f):
        """

        :param window_name:
        :param f:
        :return:
        """

        self.__processors[window_name] = f

    def __str__(self) -> str:
        return f"Lottus({dict([('initial_window', self.__initial_processor), ('mapped_windows', self.__processors)])})"
