import abc

from entities import Session, GeneratedWindow


class GeneratedWindowProvider:
    """

    """

    @abc.abstractmethod
    def get(self, name, session_id) -> GeneratedWindow:
        """

        :param name:
        :param session_id:
        :return GeneratedWindow:
        """
        pass

    @abc.abstractmethod
    def save(self, window: GeneratedWindow) -> None:
        """

        :param window:
        :return: None
        """
        pass


class SessionProvider:
    """
        Represents the session manager for lottus session
    """

    @abc.abstractmethod
    def get(self, identifier, phone) -> Session:
        """

        :param identifier:
        :param phone:
        :return: Session
        """
        pass

    @abc.abstractmethod
    def save(self, session: Session) -> None:
        """

        :param session:
        :return:
        """
        pass

    @abc.abstractmethod
    def finish(self, session: Session) -> None:
        """

        :param session:
        :return:
        """
        pass
