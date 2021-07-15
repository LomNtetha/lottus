from lottus import *
import random

windows = {
    "INITIAL": {
        "name": "INITIAL",
        "title": "Ben Chambule's USSD - CV",
        "message": "Please select your languange of choice",
        "options": [
            {"option": "1", "display": "English", "window": "ENGLISH", "active": True},
            {"option": "2", "display": "Portuguese", "window": "PORTUGUESE", "active": True}
        ],
        "type": "FORM",
        "active": True
    },
    
    "ENGLISH": {
        "name": "ENGLISH",
        "title": "English window",
        "message": "Please select one of the options",
        "options": [
            {"option": "1", "display": "Basic information", "window": "BASIC_INFO_EN", "active": True},
            {"option": "2", "display": "Skills", "window": "SKILLS_EN", "active": True},
            {"option": "3", "display": "Contact", "window": "CONTACT_EN", "active": True},
            {"option": "4", "display": "Academic Formation", "window": "ACADEMIC_EN", "active": True},
            {"option": "5", "display": "Change language", "window": "INITIAL", "active": True}
        ],
        "type": "FORM",
        "active": True
    }
}

def create_lottus_app():
    class InMemorySessionManager(SessionManager):
        def __init__(self):
            self._sessions = []

        def get(self, session_id, phone):
            return next((s for s in self._sessions if s['session_id'] == session_id and s['phone'] == phone), None)

        def save(self, session):
            self._sessions.append(session)

    lottus_app = Lottus('INITIAL', windows, InMemorySessionManager())

    @lottus_app.window('PORTUGUESE')
    def portuguese_window(session, request):
        window = {
            "name": "PORTUGUESE",
            "title": "Portuguese window",
            "message": "Por favor seleccione uma das opcoes",
            "options": [
                {"option": "1", "display": "Basic information", "window": "BASIC_INFO_PT", "active": True},
                {"option": "2", "display": "Skills", "window": "SKILLS_PT", "active": True},
                {"option": "3", "display": "Contact", "window": "CONTACT_PT", "active": True},
                {"option": "4", "display": "Academic Formation", "window": "ACADEMIC_PT", "active": True},
                {"option": "5", "display": "Change language", "window": "INITIAL", "active": True}
            ],
            "type": "FORM",
            "active": True
        }

        return window, session
    
    return lottus_app

def test_must_return_portuguese_menu():
    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(create_request(session_id=session_id, phone=phone, command=8745))

    assert window['name'] == 'INITIAL'

    window = app.process_request(create_request(session_id=session_id, phone=phone, command="2"))

    assert window['name'] == 'PORTUGUESE'

def test_must_return_english_menu():
    app = create_lottus_app()

    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(create_request(session_id=session_id, phone=phone, command=8745))

    assert window['name'] == 'INITIAL'

    window = app.process_request(create_request(session_id=session_id, phone=phone, command="1"))

    assert window['name'] == 'ENGLISH'

def test_must_return_initial_menu():
    app = create_lottus_app()
    
    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(create_request(session_id=session_id, phone=phone, command=8745))

    assert window['name'] == 'INITIAL'

def test_must_return_error_menu():
    app = create_lottus_app()
    
    session_id = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(create_request(session_id=session_id, phone=phone, command=8745))

    assert window['name'] == 'INITIAL'

    window = app.process_request(create_request(session_id=session_id, phone=phone, command="3"))

    assert window['name'] == 'INITIAL'