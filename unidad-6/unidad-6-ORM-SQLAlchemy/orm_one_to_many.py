"""
Unidad 6 - ORM SQLAlchemy 2+
Ejemplo 1: Relación One-to-Many (Un autor tiene muchos libros)

Una persona (Author) puede tener muchos libros (Book),
pero cada libro pertenece a un solo autor.
"""

from sqlalchemy import create_engine, String, ForeignKey
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


# ── Modelos ───────────────────────────────────────────────────────
class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # Un autor tiene muchos libros
    books: Mapped[list["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Author(id={self.id}, name={self.name!r})"


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    # Cada libro pertenece a un autor
    author: Mapped["Author"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title!r})"


# ── Configuración de la base de datos ────────────────────────────
engine = create_engine("sqlite:///one_to_many.db", echo=False)
Base.metadata.create_all(engine)

# ── CRUD ─────────────────────────────────────────────────────────
def crear_datos():
    with Session(engine) as session:
        autor1 = Author(
            name="Gabriel García Márquez",
            books=[
                Book(title="Cien años de soledad"),
                Book(title="El amor en los tiempos del cólera"),
            ],
        )
        autor2 = Author(
            name="Jorge Luis Borges",
            books=[
                Book(title="Ficciones"),
                Book(title="El Aleph"),
                Book(title="El libro de arena"),
            ],
        )
        session.add_all([autor1, autor2])
        session.commit()
        print("Datos creados correctamente.")


def leer_autores_con_libros():
    with Session(engine) as session:
        autores = session.query(Author).all()
        print("\n=== Autores y sus libros ===")
        for autor in autores:
            print(f"\n{autor.name}:")
            for libro in autor.books:
                print(f"  - {libro.title}")


def actualizar_libro():
    with Session(engine) as session:
        libro = session.query(Book).filter(Book.title == "El Aleph").first()
        if libro:
            libro.title = "El Aleph (edición revisada)"
            session.commit()
            print(f"\nLibro actualizado: {libro.title}")


def eliminar_autor():
    with Session(engine) as session:
        autor = session.query(Author).filter(Author.name == "Jorge Luis Borges").first()
        if autor:
            session.delete(autor)   # cascade elimina sus libros también
            session.commit()
            print(f"\nAutor y sus libros eliminados.")


if __name__ == "__main__":
    crear_datos()
    leer_autores_con_libros()
    actualizar_libro()
    leer_autores_con_libros()
    eliminar_autor()
    leer_autores_con_libros()
