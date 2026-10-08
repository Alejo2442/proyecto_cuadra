from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("usuarios.listar"))

    if request.method == "POST":
        nombre = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        usuario = Usuario.query.filter_by(usuario=nombre).first()

        if usuario and usuario.verificar_contrasena(contrasena):
            login_user(usuario)
            return redirect(url_for("usuarios.listar"))

        flash("Usuario o contraseña incorrectos", "danger")

    return render_template("index.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not nombre or not contrasena:
            flash("Completa todos los campos", "danger")
        elif Usuario.query.filter_by(usuario=nombre).first():
            flash("Ese usuario ya existe", "danger")
        else:
            nuevo = Usuario(usuario=nombre)
            nuevo.set_contrasena(contrasena)
            db.session.add(nuevo)
            db.session.commit()
            flash("Cuenta creada. Ya puedes iniciar sesión", "success")
            return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "success")
    return redirect(url_for("auth.login"))