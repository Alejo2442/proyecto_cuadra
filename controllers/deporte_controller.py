from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.deporte import Deporte
from models.perfil_deportivo import PerfilDeportivo
from controllers.decoradores import admin_requerido

deportes_bp = Blueprint("deportes", __name__, url_prefix="/deportes")


def validar(nombre, deporte=None):
    if not nombre:
        return "El nombre es obligatorio"
    existente = Deporte.query.filter(db.func.lower(Deporte.nombre) == nombre.lower()).first()
    if existente and existente is not deporte:
        return "Ese deporte ya existe"
    return None


@deportes_bp.route("/")
@admin_requerido
def listar():
    return render_template("deportes/lista.html", deportes=Deporte.query.order_by(Deporte.nombre).all())


@deportes_bp.route("/crear", methods=["GET", "POST"])
@admin_requerido
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        error = validar(nombre)
        if error:
            flash(error, "error")
        else:
            db.session.add(Deporte(nombre=nombre))
            db.session.commit()
            flash("Deporte creado correctamente", "ok")
            return redirect(url_for("deportes.listar"))
    return render_template("deportes/formulario.html", deporte=None, nombre=request.form.get("nombre", ""))


@deportes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_requerido
def editar(id):
    deporte = db.get_or_404(Deporte, id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        error = validar(nombre, deporte)
        if error:
            flash(error, "error")
        else:
            deporte.nombre = nombre
            db.session.commit()
            flash("Deporte actualizado correctamente", "ok")
            return redirect(url_for("deportes.listar"))
    return render_template("deportes/formulario.html", deporte=deporte,
                           nombre=request.form.get("nombre", deporte.nombre))


@deportes_bp.route("/eliminar/<int:id>", methods=["POST"])
@admin_requerido
def eliminar(id):
    deporte = db.get_or_404(Deporte, id)
    if deporte.niveles or PerfilDeportivo.query.filter_by(deporte_id=id).first():
        flash("No se puede eliminar: el deporte tiene niveles o perfiles asociados", "error")
    else:
        db.session.delete(deporte)
        db.session.commit()
        flash("Deporte eliminado correctamente", "ok")
    return redirect(url_for("deportes.listar"))
