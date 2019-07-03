import lottus.core

class InMemoryUSSDSessionBag(lottus.core.USSDSessionBag):
    def __init__(self):
        self.__sessions = []

    def get_session(self, msisdn, session):
        return next((s for s in self.__sessions if s['session'] == session), None)

    def update_session(self, session):
        pass

    def save_session(self, session):
        pass

    def add_session(self, session):
        self.__sessions.append(session)

def create_lottus_request(session, cell_number, request_str):
    return {'cell_number': cell_number, 'session': session, 'request_str': request_str}

def get_menus():
    return {
        "INITIAL": {
            "name": "INITIAL",
            "title": "Ben Chambule's USSD - CV",
            "message": "Please select your languange of choice",
            "options": [
                {"option": "1", "display": "English", "menu": "ENGLISH", "active": True},
                {"option": "2", "display": "Portuguese", "menu": "PORTUGUESE", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },
        "ENGLISH": {
            "name": "ENGLISH",
            "title": "ENGLISH Menu",
            "message": "Please select one of the options",
            "options": [
                {"option": "1", "display": "Basic information", "menu": "BASIC_INFO_EN", "active": True},
                {"option": "2", "display": "Skills", "menu": "SKILLS_EN", "active": True},
                {"option": "3", "display": "Contact", "menu": "CONTACT_EN", "active": True},
                {"option": "4", "display": "Academic Formation", "menu": "ACADEMIC_EN", "active": True},
                {"option": "5", "display": "Change language", "menu": "INITIAL", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "PORTUGUESE": {
            "name": "PORTUGUESE",
            "title": "Menu em Portuges",
            "message": "Por favor seleccione uma das opcoes",
            "options": [
                {"option": "1", "display": "Dados pessoais", "menu": "BASIC_INFO_PT", "active": True},
                {"option": "2", "display": "Habilidades", "menu": "SKILLS_PT", "active": True},
                {"option": "3", "display": "Contacto", "menu": "CONTACT_PT", "active": True},
                {"option": "4", "display": "Formacao Academica", "menu": "ACADEMIC_PT", "active": True},
                {"option": "5", "display": "Mudar idioma", "menu": "INITIAL", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "BASIC_INFO_EN": {
            "name": "BASIC_INFO_EN",
            "title": "Basic information",
            "message": "Name: Benjamim Chambule\nProfession: Software Developer",
            "options": [
                {"option": "0", "display": "Back", "menu": "ENGLISH", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "BASIC_INFO_PT": {
            "name": "BASIC_INFO_PT",
            "title": "Informacao Basica",
            "message": "Nome: Benjamim Chambule\nProfissao: Desenvolvedor de Software",
            "options": [
                {"option": "0", "display": "Voltar", "menu": "ENGLISH", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "SKILLS_EN": {
            "name": "SKILLS_EN",
            "title": "Skills",
            "message": "Name: Benjamim Chambule\nProfession: Software Developer",
            "options": [
                {"option": "0", "display": "Back", "menu": "ENGLISH", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "SKILLS_PT": {
            "name": "SKILLS_PT",
            "title": "Habilidades",
            "message": "Nome: Benjamim Chambule\nProfissao: Desenvolvedor de Software",
            "options": [
                {"option": "0", "display": "Voltar", "menu": "PORTUGUESE", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "CONTACT_EN": {
            "name": "CONTACT_EN",
            "title": "Contact",
            "message": "Email: benchambule@gmail.com\nTelegram: http://t.me/benchambule\nGitHub: http://github.com/benchambule",
            "options": [
                {"option": "0", "display": "Back", "menu": "ENGLISH", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "CONTACT_PT": {
            "name": "CONTACT_PT",
            "title": "Contacto",
            "message": "Email: benchambule@gmail.com\nTelegram: http://t.me/benchambule\nGitHub: http://github.com/benchambule",
            "options": [
                {"option": "0", "display": "Back", "menu": "PORTUGUESE", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "ACADEMIC_EN": {
            "name": "ACADEMIC_EN",
            "title": "Academic Formation",
            "message": "Name: Benjamim Chambule\nProfession: Software Developer",
            "options": [
                {"option": "0", "display": "Back", "menu": "ENGLISH", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
        },

        "ACADEMIC_PT": {
            "name": "ACADEMIC_PT",
            "title": "Formacao academica",
            "message": "Nome: Benjamim Chambule\nProfissao: Desenvolvedor de Software",
            "options": [
                {"option": "0", "display": "Voltar", "menu": "PORTUGUESE", "active": True}
            ],
            "type": "FORM",
            "auto_process": True,
            "active": True
            }
        }

def get_lottus_app():
    menus = get_menus()

    return lottus.core.Lottus(__name__, 'INITIAL', menus, InMemoryUSSDSessionBag())
    
def test_menu_title_must_be_initial_menu():
    lottus_app = get_lottus_app()
    resp = lottus_app.handle_request(create_lottus_request('riuytiu', '+258842217064', '*123#'))
    assert resp['name'] == 'INITIAL'


def test_menu_title_must_select_english_menu():
    lottus_app = get_lottus_app()
    lottus_app.handle_request(create_lottus_request('riuytiu', '+258842217064', '*123#'))
    resp = lottus_app.handle_request(create_lottus_request('riuytiu', '+258842217064', '1'))
    assert resp['name'] == 'ENGLISH'

def test_menu_title_must_be_academic_info_pt():
    lottus_app = get_lottus_app()
    lottus_app.handle_request(create_lottus_request('riuytiu', '+258842217064', '*123#'))
    lottus_app.handle_request(create_lottus_request('riuytiu', '+258842217064', '2'))
    resp = lottus_app.handle_request(create_lottus_request('riuytiu', '+258842217064', '4'))
    assert resp['name'] == 'ACADEMIC_PT'


if __name__ == "__main__":
    pass