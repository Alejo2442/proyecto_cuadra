import os
from flask import Flask
from config import Config
from extensions import db, login_manager
from models.usuario import Usuario
from models.deporte import Deporte
from models.nivel import Nivel
from models.ciudad import Ciudad
from models.zona import Zona
from controllers.auth_controller import auth_bp
from controllers.usuario_controller import usuarios_bp
from controllers.perfil_controller import perfiles_bp
from controllers.deporte_controller import deportes_bp
from controllers.nivel_controller import niveles_bp
from controllers.ciudad_controller import ciudades_bp
from controllers.zona_controller import zonas_bp
from controllers.api_controller import api_bp


@login_manager.user_loader
def cargar_usuario(user_id):
    return db.session.get(Usuario, int(user_id))


def cargar_datos_iniciales():
    if not Usuario.query.filter_by(usuario="admin").first():
        admin = Usuario(usuario="admin", es_admin=True)
        admin.set_contrasena(os.getenv("ADMIN_PASSWORD", "admin123"))
        db.session.add(admin)

    if not Deporte.query.first():
        niveles = {
            "Fútbol": ["Principiante", "Intermedio", "Avanzado"],
            "Jiu-jitsu": ["Cinturón blanco", "Cinturón azul", "Cinturón morado",
                          "Cinturón marrón", "Cinturón negro"],
        }
        for nombre, lista in niveles.items():
            deporte = Deporte(nombre=nombre)
            db.session.add(deporte)
            for orden, nivel in enumerate(lista, start=1):
                db.session.add(Nivel(deporte=deporte, nombre=nivel, orden=orden))

    if not Ciudad.query.first():
        zonas = {
            "Quito": ["Norte", "Centro", "Sur", "Cumbayá - Tumbaco", "Valle de los Chillos"],
            "Guayaquil": ["Norte", "Centro", "Sur", "Samborondón"],
        }
        for nombre, lista in zonas.items():
            ciudad = Ciudad(nombre=nombre)
            db.session.add(ciudad)
            for zona in lista:
                db.session.add(Zona(ciudad=ciudad, nombre=zona))

    db.session.commit()


def crear_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Inicia sesión para acceder a esta página"
    login_manager.login_message_category = "error"

    for blueprint in (auth_bp, usuarios_bp, perfiles_bp, deportes_bp,
                      niveles_bp, ciudades_bp, zonas_bp, api_bp):
        app.register_blueprint(blueprint)

    with app.app_context():
        db.create_all()
        cargar_datos_iniciales()

    return app


app = crear_app()

if __name__ == "__main__":
    app.run(debug=True)
