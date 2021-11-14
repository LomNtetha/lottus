import random
from typing import List

import pytest

from entities import Window, Option
from exceptions import InvalidSelectedOptionError
from lottus import *


def create_lottus_app():
    """

    :return:
    """

    class InMemorySessionProvider(SessionProvider):
        """

        """

        def __init__(self):
            """

            """

            self._sessions: List[Session] = []

        def get(self, identifier, phone) -> Session:
            """

            :param identifier:
            :param phone:
            :return:
            """

            return next((s for s in self._sessions if s.identifier == identifier and s.phone == phone), None)

        def save(self, session) -> None:
            """

            :param session:
            :return:
            """

            sess = self.get(session.identifier, session.phone)
            if not sess:
                self._sessions.append(session)
            else:
                self._sessions.remove(session)
                self._sessions.append(sess)

        def finish(self, session: Session) -> None:
            """

            :param session:
            :return:
            """
            sess = self.get(session.identifier, session.phone)
            self._sessions.remove(sess)

    class InMemoryGeneratedWindowProvider(GeneratedWindowProvider):
        """

        """

        def __init__(self):
            """

            """

            self.__windows: List[GeneratedWindow] = []

        def get(self, name, session_id) -> GeneratedWindow:
            """

            :param name:
            :param session_id:
            :return:
            """

            return next((s for s in self.__windows if s.session_identifier == session_id and s.name == name), None)

        def save(self, window: GeneratedWindow) -> None:
            """

            :param window:
            :return:
            """

            win = self.get(window.name, window.session_identifier)
            if not win:
                self.__windows.append(window)
            else:
                self.__windows.remove(win)
                self.__windows.append(window)

    lottus_app = Lottus(initial_window='INITIAL',
                        session_provider=InMemorySessionProvider(),
                        window_provider=InMemoryGeneratedWindowProvider())

    @lottus_app.processor('INFO_PT')
    def info_pt(lottus_context: LottusContext, command: str) -> GeneratedWindow:
        """

        :param lottus_context:
        :param command:
        :return:
        """

        return GeneratedWindow.fromWindow(
            Window(name="INFO_PT", title="Portugues", message="Por favor selecione uma das opcoes",
                   options=[
                       Option(identifier="1", display="Informacao basica", window="BASIC_INFO_PT"),
                       Option(identifier="2", display="Habilidades", window="SKILLS_INFO_PT"),
                       Option(identifier="3", display="Contacto", window="CONTACT_INFO_PT"),
                       Option(identifier="4", display="Formacao academica", window="Academic_INFO_PT"),
                       Option(identifier="5", display="Mudar idioma", window="INITIAL")
                   ]),
            session_identifier=lottus_context.current_session.identifier
        )

    @lottus_app.processor('BASIC_INFO_PT')
    def basic_info_pt(lottus_context: LottusContext, command: str) -> GeneratedWindow:
        """

        :param lottus_context:
        :param command:
        :return:
        """

        return GeneratedWindow.fromWindow(
            Window(name="BASIC_INFO_PT", title="Portugues", message="Benjamim Chambule\nProject manager @ VM.CO.MZ"),
            session_identifier=lottus_context.current_session.identifier
        )

    @lottus_app.processor("INITIAL")
    def initial(lottus_context: LottusContext, command: str) -> GeneratedWindow:
        """

        :param lottus_context:
        :param command:
        :return:
        """

        return GeneratedWindow.fromWindow(
            Window(name="INITIAL", title="Ben Chambule's USSD - CV", message="Select language/Escolha idioma",
                   options=[
                       Option(identifier="1", display="Portugues", window="INFO_PT"),
                       Option(identifier="2", display="English", window="INFO_EN")
                   ]),
            session_identifier=lottus_context.current_session.identifier
        )

    @lottus_app.processor("INFO_EN")
    def info_en(lottus_context: LottusContext, command: str) -> GeneratedWindow:
        """

        :param lottus_context:
        :param command:
        :return:
        """

        return GeneratedWindow.fromWindow(
            Window(name="INFO_EN", title="English", message="Please select on of the options", options=[
                Option(identifier="1", display="Basic Information", window="BASIC_INFO_EN"),
                Option(identifier="2", display="Skills", window="SKILLS_INFO_EN"),
                Option(identifier="3", display="Contact", window="CONTACT_INFO_EN"),
                Option(identifier="4", display="Academic Formation", window="Academic_INFO_EN"),
                Option(identifier="5", display="Change Language", window="INITIAL")
            ]),
            session_identifier=lottus_context.current_session.identifier
        )

    return lottus_app


def test_must_return_portuguese_window() -> None:
    """

    :return:
    """

    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258840000000'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="hello"))

    assert window.name == 'INITIAL'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="1"))

    assert window.name == 'INFO_PT'


def test_must_return_basic_info_pt_window() -> None:
    """

    :return:
    """

    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258840000000'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="hello"))

    assert window.name == 'INITIAL'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="1"))

    assert window.name == 'INFO_PT'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="1"))

    assert window.name == 'BASIC_INFO_PT'


def test_must_return_english_window() -> None:
    """

    :return:
    """

    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258840000000'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="ola"))

    assert window.name == 'INITIAL'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="2"))

    assert window.name == 'INFO_EN'


def test_must_return_initial_window() -> None:
    """

    :return:
    """

    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258840000000'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="hola"))

    assert window.name == 'INITIAL'


def test_must_return_error_menu() -> None:
    """

    :return:
    """

    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258840000000'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="hi"))

    assert window.name == 'INITIAL'

    with pytest.raises(Exception):
        app.process_request(Request(identifier=session_id, phone=phone, command="3"))


@pytest.mark.xfail(raises=InvalidSelectedOptionError)
def test_must_raise_an_exception() -> None:
    """

    :return:
    """

    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258840000000'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="hey"))

    assert window.name == 'INITIAL'

    with pytest.raises(Exception):
        app.process_request(Request(identifier=session_id, phone=phone, command="3"))
