from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.usuario import Usuario
from models.deporte import Deporte
from models.nivel import Nivel
from models.perfil_deportivo import PerfilDeportivo
from controllers.decoradores import admin_requerido

perfiles_bp = Blueprint("perfiles", __name__, url_prefix="/perfiles")


def validar_perfil(form, perfil=None):
    errores = []
    usuario = db.session.get(Usuario, form.get("usuario_id", type=int) or 0)
    deporte = db.session.get(Deporte, form.get("deporte_id", type=int) or 0)
    nivel = db.session.get(Nivel, form.get("nivel_id", type=int) or 0)
    posicion = form.get("posicion", "").strip() or None
    peso_texto = form.get("peso", "").strip().replace(",", ".")
    peso = None

    if usuario is None or usuario.es_admin:
        errores.append("Elige un deportista")
    if deporte is None:
        errores.append("Elige un deporte")
    if nivel is None:
        errores.append("Elige un nivel")
    elif deporte is not None and nivel.deporte_id != deporte.id:
        errores.append("Ese nivel no pertenece al deporte elegido")

    if usuario and deporte:
        repetido = PerfilDeportivo.query.filter_by(usuario_id=usuario.id, deporte_id=deporte.id).first()
        if repetido and repetido is not perfil:
            errores.append("Ese deportista ya tiene un perfil de " + deporte.nombre)

    if peso_texto:
        try:
            peso = float(peso_texto)
            if not 30 <= peso <= 200:
                errores.append("El peso debe estar entre 30 y 200 kg")
        except ValueError:
            errores.append("El peso debe ser un número")

    datos = {"usuario": usuario, "deporte": deporte, "nivel": nivel, "posicion": posicion, "peso": peso}
    return errores, datos


def mostrar_formulario(perfil, datos):
    deporte_id = datos.get("deporte_id")
    niveles = Nivel.query.filter_by(deporte_id=int(deporte_id)).order_by(Nivel.orden).all() if deporte_id else []
    return render_template("perfiles/formulario.html", perfil=perfil, datos=datos,
                           deportistas=Usuario.query.filter_by(es_admin=False).order_by(Usuario.usuario).all(),
                           deportes=Deporte.query.order_by(Deporte.nombre).all(), niveles=niveles)


@perfiles_bp.route("/")
@admin_requerido
def listar():
    perfiles = PerfilDeportivo.query.order_by(PerfilDeportivo.id).all()
    return render_template("perfiles/lista.html", perfiles=perfiles)


@perfiles_bp.route("/crear", methods=["GET", "POST"])
@admin_requerido
def crear():
    if request.method == "POST":
        errores, d = validar_perfil(request.form)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(None, request.form)
        db.session.add(PerfilDeportivo(usuario=d["usuario"], deporte=d["deporte"], nivel=d["nivel"],
                                       posicion=d["posicion"], peso=d["peso"]))
        db.session.commit()
        flash("Perfil deportivo creado correctamente", "ok")
        return redirect(url_for("perfiles.listar"))
    return mostrar_formulario(None, {})


@perfiles_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@admin_requerido
def editar(id):
    perfil = db.get_or_404(PerfilDeportivo, id)
    if request.method == "POST":
        errores, d = validar_perfil(request.form, perfil)
        if errores:
            for e in errores:
                flash(e, "error")
            return mostrar_formulario(perfil, request.form)
        perfil.usuario, perfil.deporte, perfil.nivel = d["usuario"], d["deporte"], d["nivel"]
        perfil.posicion, perfil.peso = d["posicion"], d["peso"]
        db.session.commit()
        flash("Perfil deportivo actualizado correctamente", "ok")
        return redirect(url_for("perfiles.listar"))

    datos = {"usuario_id": perfil.usuario_id, "deporte_id": perfil.deporte_id, "nivel_id": perfil.nivel_id,
             "posicion": perfil.posicion or "", "peso": perfil.peso or ""}
    return mostrar_formulario(perfil, datos)


@perfiles_bp.route("/eliminar/<int:id>", methods=["POST"])
@admin_requerido
def eliminar(id):
    db.session.delete(db.get_or_404(PerfilDeportivo, id))
    db.session.commit()
    flash("Perfil deportivo eliminado correctamente", "ok")
    return redirect(url_for("perfiles.listar"))
