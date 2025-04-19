from functools import wraps
from flask import session, redirect, url_for

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('raiz'))  # nombre de la ruta del login
        return f(*args, **kwargs)
    return decorada
