from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.usuario import Usuario
from models.ciudad import Ciudad
from models.zona import Zona
from services.validaciones import validar_deportista
from controllers.decoradores import admin_requerido

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


def mostrar_formulario(deportista, datos):
    ciudad_id = datos.get("ciudad_id")
    zonas = Zona.query.filter_by(ciudad_id=int(ciudad_id)).order_by(Zona.nombre).all() if ciudad_id else []
    return render_template("usuarios/formulario.html", deportista=deportista, datos=datos,
                           ciudades=Ciudad.query.order_by(Ciudad.nombre).all(), zonas=zonas)


@usuarios_bp.route("/")
@admin_requerido
def listar():
    deportistas = Usuario.query.filter_by(es_admin=False).order_by(Usuario.id).all()
    return render_template("usuarios/lista.html", deportistas=deportistas)


@usuarios_bp.route("/crear", methods=["GET", "POST"])
@admin_requerido
def crear():
    if request.method == "POST":
        errores, limpios = validar_deportista(request.form)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(None, request.form)

        nuevo = Usuario(usuario=limpios["usuario"], cedula=limpios["cedula"],
                        telefono=limpios["telefono"], zona_id=limpios["zona_id"])
        nuevo.set_contrasena(limpios["contrasena"])
        db.session.add(nuevo)
        db.session.commit()
        flash("Deportista creado correctamente", "ok")
        return redirect(url_for("usuarios.listar"))

    return mostrar_formulario(None, {})


@usuarios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_requerido
def editar(id):
    deportista = db.get_or_404(Usuario, id)
    if deportista.es_admin:
        flash("La cuenta del administrador no se edita desde aquí", "error")
        return redirect(url_for("usuarios.listar"))

    if request.method == "POST":
        errores, limpios = validar_deportista(request.form, deportista)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(deportista, request.form)

        deportista.usuario = limpios["usuario"]
        deportista.cedula = limpios["cedula"]
        deportista.telefono = limpios["telefono"]
        deportista.zona_id = limpios["zona_id"]
        if limpios["contrasena"]:
            deportista.set_contrasena(limpios["contrasena"])
        db.session.commit()
        flash("Deportista actualizado correctamente", "ok")
        return redirect(url_for("usuarios.listar"))

    datos = {
        "usuario": deportista.usuario,
        "cedula": deportista.cedula or "",
        "telefono": deportista.telefono or "",
        "ciudad_id": deportista.zona.ciudad_id if deportista.zona else "",
        "zona_id": deportista.zona_id or "",
    }
    return mostrar_formulario(deportista, datos)


@usuarios_bp.route("/eliminar/<int:id>", methods=["POST"])
@admin_requerido
def eliminar(id):
    deportista = db.get_or_404(Usuario, id)
    if deportista.es_admin:
        flash("La cuenta del administrador no se puede eliminar", "error")
    else:
        db.session.delete(deportista)
        db.session.commit()
        flash("Deportista eliminado correctamente", "ok")
    return redirect(url_for("usuarios.listar"))
