from datetime import datetime
from config import app, db
from models import Ilustrador, Ilustracion

ILUSTRADORES_DATA = [
    {
        "fname": "Joaquin",
        "lname": "Quino",
        "especialidad": "Humor grafico e historieta",
        "ilustraciones": [
            {"titulo": "Mafalda y la sopa", "tecnica": "Tinta sobre papel", "anio": 1964, "precio": 25000.0},
            {"titulo": "El mundo segun Mafalda", "tecnica": "Tinta sobre papel", "anio": 1968, "precio": 30000.0},
            {"titulo": "Humano se nace", "tecnica": "Tinta sobre papel", "anio": 1991, "precio": 18000.0},
        ],
    },
    {
        "fname": "Alberto",
        "lname": "Breccia",
        "especialidad": "Historieta y novela grafica",
        "ilustraciones": [
            {"titulo": "El Eternauta - portada", "tecnica": "Tinta y gouache", "anio": 1957, "precio": 40000.0},
            {"titulo": "Mort Cinder", "tecnica": "Tinta sobre papel", "anio": 1962, "precio": 35000.0},
            {"titulo": "Perramus", "tecnica": "Tinta y acuarela", "anio": 1984, "precio": 28000.0},
        ],
    },
    {
        "fname": "Roberto",
        "lname": "Fontanarrosa",
        "especialidad": "Humor grafico y caricatura",
        "ilustraciones": [
            {"titulo": "Inodoro Pereyra vol. 1", "tecnica": "Tinta sobre papel", "anio": 1972, "precio": 15000.0},
            {"titulo": "Boogie el aceitoso", "tecnica": "Tinta sobre papel", "anio": 1975, "precio": 17000.0},
            {"titulo": "El mundo ha vivido equivocado", "tecnica": "Tinta", "anio": 1982, "precio": 12000.0},
        ],
    },
]


def build_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        for datos in ILUSTRADORES_DATA:
            ilustrador = Ilustrador(
                fname=datos["fname"],
                lname=datos["lname"],
                especialidad=datos["especialidad"],
                timestamp=datetime.utcnow(),
            )
            for il in datos["ilustraciones"]:
                ilustracion = Ilustracion(
                    titulo=il["titulo"],
                    tecnica=il["tecnica"],
                    anio=il["anio"],
                    precio=il["precio"],
                    timestamp=datetime.utcnow(),
                )
                ilustrador.ilustraciones.append(ilustracion)
            db.session.add(ilustrador)

        db.session.commit()
        print("Base de datos creada con datos de ejemplo.")


if __name__ == "__main__":
    build_database()