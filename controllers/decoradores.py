from functools import wraps
from flask import redirect, url_for, flash
from flask_login import login_required, current_user


def admin_requerido(vista):
    @wraps(vista)
    @login_required
    def envoltura(*args, **kwargs):
        if not current_user.es_admin:
            flash("Solo el administrador puede entrar a esa sección", "error")
            return redirect(url_for("auth.inicio"))
        return vista(*args, **kwargs)
    return envoltura
