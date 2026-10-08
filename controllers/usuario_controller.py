from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.usuario import Usuario

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


# LEER
@usuarios_bp.route("/")
@login_required
def listar():
    usuarios = Usuario.query.order_by(Usuario.id).all()
    return render_template("usuarios/lista.html", usuarios=usuarios)


# CREAR
@usuarios_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear():
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
            flash("Usuario creado correctamente", "success")
            return redirect(url_for("usuarios.listar"))

    return render_template("usuarios/formulario.html", usuario=None)


# ACTUALIZAR
@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    usuario = db.get_or_404(Usuario, id)

    if request.method == "POST":
        nombre = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "")
        existente = Usuario.query.filter_by(usuario=nombre).first()

        if not nombre:
            flash("El usuario no puede estar vacío", "danger")
        elif existente and existente.id != usuario.id:
            flash("Ese usuario ya existe", "danger")
        else:
            usuario.usuario = nombre
            if contrasena:
                usuario.set_contrasena(contrasena)
            db.session.commit()
            flash("Usuario actualizado correctamente", "success")
            return redirect(url_for("usuarios.listar"))

    return render_template("usuarios/formulario.html", usuario=usuario)


# ELIMINAR
@usuarios_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar(id):
    usuario = db.get_or_404(Usuario, id)

    if usuario.id == current_user.id:
        flash("No puedes eliminar tu propia cuenta", "warning")
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuario eliminado correctamente", "success")

    return redirect(url_for("usuarios.listar"))