import sqlite3
from datetime import datetime

from .modelo import (Cliente, Estado, Hito, Notificacion, Producto,
                     RepresentanteTelefonico, Ticket, TipoProducto)


class UsuarioDuplicado(Exception):
    pass


ESQUEMA = """
CREATE TABLE IF NOT EXISTS tipo_producto (
    id      INTEGER PRIMARY KEY,
    rubro   TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS usuario (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    email        TEXT NOT NULL UNIQUE,
    rol          TEXT NOT NULL CHECK (rol IN ('cliente', 'representante')),
    nombre       TEXT,
    telefono     TEXT,
    legajo       TEXT,
    especialidad TEXT
);
CREATE TABLE IF NOT EXISTS representante_tipo (
    representante_id INTEGER NOT NULL REFERENCES usuario(id),
    tipo_producto_id INTEGER NOT NULL REFERENCES tipo_producto(id),
    PRIMARY KEY (representante_id, tipo_producto_id)
);
CREATE TABLE IF NOT EXISTS producto (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion      TEXT NOT NULL,
    tipo_producto_id INTEGER REFERENCES tipo_producto(id)
);
CREATE TABLE IF NOT EXISTS ticket (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo           TEXT NOT NULL,
    descripcion      TEXT NOT NULL,
    estado           TEXT NOT NULL,
    fecha            TEXT NOT NULL,
    cliente_id       INTEGER NOT NULL REFERENCES usuario(id),
    representante_id INTEGER REFERENCES usuario(id),
    producto_id      INTEGER NOT NULL UNIQUE REFERENCES producto(id)
);
CREATE TABLE IF NOT EXISTS hito (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL REFERENCES ticket(id),
    contenido TEXT NOT NULL,
    fecha     TEXT NOT NULL,
    autor_id  INTEGER NOT NULL REFERENCES usuario(id)
);
CREATE TABLE IF NOT EXISTS notificacion (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id       INTEGER NOT NULL REFERENCES ticket(id),
    destinatario_id INTEGER NOT NULL REFERENCES usuario(id),
    mensaje         TEXT NOT NULL,
    fecha           TEXT NOT NULL,
    enviada         INTEGER NOT NULL DEFAULT 0
);
"""


class BaseDeDatos:
    def __init__(self, ruta="ticketing.db"):
        self.conexion = sqlite3.connect(ruta, check_same_thread=False)
        self.conexion.row_factory = sqlite3.Row
        self.conexion.execute("PRAGMA foreign_keys = ON")
        self.conexion.executescript(ESQUEMA)
        self.conexion.executemany(
            "INSERT OR IGNORE INTO tipo_producto (id, rubro) VALUES (?, ?)",
            [(t.id, t.getRubro()) for t in TipoProducto])
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()

    def guardarUsuario(self, usuario):
        try:
            with self.conexion:
                if isinstance(usuario, Cliente):
                    cursor = self.conexion.execute(
                        "INSERT INTO usuario (email, rol, nombre, telefono) VALUES (?, 'cliente', ?, ?)",
                        (usuario.email, usuario.nombre, usuario.telefono))
                else:
                    cursor = self.conexion.execute(
                        "INSERT INTO usuario (email, rol, legajo, especialidad) VALUES (?, 'representante', ?, ?)",
                        (usuario.email, usuario.legajo, usuario.especialidad))
                    self.conexion.executemany(
                        "INSERT INTO representante_tipo VALUES (?, ?)",
                        [(cursor.lastrowid, t.id) for t in usuario.tiposProducto])
        except sqlite3.IntegrityError:
            raise UsuarioDuplicado(f"Ya existe un usuario con el email {usuario.email}.")
        usuario.id = cursor.lastrowid
        return usuario

    def _usuarioDesdeFila(self, fila):
        if fila["rol"] == "cliente":
            return Cliente(fila["email"], fila["nombre"], fila["telefono"], id=fila["id"])
        tipos = [TipoProducto.desdeId(r["tipo_producto_id"]) for r in self.conexion.execute(
            "SELECT tipo_producto_id FROM representante_tipo WHERE representante_id = ? ORDER BY 1",
            (fila["id"],))]
        return RepresentanteTelefonico(fila["email"], fila["legajo"], fila["especialidad"],
                                       tipos, id=fila["id"])

    def buscarUsuarioPorEmail(self, email):
        fila = self.conexion.execute("SELECT * FROM usuario WHERE email = ?", (email,)).fetchone()
        return self._usuarioDesdeFila(fila) if fila else None

    def listarUsuarios(self):
        filas = self.conexion.execute("SELECT * FROM usuario ORDER BY id").fetchall()
        return [self._usuarioDesdeFila(f) for f in filas]

    def listarRepresentantes(self):
        return [u for u in self.listarUsuarios() if isinstance(u, RepresentanteTelefonico)]

    def guardarTicket(self, ticket):
        with self.conexion:
            tipo_id = ticket.producto.tipo.id if ticket.producto.tipo else None
            rep_id = ticket.representante.id if ticket.representante else None
            if ticket.id is None:
                cursor = self.conexion.execute(
                    "INSERT INTO producto (descripcion, tipo_producto_id) VALUES (?, ?)",
                    (ticket.producto.descripcion, tipo_id))
                ticket.producto.id = cursor.lastrowid
                cursor = self.conexion.execute(
                    "INSERT INTO ticket (titulo, descripcion, estado, fecha, cliente_id, "
                    "representante_id, producto_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (ticket.titulo, ticket.descripcion, ticket.estado.value,
                     ticket.fecha.isoformat(), ticket.cliente.id, rep_id, ticket.producto.id))
                ticket.id = cursor.lastrowid
            else:
                self.conexion.execute(
                    "UPDATE ticket SET estado = ?, representante_id = ? WHERE id = ?",
                    (ticket.estado.value, rep_id, ticket.id))
        return ticket

    def actualizarProducto(self, producto):
        with self.conexion:
            self.conexion.execute(
                "UPDATE producto SET tipo_producto_id = ? WHERE id = ?",
                (producto.tipo.id if producto.tipo else None, producto.id))

    def guardarHito(self, ticket, hito):
        with self.conexion:
            cursor = self.conexion.execute(
                "INSERT INTO hito (ticket_id, contenido, fecha, autor_id) VALUES (?, ?, ?, ?)",
                (ticket.id, hito.contenido, hito.fecha.isoformat(), hito.autor.id))
        hito.id = cursor.lastrowid
        return hito

    def guardarNotificacion(self, notificacion):
        with self.conexion:
            cursor = self.conexion.execute(
                "INSERT INTO notificacion (ticket_id, destinatario_id, mensaje, fecha, enviada) "
                "VALUES (?, ?, ?, ?, ?)",
                (notificacion.ticket.id, notificacion.destinatario.id, notificacion.mensaje,
                 notificacion.fecha.isoformat(), int(notificacion.enviada)))
        notificacion.id = cursor.lastrowid
        return notificacion

    def cargarTickets(self):
        usuarios = {u.id: u for u in self.listarUsuarios()}
        tickets = []
        for f in self.conexion.execute(
                "SELECT t.*, p.descripcion AS p_desc, p.tipo_producto_id "
                "FROM ticket t JOIN producto p ON p.id = t.producto_id ORDER BY t.id"):
            producto = Producto(f["p_desc"], TipoProducto.desdeId(f["tipo_producto_id"]),
                                id=f["producto_id"])
            ticket = Ticket(f["titulo"], f["descripcion"], usuarios[f["cliente_id"]], producto,
                            representante=usuarios.get(f["representante_id"]),
                            estado=Estado(f["estado"]),
                            fecha=datetime.fromisoformat(f["fecha"]), id=f["id"])
            for h in self.conexion.execute(
                    "SELECT * FROM hito WHERE ticket_id = ? ORDER BY id", (ticket.id,)):
                ticket.agregarHito(Hito(h["contenido"], usuarios[h["autor_id"]],
                                        datetime.fromisoformat(h["fecha"]), id=h["id"]))
            for n in self.conexion.execute(
                    "SELECT * FROM notificacion WHERE ticket_id = ? ORDER BY id", (ticket.id,)):
                ticket.agregarNotificacion(Notificacion(
                    n["mensaje"], ticket, usuarios[n["destinatario_id"]],
                    datetime.fromisoformat(n["fecha"]), bool(n["enviada"]), id=n["id"]))
            tickets.append(ticket)
        return tickets
