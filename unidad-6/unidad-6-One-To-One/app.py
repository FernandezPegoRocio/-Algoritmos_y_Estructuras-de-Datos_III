"""
app.py — Punto de entrada de la aplicación Flask REST API.
(versión sin Connexion, compatible con Python 3.14)

Ejecución:
    python app.py

La API queda disponible en:
    http://localhost:8000/           (página de inicio HTML)
    http://localhost:8000/api/people (JSON con todas las personas)
"""

from flask import render_template, request, jsonify, abort, make_response
import config
from config import app, db
from models import Person, person_schema, people_schema


# ── Página de inicio ──────────────────────────────────────────────────────────

@app.route("/")
def home():
    """Muestra todas las personas en formato HTML."""
    people = Person.query.order_by(Person.lname).all()
    return render_template("home.html", people=people)


# ── API REST /api/people ──────────────────────────────────────────────────────

@app.route("/api/people", methods=["GET"])
def read_all():
    """GET /api/people — Devuelve todas las personas."""
    people = Person.query.order_by(Person.lname).all()
    return jsonify(people_schema.dump(people))


@app.route("/api/people", methods=["POST"])
def create():
    """POST /api/people — Crea una nueva persona."""
    person_data = request.get_json()
    lname = person_data.get("lname")

    existing = Person.query.filter(Person.lname == lname).one_or_none()
    if existing is not None:
        abort(406, description=f"Ya existe una persona con apellido '{lname}'")

    new_person = person_schema.load(person_data, session=db.session)
    db.session.add(new_person)
    db.session.commit()
    return jsonify(person_schema.dump(new_person)), 201


@app.route("/api/people/<lname>", methods=["GET"])
def read_one(lname):
    """GET /api/people/{lname} — Devuelve una persona por apellido."""
    person = Person.query.filter(Person.lname == lname).one_or_none()
    if person is None:
        abort(404, description=f"No se encontró persona con apellido '{lname}'")
    return jsonify(person_schema.dump(person))


@app.route("/api/people/<lname>", methods=["PUT"])
def update(lname):
    """PUT /api/people/{lname} — Actualiza el nombre de una persona."""
    existing = Person.query.filter(Person.lname == lname).one_or_none()
    if existing is None:
        abort(404, description=f"No se encontró persona con apellido '{lname}'")

    person_data = request.get_json()
    update_person = person_schema.load(person_data, session=db.session)
    existing.fname = update_person.fname
    db.session.merge(existing)
    db.session.commit()
    return jsonify(person_schema.dump(existing)), 200


@app.route("/api/people/<lname>", methods=["DELETE"])
def delete(lname):
    """DELETE /api/people/{lname} — Elimina una persona."""
    existing = Person.query.filter(Person.lname == lname).one_or_none()
    if existing is None:
        abort(404, description=f"No se encontró persona con apellido '{lname}'")

    db.session.delete(existing)
    db.session.commit()
    return make_response(jsonify({"mensaje": f"'{lname}' eliminado correctamente"}), 200)


# ── Arranque ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # crea people.db y la tabla person si no existen
    app.run(host="0.0.0.0", port=8000, debug=True)