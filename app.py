from flask import Flask
from config import Config
from extensions import db, login_manager
from models.usuario import Usuario
from controllers.auth_controller import auth_bp
from controllers.usuario_controller import usuarios_bp


@login_manager.user_loader
def cargar_usuario(user_id):
    return db.session.get(Usuario, int(user_id))


def crear_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Inicia sesión"
    login_manager.login_message_category = "warning"

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)

    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(usuario="admin").first():
            admin = Usuario(usuario="admin")
            admin.set_contrasena("admin123")
            db.session.add(admin)
            db.session.commit()

    return app


app = crear_app()

if __name__ == "__main__":
    app.run(debug=True)