"""
models.py — Modelos SQLAlchemy y esquemas Marshmallow
"""

from datetime import datetime
from config import db, ma


class Person(db.Model):
    """
    Representa una persona en la base de datos.
    Cada persona tiene un apellido único (lname) que actúa como identificador natural.
    """
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True, nullable=False)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"Person(id={self.id}, name={self.fname} {self.lname})"


class PersonSchema(ma.SQLAlchemyAutoSchema):
    """
    Esquema de serialización/deserialización para Person.
    SQLAlchemyAutoSchema genera automáticamente los campos a partir del modelo.
    """
    class Meta:
        model = Person
        load_instance = True       # deserializa directamente a instancias Person
        sqla_session = db.session  # usa la sesión de la app


# Instancias del esquema:
# person_schema  → para un solo objeto
# people_schema  → para listas (many=True)
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
