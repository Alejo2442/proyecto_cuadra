from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.ciudad import Ciudad
from models.zona import Zona
from models.usuario import Usuario
from controllers.decoradores import admin_requerido

zonas_bp = Blueprint("zonas", __name__, url_prefix="/zonas")


def validar(form, zona=None):
    errores = []
    ciudad = db.session.get(Ciudad, form.get("ciudad_id", type=int) or 0)
    nombre = form.get("nombre", "").strip()

    if ciudad is None:
        errores.append("Elige una ciudad")
    if not nombre:
        errores.append("El nombre es obligatorio")
    if ciudad and nombre:
        repetida = Zona.query.filter_by(ciudad_id=ciudad.id, nombre=nombre).first()
        if repetida and repetida is not zona:
            errores.append("Esa zona ya existe en " + ciudad.nombre)
    return errores, ciudad, nombre


def mostrar_formulario(zona, datos):
    return render_template("zonas/formulario.html", zona=zona, datos=datos,
                           ciudades=Ciudad.query.order_by(Ciudad.nombre).all())


@zonas_bp.route("/")
@admin_requerido
def listar():
    zonas = Zona.query.join(Ciudad).order_by(Ciudad.nombre, Zona.nombre).all()
    return render_template("zonas/lista.html", zonas=zonas)


@zonas_bp.route("/crear", methods=["GET", "POST"])
@admin_requerido
def crear():
    if request.method == "POST":
        errores, ciudad, nombre = validar(request.form)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(None, request.form)
        db.session.add(Zona(ciudad=ciudad, nombre=nombre))
        db.session.commit()
        flash("Zona creada correctamente", "ok")
        return redirect(url_for("zonas.listar"))
    return mostrar_formulario(None, {})


@zonas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_requerido
def editar(id):
    zona = db.get_or_404(Zona, id)
    if request.method == "POST":
        errores, ciudad, nombre = validar(request.form, zona)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(zona, request.form)
        zona.ciudad, zona.nombre = ciudad, nombre
        db.session.commit()
        flash("Zona actualizada correctamente", "ok")
        return redirect(url_for("zonas.listar"))
    return mostrar_formulario(zona, {"ciudad_id": zona.ciudad_id, "nombre": zona.nombre})


@zonas_bp.route("/eliminar/<int:id>", methods=["POST"])
@admin_requerido
def eliminar(id):
    zona = db.get_or_404(Zona, id)
    if Usuario.query.filter_by(zona_id=id).first():
        flash("No se puede eliminar: hay deportistas en esa zona", "error")
    else:
        db.session.delete(zona)
        db.session.commit()
        flash("Zona eliminada correctamente", "ok")
    return redirect(url_for("zonas.listar"))
