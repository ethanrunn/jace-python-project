from flask import session, redirect, url_for
from functools import wraps

def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not "ADMIN_EMAIL" in session:
            return redirect(url_for('admin.admin_login'))
        return func(*args, **kwargs)
    return wrapper

