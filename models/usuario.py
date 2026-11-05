from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    cedula = db.Column(db.String(10), unique=True)
    telefono = db.Column(db.String(10))
    zona_id = db.Column(db.Integer, db.ForeignKey("zonas.id"))
    es_admin = db.Column(db.Boolean, nullable=False, default=False)

    zona = db.relationship("Zona")
    perfiles = db.relationship("PerfilDeportivo", back_populates="usuario", cascade="all, delete-orphan")

    def set_contrasena(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena_hash, contrasena)
