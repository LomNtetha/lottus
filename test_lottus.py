from abc import ABC

from lottus import *
import random


def get_windows() -> List[Window]:
    return [
        Window(name="INITIAL", title="Ben Chambule's USSD - CV", message="Select language/Escolha idioma", options=[
            Option(identifier="1", display="Portugues", window="INFO_PT"),
            Option(identifier="2", display="English", window="INFO_EN")
        ]),
        Window(name="INFO_EN", title="English", message="Please select on of the options", options=[
            Option(identifier="1", display="Basic Information", window="BASIC_INFO_EN"),
            Option(identifier="2", display="Skills", window="SKILLS_INFO_EN"),
            Option(identifier="3", display="Contact", window="CONTACT_INFO_EN"),
            Option(identifier="4", display="Academic Formation", window="Academic_INFO_EN"),
            Option(identifier="5", display="Change Languague", window="INITIAL")
        ])
    ]


def create_lottus_app():
    class InMemorySessionManager(SessionManager, ABC):
        def __init__(self):
            self._sessions: List[Session] = []

        def get(self, session_id, phone):
            return next((s for s in self._sessions if s.identifier == session_id and s.phone == phone), None)

        def save(self, session):
            self._sessions.append(session)

    lottus_app = Lottus('INITIAL', get_windows(), InMemorySessionManager())

    @lottus_app.window('INFO_PT')
    def portuguese_window(session):
        session.window = Window(name="INFO_PT", title="Portugues", message="Por favor selecione uma das opcoes", options=[
            Option(identifier="1", display="Informacao basica", window="BASIC_INFO_PT"),
            Option(identifier="2", display="Habilidades", window="SKILLS_INFO_PT"),
            Option(identifier="3", display="Contacto", window="CONTACT_INFO_PT"),
            Option(identifier="4", display="Formacao academica", window="Academic_INFO_PT"),
            Option(identifier="5", display="Mudar idioma", window="INITIAL")
        ])

        return session

    return lottus_app


def test_must_return_portuguese_menu():
    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(Request(identifier=session_id, phone=phone, command=8745))

    assert window.name == 'INITIAL'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="1"))

    assert window.name == 'INFO_PT'


def test_must_return_english_menu():
    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(Request(identifier=session_id, phone=phone, command=8745))

    assert window.name == 'INITIAL'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="2"))

    assert window.name == 'INFO_EN'


def test_must_return_initial_menu():
    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(Request(identifier=session_id, phone=phone, command=8745))

    assert window.name == 'INITIAL'


def test_must_return_error_menu():
    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(Request(identifier=session_id, phone=phone, command=8745))

    assert window.name == 'INITIAL'

    window = app.process_request(Request(identifier=session_id, phone=phone, command="3"))

    assert window.name == 'INITIAL'
