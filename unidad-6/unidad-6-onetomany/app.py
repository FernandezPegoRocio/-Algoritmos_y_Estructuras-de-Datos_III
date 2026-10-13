from flask import render_template, request, jsonify, abort, make_response

from config import app, db
from models import Note, Person, note_schema, person_schema, people_schema


# ── Página principal ──────────────────────────────────────────
@app.route("/")
def home():
    people = Person.query.all()
    return render_template("home.html", people=people)


# ── People ────────────────────────────────────────────────────
@app.route("/api/people", methods=["GET"])
def read_all():
    people = Person.query.all()
    return jsonify(people_schema.dump(people))


@app.route("/api/people", methods=["POST"])
def create_person():
    data = request.get_json()
    lname = data.get("lname")
    existing = Person.query.filter(Person.lname == lname).one_or_none()
    if existing is not None:
        abort(406, description=f"Person with last name {lname} already exists")
    new_person = person_schema.load(data, session=db.session)
    db.session.add(new_person)
    db.session.commit()
    return jsonify(person_schema.dump(new_person)), 201


@app.route("/api/people/<lname>", methods=["GET"])
def read_one_person(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()
    if person is None:
        abort(404, description=f"Person with last name {lname} not found")
    return jsonify(person_schema.dump(person))


@app.route("/api/people/<lname>", methods=["PUT"])
def update_person(lname):
    existing = Person.query.filter(Person.lname == lname).one_or_none()
    if existing is None:
        abort(404, description=f"Person with last name {lname} not found")
    data = request.get_json()
    update_p = person_schema.load(data, session=db.session)
    existing.fname = update_p.fname
    db.session.merge(existing)
    db.session.commit()
    return jsonify(person_schema.dump(existing)), 200


@app.route("/api/people/<lname>", methods=["DELETE"])
def delete_person(lname):
    existing = Person.query.filter(Person.lname == lname).one_or_none()
    if existing is None:
        abort(404, description=f"Person with last name {lname} not found")
    db.session.delete(existing)
    db.session.commit()
    return make_response(jsonify({"mensaje": f"{lname} eliminado"}), 200)


# ── Notes ─────────────────────────────────────────────────────
@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    person_id = data.get("person_id")
    person = Person.query.get(person_id)
    if person is None:
        abort(404, description=f"Person not found for ID: {person_id}")
    new_note = note_schema.load(data, session=db.session)
    person.notes.append(new_note)
    db.session.commit()
    return jsonify(note_schema.dump(new_note)), 201


@app.route("/api/notes/<int:note_id>", methods=["GET"])
def read_one_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        abort(404, description=f"Note with ID {note_id} not found")
    return jsonify(note_schema.dump(note))


@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    existing = db.session.get(Note, note_id)
    if existing is None:
        abort(404, description=f"Note with ID {note_id} not found")
    data = request.get_json()
    update_n = note_schema.load(data, session=db.session)
    existing.content = update_n.content
    db.session.merge(existing)
    db.session.commit()
    return jsonify(note_schema.dump(existing)), 200


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    existing = db.session.get(Note, note_id)
    if existing is None:
        abort(404, description=f"Note with ID {note_id} not found")
    db.session.delete(existing)
    db.session.commit()
    return make_response(jsonify({"mensaje": f"Nota {note_id} eliminada"}), 200)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000, debug=True)
