"""
people.py — Controladores (handlers) para la API REST de People.
Connexion mapea cada operationId del swagger.yml a una función de este módulo.
"""

from flask import abort, make_response
from config import db
from models import Person, people_schema, person_schema


def read_all():
    """GET /api/people — Devuelve todas las personas."""
    people = Person.query.order_by(Person.lname).all()
    return people_schema.dump(people)


def create(person):
    """POST /api/people — Crea una nueva persona."""
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Ya existe una persona con apellido '{lname}'")


def read_one(lname):
    """GET /api/people/{lname} — Devuelve una persona por apellido."""
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"No se encontró persona con apellido '{lname}'")


def update(lname, person):
    """PUT /api/people/{lname} — Actualiza el nombre de una persona."""
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 200
    else:
        abort(404, f"No se encontró persona con apellido '{lname}'")


def delete(lname):
    """DELETE /api/people/{lname} — Elimina una persona."""
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"'{lname}' eliminado correctamente", 200)
    else:
        abort(404, f"No se encontró persona con apellido '{lname}'")
