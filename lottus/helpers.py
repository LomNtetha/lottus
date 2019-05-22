def is_menu_a_form(menu):
    return menu['type'] == 'FORM'

def is_active_menu(menu):
    return menu['active']

def do_non_auto_process_menu(menu, processor, session, request):
    return processor(menu, session, request)

def is_auto_processable_menu(menu):
    return menu['auto_process']

def menu_add_parameters(menu, session):
    for parameter in session['parameters']:
        if parameter in menu['message']:
            menu['message'] = menu['message'].replace(parameter, session['parameters'][parameter])

    return menu

def get_option(option_name, options):
    return next((s for s in options if s['option'] == option_name), None)

def request_matches_options(request, options):
        option = options.get(request, None)
        return False if not option else True

def generate_menu(menu_name, title, with_message):
    return {
        "name": menu_name,
        "message": with_message,
        "title": title,
        "options": [],
        "type": "FORM",
        "auto_process": False,
        "active": True,
    }

def beautify_menu(menu):
    return {
        'title': menu['title'],
        'message': menu['message'],
        'options': [beautify_option(x) for x in menu['options']],
        'type': menu['type']
    }

def beautify_option(option):
    return f"{option['option']} - {option['display']}"