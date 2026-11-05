from extensions import db


class Zona(db.Model):
    __tablename__ = "zonas"
    __table_args__ = (db.UniqueConstraint("ciudad_id", "nombre"),)

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    ciudad_id = db.Column(db.Integer, db.ForeignKey("ciudades.id"), nullable=False)

    ciudad = db.relationship("Ciudad", back_populates="zonas")
