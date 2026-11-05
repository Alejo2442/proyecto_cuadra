from extensions import db


class Nivel(db.Model):
    __tablename__ = "niveles"
    __table_args__ = (db.UniqueConstraint("deporte_id", "nombre"),)

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    orden = db.Column(db.Integer, nullable=False)
    deporte_id = db.Column(db.Integer, db.ForeignKey("deportes.id"), nullable=False)

    deporte = db.relationship("Deporte", back_populates="niveles")
