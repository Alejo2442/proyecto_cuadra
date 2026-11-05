from extensions import db


class Ciudad(db.Model):
    __tablename__ = "ciudades"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True, nullable=False)

    zonas = db.relationship("Zona", back_populates="ciudad", order_by="Zona.nombre")
