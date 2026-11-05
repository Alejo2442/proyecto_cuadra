from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.ciudad import Ciudad
from controllers.decoradores import admin_requerido

ciudades_bp = Blueprint("ciudades", __name__, url_prefix="/ciudades")


def validar(nombre, ciudad=None):
    if not nombre:
        return "El nombre es obligatorio"
    existente = Ciudad.query.filter(db.func.lower(Ciudad.nombre) == nombre.lower()).first()
    if existente and existente is not ciudad:
        return "Esa ciudad ya existe"
    return None


@ciudades_bp.route("/")
@admin_requerido
def listar():
    return render_template("ciudades/lista.html", ciudades=Ciudad.query.order_by(Ciudad.nombre).all())


@ciudades_bp.route("/crear", methods=["GET", "POST"])
@admin_requerido
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        error = validar(nombre)
        if error:
            flash(error, "error")
        else:
            db.session.add(Ciudad(nombre=nombre))
            db.session.commit()
            flash("Ciudad creada correctamente", "ok")
            return redirect(url_for("ciudades.listar"))
    return render_template("ciudades/formulario.html", ciudad=None, nombre=request.form.get("nombre", ""))


@ciudades_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_requerido
def editar(id):
    ciudad = db.get_or_404(Ciudad, id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        error = validar(nombre, ciudad)
        if error:
            flash(error, "error")
        else:
            ciudad.nombre = nombre
            db.session.commit()
            flash("Ciudad actualizada correctamente", "ok")
            return redirect(url_for("ciudades.listar"))
    return render_template("ciudades/formulario.html", ciudad=ciudad,
                           nombre=request.form.get("nombre", ciudad.nombre))


@ciudades_bp.route("/eliminar/<int:id>", methods=["POST"])
@admin_requerido
def eliminar(id):
    ciudad = db.get_or_404(Ciudad, id)
    if ciudad.zonas:
        flash("No se puede eliminar: la ciudad tiene zonas asociadas", "error")
    else:
        db.session.delete(ciudad)
        db.session.commit()
        flash("Ciudad eliminada correctamente", "ok")
    return redirect(url_for("ciudades.listar"))
