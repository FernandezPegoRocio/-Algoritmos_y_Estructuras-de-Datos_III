from datetime import datetime

from marshmallow_sqlalchemy import fields

from config import db, ma


class Ilustracion(db.Model):
    __tablename__ = "ilustracion"
    id = db.Column(db.Integer, primary_key=True)
    ilustrador_id = db.Column(db.Integer, db.ForeignKey("ilustrador.id"))
    titulo = db.Column(db.String(100), nullable=False)
    tecnica = db.Column(db.String(50))
    anio = db.Column(db.Integer)
    precio = db.Column(db.Float)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class IlustracionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ilustracion
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Ilustrador(db.Model):
    __tablename__ = "ilustrador"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(32))
    lname = db.Column(db.String(32), unique=True, nullable=False)
    especialidad = db.Column(db.String(50))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    ilustraciones = db.relationship(
        Ilustracion,
        backref="ilustrador",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Ilustracion.anio)",
    )


class IlustradorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ilustrador
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    ilustraciones = fields.Nested(IlustracionSchema, many=True)


ilustracion_schema = IlustracionSchema()
ilustrador_schema = IlustradorSchema()
ilustradores_schema = IlustradorSchema(many=True)
