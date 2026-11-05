from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.usuario import Usuario
from models.ciudad import Ciudad
from models.zona import Zona
from services.validaciones import validar_deportista

auth_bp = Blueprint("auth", __name__)


def destino_segun_rol(usuario):
    return url_for("usuarios.listar") if usuario.es_admin else url_for("auth.inicio")


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(destino_segun_rol(current_user))

    if request.method == "POST":
        nombre = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        usuario = Usuario.query.filter_by(usuario=nombre).first()

        if usuario and usuario.verificar_contrasena(contrasena):
            login_user(usuario)
            return redirect(destino_segun_rol(usuario))

        flash("Usuario o contraseña incorrectos", "error")

    return render_template("index.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    datos = request.form if request.method == "POST" else {}

    if request.method == "POST":
        errores, limpios = validar_deportista(request.form)
        if errores:
            for e in errores:
                flash(e, "error")
        else:
            nuevo = Usuario(usuario=limpios["usuario"], cedula=limpios["cedula"],
                            telefono=limpios["telefono"], zona_id=limpios["zona_id"])
            nuevo.set_contrasena(limpios["contrasena"])
            db.session.add(nuevo)
            db.session.commit()
            flash("Cuenta creada. Ya puedes iniciar sesión", "ok")
            return redirect(url_for("auth.login"))

    ciudad_id = request.form.get("ciudad_id", type=int)
    zonas = Zona.query.filter_by(ciudad_id=ciudad_id).order_by(Zona.nombre).all() if ciudad_id else []
    return render_template("registro.html", datos=datos,
                           ciudades=Ciudad.query.order_by(Ciudad.nombre).all(), zonas=zonas)


@auth_bp.route("/inicio")
@login_required
def inicio():
    return render_template("inicio.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "ok")
    return redirect(url_for("auth.login"))
