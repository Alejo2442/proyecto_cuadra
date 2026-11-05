from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.deporte import Deporte
from models.nivel import Nivel
from models.perfil_deportivo import PerfilDeportivo
from controllers.decoradores import admin_requerido

niveles_bp = Blueprint("niveles", __name__, url_prefix="/niveles")


def validar(form, nivel=None):
    errores = []
    deporte = db.session.get(Deporte, form.get("deporte_id", type=int) or 0)
    nombre = form.get("nombre", "").strip()
    orden = form.get("orden", type=int)

    if deporte is None:
        errores.append("Elige un deporte")
    if not nombre:
        errores.append("El nombre es obligatorio")
    if orden is None or orden < 1:
        errores.append("El orden debe ser un número entero desde 1")
    if deporte and nombre:
        repetido = Nivel.query.filter_by(deporte_id=deporte.id, nombre=nombre).first()
        if repetido and repetido is not nivel:
            errores.append("Ese nivel ya existe en " + deporte.nombre)
    if deporte and orden:
        mismo_orden = Nivel.query.filter_by(deporte_id=deporte.id, orden=orden).first()
        if mismo_orden and mismo_orden is not nivel:
            errores.append("Ya hay un nivel con el orden " + str(orden) + " en " + deporte.nombre)
    return errores, deporte, nombre, orden


def mostrar_formulario(nivel, datos):
    return render_template("niveles/formulario.html", nivel=nivel, datos=datos,
                           deportes=Deporte.query.order_by(Deporte.nombre).all())


@niveles_bp.route("/")
@admin_requerido
def listar():
    niveles = Nivel.query.join(Deporte).order_by(Deporte.nombre, Nivel.orden).all()
    return render_template("niveles/lista.html", niveles=niveles)


@niveles_bp.route("/crear", methods=["GET", "POST"])
@admin_requerido
def crear():
    if request.method == "POST":
        errores, deporte, nombre, orden = validar(request.form)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(None, request.form)
        db.session.add(Nivel(deporte=deporte, nombre=nombre, orden=orden))
        db.session.commit()
        flash("Nivel creado correctamente", "ok")
        return redirect(url_for("niveles.listar"))
    return mostrar_formulario(None, {})


@niveles_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_requerido
def editar(id):
    nivel = db.get_or_404(Nivel, id)
    if request.method == "POST":
        errores, deporte, nombre, orden = validar(request.form, nivel)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(nivel, request.form)
        nivel.deporte, nivel.nombre, nivel.orden = deporte, nombre, orden
        db.session.commit()
        flash("Nivel actualizado correctamente", "ok")
        return redirect(url_for("niveles.listar"))
    return mostrar_formulario(nivel, {"deporte_id": nivel.deporte_id, "nombre": nivel.nombre, "orden": nivel.orden})


@niveles_bp.route("/eliminar/<int:id>", methods=["POST"])
@admin_requerido
def eliminar(id):
    nivel = db.get_or_404(Nivel, id)
    if PerfilDeportivo.query.filter_by(nivel_id=id).first():
        flash("No se puede eliminar: hay perfiles deportivos con ese nivel", "error")
    else:
        db.session.delete(nivel)
        db.session.commit()
        flash("Nivel eliminado correctamente", "ok")
    return redirect(url_for("niveles.listar"))
