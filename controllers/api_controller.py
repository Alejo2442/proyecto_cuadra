from flask import Blueprint, jsonify
from models.zona import Zona
from models.nivel import Nivel

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/ciudades/<int:id>/zonas")
def zonas_de_ciudad(id):
    zonas = Zona.query.filter_by(ciudad_id=id).order_by(Zona.nombre).all()
    return jsonify([{"id": z.id, "nombre": z.nombre} for z in zonas])


@api_bp.route("/deportes/<int:id>/niveles")
def niveles_de_deporte(id):
    niveles = Nivel.query.filter_by(deporte_id=id).order_by(Nivel.orden).all()
    return jsonify([{"id": n.id, "nombre": n.nombre} for n in niveles])
