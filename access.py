from flask import *
from functools import wraps


def login_required(func):#проверка на наличие акка
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return render_template('access_refused_login.html')
    return wrapper

def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint
    print('endpoint_func=', endpoint_func)
    endpoint_app = request.endpoint.split('.')[0]
    print('endpoint_app=', endpoint_app)
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            return True
        elif user_group in config and endpoint_func in config[user_group]:
            return True
    return False

def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config) or external_validation(config):
            return f(*args, **kwargs)
        return render_template('access_refused.html')
    return wrapper

def external_validation(config:dict)-> bool:
    endpoint_app = request.endpoint.split('.')[0]
    endpoint_func = request.endpoint
    user_group = session.get('user_group', None)
    if user_group is None:
        if endpoint_app in config['external']:
            return True
        if endpoint_func in config['external']:
            return True
    return False
