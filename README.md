Lottus
==========================

An USSD library that will save you time. Ever wondered if you could quickly write and/or prototype an ussd application? 

Installation
------------
``` {.sourceCode .bash}
pipenv install -e git+https://github.com/benchambule/lottus.git@master#egg=lottus
```

After installation

``` {.sourceCode .python}
#file appy.py
#flask is used to serve our ussd app over http
from flask import Flask, request, json, Response

from lottus import *
import random

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
        "type": "FORM",
        "active": True
    }
}

def create_lottus_app():
    class Cacheablility(WindowCache):
        def __init__(self):
            self._windows = {}

        def get(self, window, session_id=None):
            return self._windows[window] if window in self._windows else None

        def cache(self, window, session_id=None):
            self._windows[window['name']] = window

    class InMemorySessionContext(SessionManager):
        def __init__(self):
            self._sessions = []

        def get(self, session_id, phone):
            return next((s for s in self._sessions if s['number'] == session_id and s['cell'] == phone), None)

        def save(self, session):
            self._sessions.append(session)

        def create(self, session_id, phone):
            return {'number': session_id, 'cell': phone}

    lottus_app = Lottus('INITIAL', windows, InMemorySessionContext(), Cacheablility())

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

app = Flask(__name__)

lottus_app = create_lottus_app()

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

Anyone can test it on Postman or curl or httpie (my favorite)

``` {.sourceCode .bash}
echo '{"session": 1234, "phone": "+258840000000", "command": "0"}' | http http://localhost:5000/ussdapp/json/
```
