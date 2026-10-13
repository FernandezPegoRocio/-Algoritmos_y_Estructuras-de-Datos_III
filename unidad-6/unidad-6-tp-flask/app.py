from flask import render_template, abort
from config import app, db
from models import (
    Ilustrador,
    IlustradorSchema,
    Ilustracion,
    IlustracionSchema,
    ilustrador_schema,
    ilustradores_schema,
    ilustracion_schema,
)


@app.route("/")
def home():
    ilustradores = db.session.execute(db.select(Ilustrador)).scalars().all()
    return render_template("home.html", ilustradores=ilustradores)


# ── Ilustradores ──────────────────────────────────────────────────────────────

@app.route("/api/ilustradores", methods=["GET"])
def get_ilustradores():
    ilustradores = db.session.execute(db.select(Ilustrador)).scalars().all()
    return ilustradores_schema.dump(ilustradores)


@app.route("/api/ilustradores", methods=["POST"])
def create_ilustrador():
    from flask import request
    data = request.get_json()
    lname = data.get("lname")
    if not lname:
        abort(400, "El campo 'lname' es obligatorio")
    existing = db.session.execute(
        db.select(Ilustrador).filter(Ilustrador.lname == lname)
    ).scalar()
    if existing:
        abort(409, f"Ya existe un ilustrador con apellido '{lname}'")
    nuevo = ilustrador_schema.load(data)
    db.session.add(nuevo)
    db.session.commit()
    return ilustrador_schema.dump(nuevo), 201


@app.route("/api/ilustradores/<int:ilustrador_id>", methods=["GET"])
def get_ilustrador(ilustrador_id):
    ilustrador = db.session.get(Ilustrador, ilustrador_id)
    if ilustrador is None:
        abort(404, f"Ilustrador con id {ilustrador_id} no encontrado")
    return ilustrador_schema.dump(ilustrador)


@app.route("/api/ilustradores/<int:ilustrador_id>", methods=["PUT"])
def update_ilustrador(ilustrador_id):
    from flask import request
    ilustrador = db.session.get(Ilustrador, ilustrador_id)
    if ilustrador is None:
        abort(404, f"Ilustrador con id {ilustrador_id} no encontrado")
    data = request.get_json()
    ilustrador_schema.load(data, instance=ilustrador, partial=True)
    db.session.commit()
    return ilustrador_schema.dump(ilustrador)


@app.route("/api/ilustradores/<int:ilustrador_id>", methods=["DELETE"])
def delete_ilustrador(ilustrador_id):
    ilustrador = db.session.get(Ilustrador, ilustrador_id)
    if ilustrador is None:
        abort(404, f"Ilustrador con id {ilustrador_id} no encontrado")
    db.session.delete(ilustrador)
    db.session.commit()
    return {"mensaje": f"Ilustrador {ilustrador_id} eliminado correctamente"}


# ── Ilustraciones ─────────────────────────────────────────────────────────────

@app.route("/api/ilustraciones", methods=["POST"])
def create_ilustracion():
    from flask import request
    data = request.get_json()
    ilustrador_id = data.get("ilustrador_id")
    ilustrador = db.session.get(Ilustrador, ilustrador_id)
    if ilustrador is None:
        abort(404, f"Ilustrador con id {ilustrador_id} no encontrado")
    nueva = ilustracion_schema.load(data)
    db.session.add(nueva)
    db.session.commit()
    return ilustracion_schema.dump(nueva), 201


@app.route("/api/ilustraciones/<int:ilustracion_id>", methods=["GET"])
def get_ilustracion(ilustracion_id):
    ilustracion = db.session.get(Ilustracion, ilustracion_id)
    if ilustracion is None:
        abort(404, f"Ilustración con id {ilustracion_id} no encontrada")
    return ilustracion_schema.dump(ilustracion)


@app.route("/api/ilustraciones/<int:ilustracion_id>", methods=["PUT"])
def update_ilustracion(ilustracion_id):
    from flask import request
    ilustracion = db.session.get(Ilustracion, ilustracion_id)
    if ilustracion is None:
        abort(404, f"Ilustración con id {ilustracion_id} no encontrada")
    data = request.get_json()
    ilustracion_schema.load(data, instance=ilustracion, partial=True)
    db.session.commit()
    return ilustracion_schema.dump(ilustracion)


@app.route("/api/ilustraciones/<int:ilustracion_id>", methods=["DELETE"])
def delete_ilustracion(ilustracion_id):
    ilustracion = db.session.get(Ilustracion, ilustracion_id)
    if ilustracion is None:
        abort(404, f"Ilustración con id {ilustracion_id} no encontrada")
    db.session.delete(ilustracion)
    db.session.commit()
    return {"mensaje": f"Ilustración {ilustracion_id} eliminada correctamente"}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
