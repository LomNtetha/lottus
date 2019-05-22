Lottus
==========================

An USSD library that will save you time. Ever wondered if you could quickly write and/or prototype an ussd application? 

Installation
------------
``` {.sourceCode .bash}
pipenv install git+https://github.com/benchambule/lottus.git@master#egg=lottus
```

After installation

``` {.sourceCode .python}
#file appy.py
#flask is used to serve our ussd app over http
from flask import Flask, request, json, Response

import lottus.core
import os
import lottus.helpers

# create our menus
menus = {
    "INITIAL": {
      "name": "INITIAL",
      "title": "Ben Chambule's USSD - CV",
      "message": "Please select your languange of choice",
      "options": [
        {"option": "1", "display": "English", "menu": "ENGLISH", "active": true},
        {"option": "2", "display": "Portuguese", "menu": "PORTUGUESE", "active": true}
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "ENGLISH": {
      "name": "ENGLISH",
      "title": "ENGLISH Menu",
      "message": "Please select one of the options",
      "options": [
        {"option": "1", "display": "Basic information", "menu": "BASIC_INFO_EN", "active": true},
        {"option": "2", "display": "Skills", "menu": "SKILLS_EN", "active": true},
        {"option": "3", "display": "Contact", "menu": "CONTACT_EN", "active": true},
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "PORTUGUESE": {
      "name": "PORTUGUESE",
      "title": "Menu em Portuges",
      "message": "Por favor seleccione uma das opcoes",
      "options": [
        {"option": "1", "display": "Dados pessoais", "menu": "BASIC_INFO_PT", "active": true},
        {"option": "2", "display": "Habilidades", "menu": "SKILLS_PT", "active": true},
        {"option": "3", "display": "Contacto", "menu": "CONTACT_PT", "active": true},
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "BASIC_INFO_EN": {
      "name": "BASIC_INFO_EN",
      "title": "Basic information",
      "message": "Name: Benjamim Chambule\nProfession: Software Developer",
      "options": [
        {"option": "0", "display": "Back", "menu": "ENGLISH", "active": true}
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "BASIC_INFO_PT": {
      "name": "BASIC_INFO_PT",
      "title": "Informacao Basica",
      "message": "Nome: Benjamim Chambule\nProfissao: Desenvolvedor de Software",
      "options": [
        {"option": "0", "display": "Voltar", "menu": "ENGLISH", "active": true}
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "SKILLS_EN": {
      "name": "SKILLS_EN",
      "title": "Skills",
      "message": "Name: Benjamim Chambule\nProfession: Software Developer",
      "options": [
        {"option": "0", "display": "Back", "menu": "ENGLISH", "active": true}
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "SKILLS_PT": {
      "name": "SKILLS_PT",
      "title": "Habilidades",
      "message": "Nome: Benjamim Chambule\nProfissao: Desenvolvedor de Software",
      "options": [
        {"option": "0", "display": "Voltar", "menu": "PORTUGUESE", "active": true}
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "CONTACT_EN": {
      "name": "CONTACT_EN",
      "title": "Contact",
      "message": "Email: benchambule@gmail.com\nTelegram: http://t.me/benchambule\nGitHub: http://github.com/benchambule",
      "options": [
        {"option": "0", "display": "Back", "menu": "ENGLISH", "active": true}
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    },
  
    "CONTACT_PT": {
      "name": "CONTACT_PT",
      "title": "Contacto",
      "message": "Email: benchambule@gmail.com\nTelegram: http://t.me/benchambule\nGitHub: http://github.com/benchambule",
      "options": [
        {"option": "0", "display": "Back", "menu": "PORTUGUESE", "active": true}
      ],
      "type": "FORM",
      "auto_process": true,
      "active": true
    }
  }


def get_lottus_app():
    lottus_app = lottus.core.Lottus(__name__, 'INITIAL', menus, InMemoryUSSDSessionBag())

    return lottus_app


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


app = Flask(__name__)

lottus_app = get_lottus_app()

@app.route('/ussdapp/json/', methods=['POST'])
def ussd_json_api():
    js = json.dumps(request.json)
    req_dict = json.loads(js)

    resp = lottus_app.handle_request(req_dict)

    return Response(json.dumps(resp), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run()
```

Run your application
--------------------

``` {.sourceCode .bash}
python app.py
```

Testing
------------------------

Any one can test it on Postman or curl or httpie (my favorite)

``` {.sourceCode .bash}
echo {"session": 1234, "cell_number": "+258842271064", "request_str": "4"} | http http://localhost:5000/ussdapp/json/
```