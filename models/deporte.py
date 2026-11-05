from extensions import db


class Deporte(db.Model):
    __tablename__ = "deportes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), unique=True, nullable=False)

    niveles = db.relationship("Nivel", back_populates="deporte", order_by="Nivel.orden")
