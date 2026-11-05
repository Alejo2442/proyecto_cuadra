from extensions import db


class PerfilDeportivo(db.Model):
    __tablename__ = "perfiles_deportivos"
    __table_args__ = (db.UniqueConstraint("usuario_id", "deporte_id"),)

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    deporte_id = db.Column(db.Integer, db.ForeignKey("deportes.id"), nullable=False)
    nivel_id = db.Column(db.Integer, db.ForeignKey("niveles.id"), nullable=False)
    posicion = db.Column(db.String(40))
    peso = db.Column(db.Float)

    usuario = db.relationship("Usuario", back_populates="perfiles")
    deporte = db.relationship("Deporte")
    nivel = db.relationship("Nivel")
