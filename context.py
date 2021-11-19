from typing import Dict

from entities import Session, GeneratedWindow, Tag, WindowType
from exceptions import WindowNotFoundError, InvalidSelectedOptionError, ProcessorNotFoundError, \
    ProcessorInvalidReturnError, SessionAlreadyFinishedError


class LottusContext:
    """

    """

    def __init__(self, initial_window: str, current_session: Session, processors: Dict) -> None:
        """

        :param initial_window:
        :param current_session:
        :param processors:
        """

        if not initial_window or not isinstance(initial_window, str):
            raise ValueError("initial window cannot be empty nor null")

        if not current_session or not isinstance(current_session, Session):
            raise ValueError("current session cannot be null")

        if not processors or not isinstance(processors, Dict):
            raise ValueError("processors cannot be null")

        if initial_window not in processors:
            raise WindowNotFoundError(None, f"Window {initial_window} not found in the processors list")

        self.__processors = processors
        self.__currentSession = current_session
        self.__initial_window = initial_window

    def set_current_window(self, current_window: GeneratedWindow) -> None:
        """

        :param current_window:
        :return:
        """

        self.__currentSession.current_window = current_window

    @property
    def current_window(self) -> GeneratedWindow:
        """

        :return:
        """

        return self.__currentSession.current_window

    def add_tag(self, name, value=None) -> None:
        """

        :param name:
        :param value:
        :return:
        """

        if not name:
            raise ValueError("Invalid argument 'name'")

        self.__currentSession.add_tag(Tag(name, value))

    @property
    def current_session(self) -> Session:
        """

        :return:
        """

        return self.__currentSession

    def call_processor(self, processor_name: str, command: str) -> GeneratedWindow:
        """

        :param command:
        :param processor_name:
        :return:
        """
        if processor_name in self.__processors:
            processor = self.__processors[processor_name]
        else:
            raise ProcessorNotFoundError(None, f"No processor found for window {processor_name}")

        return processor(processor_name, command)

    def process_command(self, command: str) -> GeneratedWindow:
        """

        :param command:
        :return:
        """

        current_window = self.current_session.current_window

        if current_window.window_type == WindowType.MESSAGE:
            raise SessionAlreadyFinishedError(None, "Current session already finished")

        if not current_window:
            processor = self.__processors.get(self.__initial_window)
        else:
            processor = self.__processors.get(current_window.name)

        if not processor:
            raise ProcessorNotFoundError(None, f"Processor for window {current_window.name} not found")

        generated_window = processor(self, command)

        if not generated_window or not isinstance(generated_window, GeneratedWindow):
            raise ProcessorInvalidReturnError(
                None,
                f"Processor {processor} for window {current_window.name} returned an invalid response")

        generated_window.previous_window = current_window

        return generated_window

    @property
    def processors(self) -> Dict:
        """

        :return:
        """

        return self.__processors
