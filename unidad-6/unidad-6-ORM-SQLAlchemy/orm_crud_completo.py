"""
Unidad 6 - ORM SQLAlchemy 2+
Ejemplo 3: CRUD completo con modelo único (Producto)
"""

from sqlalchemy import create_engine, String, Float, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


# ── Base declarativa ──────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── Modelo ────────────────────────────────────────────────────────
class Producto(Base):
    __tablename__ = "producto"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        return (
            f"Producto(id={self.id}, nombre={self.nombre!r}, "
            f"precio={self.precio:.2f}, stock={self.stock})"
        )


# ── Configuración de la base de datos ────────────────────────────
engine = create_engine("sqlite:///crud_completo.db", echo=False)
Base.metadata.create_all(engine)


# ── CREATE ────────────────────────────────────────────────────────
def crear_producto(nombre: str, precio: float, stock: int) -> Producto:
    with Session(engine) as session:
        producto = Producto(nombre=nombre, precio=precio, stock=stock)
        session.add(producto)
        session.commit()
        session.refresh(producto)
        print(f"[CREATE] {producto}")
        return producto


# ── READ ──────────────────────────────────────────────────────────
def leer_todos() -> list[Producto]:
    with Session(engine) as session:
        productos = session.execute(select(Producto)).scalars().all()
        print("\n[READ] Todos los productos:")
        for p in productos:
            print(f"  {p}")
        return productos


def leer_por_id(producto_id: int) -> Producto | None:
    with Session(engine) as session:
        producto = session.get(Producto, producto_id)
        if producto:
            print(f"[READ] Encontrado: {producto}")
        else:
            print(f"[READ] No existe producto con id={producto_id}")
        return producto


def buscar_por_nombre(nombre: str) -> Producto | None:
    with Session(engine) as session:
        stmt = select(Producto).where(Producto.nombre == nombre)
        producto = session.execute(stmt).scalar_one_or_none()
        if producto:
            print(f"[READ] Encontrado por nombre: {producto}")
        else:
            print(f"[READ] No existe: '{nombre}'")
        return producto


# ── UPDATE ────────────────────────────────────────────────────────
def actualizar_precio(producto_id: int, nuevo_precio: float):
    with Session(engine) as session:
        producto = session.get(Producto, producto_id)
        if producto:
            producto.precio = nuevo_precio
            session.commit()
            print(f"[UPDATE] Precio actualizado: {producto}")
        else:
            print(f"[UPDATE] No existe producto con id={producto_id}")


def actualizar_stock(producto_id: int, cantidad: int):
    with Session(engine) as session:
        producto = session.get(Producto, producto_id)
        if producto:
            producto.stock += cantidad
            session.commit()
            print(f"[UPDATE] Stock actualizado: {producto}")
        else:
            print(f"[UPDATE] No existe producto con id={producto_id}")


# ── DELETE ────────────────────────────────────────────────────────
def eliminar_producto(producto_id: int):
    with Session(engine) as session:
        producto = session.get(Producto, producto_id)
        if producto:
            nombre = producto.nombre
            session.delete(producto)
            session.commit()
            print(f"[DELETE] Eliminado: '{nombre}' (id={producto_id})")
        else:
            print(f"[DELETE] No existe producto con id={producto_id}")


# ── Ejecución principal ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("CRUD COMPLETO - SQLAlchemy 2.0+ ORM")
    print("=" * 50)

    # CREATE
    p1 = crear_producto("Laptop", 1200.00, 10)
    p2 = crear_producto("Mouse inalámbrico", 25.50, 50)
    p3 = crear_producto("Teclado mecánico", 89.99, 30)
    p4 = crear_producto("Monitor 27\"", 350.00, 8)

    # READ
    leer_todos()
    leer_por_id(1)
    buscar_por_nombre("Mouse inalámbrico")
    leer_por_id(99)  # no existe

    # UPDATE
    print()
    actualizar_precio(1, 1099.00)       # baja de precio a Laptop
    actualizar_stock(2, 20)             # entran 20 mouses más

    # DELETE
    print()
    eliminar_producto(4)                # eliminamos el monitor
    eliminar_producto(99)               # id inexistente

    # Estado final
    leer_todos()
