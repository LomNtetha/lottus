from lottus import *
import random
import pytest

windows = {
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
        "type": "FORM"
    }
}

def create_lottus_app():
    class InMemoryWindowCache(WindowCache):
        def __init__(self):
            self.windows = {}

        def get(self, window_name, session_id=None):
            return self.windows[window_name] if window_name in self.windows else None

        def cache(self, window, session_id=None):
            self.windows[window[Constants.NAME.value]] = window

    class InMemorySessionManager(SessionManager):
        def __init__(self):
            self._sessions = []

        def get(self, session_id, phone):
            return next((s for s in self._sessions if s[Constants.SESSION.value] == session_id and s[Constants.PHONE.value] == phone), None)

        def save(self, session):
            self._sessions.append(session)

    lottus_app = Lottus('INITIAL', windows, InMemorySessionManager(), InMemoryWindowCache())

    @lottus_app.window('INITIAL')
    def initial_window(session, request):
        options = [create_option("1", "English", "ENGLISH"), create_option("2", "Portuguese", "PORTUGUESE")]
        window = create_window("INITIAL", "Ben Chambule's CV", "Select one of following options", options)

        return window, session
    
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

def test_must_return_portuguese_window():
    app = create_lottus_app()

    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))
    window = app.process_request(create_request(session_id=sessio_nr, phone=phone, command="2"))

    assert window[Constants.NAME.value] == 'PORTUGUESE'

def test_must_return_english_window():
    app = create_lottus_app()

    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))
    window = app.process_request(create_request(session_id=sessio_nr, phone=phone, command="1"))

    assert window[Constants.NAME.value] == 'ENGLISH'

def test_must_return_initial_window():
    app = create_lottus_app()
    
    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))

    assert window[Constants.NAME.value] == 'INITIAL'

def test_must_return_error_window():
    app = create_lottus_app()
    
    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    window = app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))

    assert window[Constants.NAME.value] == 'INITIAL'

    window = app.process_request(create_request(session_id=sessio_nr, phone=phone, command="3"))

    assert window[Constants.NAME.value] == 'INITIAL'

def test_cache_must_not_be_empty():
    app = create_lottus_app()
    
    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))
    app.process_request(create_request(session_id=sessio_nr, phone=phone, command="3"))

    cache = app.window_cache

    assert cache.windows != {}

def test_cache_must_have_initial_window():
    app = create_lottus_app()
    
    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))
    app.process_request(create_request(session_id=sessio_nr, phone=phone, command="3"))
    
    cache = app.window_cache

    assert cache.windows.get('INITIAL') != None

def test_cache_must_have_portuguese_window():
    app = create_lottus_app()
    
    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))
    app.process_request(create_request(session_id=sessio_nr, phone=phone, command="2"))

    cache = app.window_cache

    assert cache.windows.get('PORTUGUESE') != None

def test_cache_has_not_portuguese_menu():
    app = create_lottus_app()
    
    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))
    app.process_request(create_request(session_id=sessio_nr, phone=phone, command="1"))

    cache = app.window_cache

    with pytest.raises(KeyError):
        cache.windows['PORTUGUESE']


if __name__ == '__main__':
    app = create_lottus_app()
    
    sessio_nr = random.randint(1000000, 9999999)
    phone = '258842217064'

    app.process_request(create_request(session_id=sessio_nr, phone=phone, command=8745))
    app.process_request(create_request(session_id=sessio_nr, phone=phone, command="1"))

    cache = app.window_cache
    print(cache.windows['PORTUGUESE'])