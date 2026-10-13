"""
Unidad 6 - ORM SQLAlchemy 2+
Ejemplo 2: Relación Many-to-Many (Estudiantes y Materias)

Un estudiante puede estar inscripto en muchas materias,
y una materia puede tener muchos estudiantes.
La relación se implementa con una tabla de asociación intermedia.
"""

from sqlalchemy import create_engine, String, Table, Column, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)


# ── Base declarativa ──────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── Tabla de asociación (intermedia) ─────────────────────────────
# No es un modelo, es solo la tabla que conecta ambas entidades
inscripcion = Table(
    "inscripcion",
    Base.metadata,
    Column("estudiante_id", ForeignKey("estudiante.id"), primary_key=True),
    Column("materia_id", ForeignKey("materia.id"), primary_key=True),
)


# ── Modelos ───────────────────────────────────────────────────────
class Estudiante(Base):
    __tablename__ = "estudiante"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    # Muchos estudiantes ↔ muchas materias
    materias: Mapped[list["Materia"]] = relationship(
        secondary=inscripcion,
        back_populates="estudiantes",
    )

    def __repr__(self) -> str:
        return f"Estudiante(id={self.id}, nombre={self.nombre!r})"


class Materia(Base):
    __tablename__ = "materia"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    # Muchas materias ↔ muchos estudiantes
    estudiantes: Mapped[list["Estudiante"]] = relationship(
        secondary=inscripcion,
        back_populates="materias",
    )

    def __repr__(self) -> str:
        return f"Materia(id={self.id}, nombre={self.nombre!r})"


# ── Configuración de la base de datos ────────────────────────────
engine = create_engine("sqlite:///many_to_many.db", echo=False)
Base.metadata.create_all(engine)


# ── CRUD ─────────────────────────────────────────────────────────
def crear_datos():
    with Session(engine) as session:
        algoritmos = Materia(nombre="Algoritmos y Estructuras de Datos III")
        redes = Materia(nombre="Redes de Computadoras")
        sistemas = Materia(nombre="Sistemas Operativos")

        rocio = Estudiante(nombre="Rocío", materias=[algoritmos, redes])
        ana = Estudiante(nombre="Ana", materias=[algoritmos, sistemas])
        carlos = Estudiante(nombre="Carlos", materias=[redes, sistemas, algoritmos])

        session.add_all([rocio, ana, carlos])
        session.commit()
        print("Datos creados correctamente.")


def leer_inscripciones():
    with Session(engine) as session:
        estudiantes = session.query(Estudiante).all()
        print("\n=== Estudiantes y sus materias ===")
        for est in estudiantes:
            materias_str = ", ".join(m.nombre for m in est.materias)
            print(f"  {est.nombre}: {materias_str}")

        print("\n=== Materias y sus estudiantes ===")
        materias = session.query(Materia).all()
        for mat in materias:
            alumnos_str = ", ".join(e.nombre for e in mat.estudiantes)
            print(f"  {mat.nombre}: {alumnos_str}")


def agregar_inscripcion():
    with Session(engine) as session:
        rocio = session.query(Estudiante).filter(Estudiante.nombre == "Rocío").first()
        sistemas = session.query(Materia).filter(Materia.nombre == "Sistemas Operativos").first()
        if rocio and sistemas and sistemas not in rocio.materias:
            rocio.materias.append(sistemas)
            session.commit()
            print(f"\nRocío inscripta en: {sistemas.nombre}")


def desinscribir():
    with Session(engine) as session:
        ana = session.query(Estudiante).filter(Estudiante.nombre == "Ana").first()
        redes = session.query(Materia).filter(Materia.nombre == "Redes de Computadoras").first()
        if redes and redes in ana.materias:
            ana.materias.remove(redes)
            session.commit()
            print(f"\nAna desinscripta de: {redes.nombre}")


if __name__ == "__main__":
    crear_datos()
    leer_inscripciones()
    agregar_inscripcion()
    desinscribir()
    leer_inscripciones()
