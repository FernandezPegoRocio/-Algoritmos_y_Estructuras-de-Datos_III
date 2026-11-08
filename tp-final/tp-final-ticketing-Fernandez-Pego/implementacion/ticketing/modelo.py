from datetime import datetime
from enum import Enum


class TransicionInvalida(Exception):
    pass


class TicketCerrado(Exception):
    pass


class Estado(Enum):
    ABIERTO = "abierto"
    EN_PROCESO = "en proceso"
    CERRADO = "cerrado"

    def getNombre(self):
        return self.value

    def getTransicionesValidas(self):
        return list(_TRANSICIONES[self])

    def esValido(self, destino):
        return destino in _TRANSICIONES[self]

    def transicion(self, destino):
        if not self.esValido(destino):
            raise TransicionInvalida(
                f"No se puede pasar de '{self.value}' a '{destino.value}'.")
        return destino


_TRANSICIONES = {
    Estado.ABIERTO: (Estado.EN_PROCESO, Estado.CERRADO),
    Estado.EN_PROCESO: (Estado.CERRADO,),
    Estado.CERRADO: (Estado.ABIERTO,),
}


class TipoProducto(Enum):
    LINEA_BLANCA = (1, "línea blanca")
    COCINA = (2, "cocina")
    ELECTRO = (3, "electro")
    PEQUENOS_ELECTRODOMESTICOS = (4, "pequeños electrodomésticos")

    @property
    def id(self):
        return self.value[0]

    def getRubro(self):
        return self.value[1]

    @staticmethod
    def esValido(rubro):
        return any(t.getRubro() == rubro for t in TipoProducto)

    @staticmethod
    def desdeId(id):
        for t in TipoProducto:
            if t.id == id:
                return t
        return None


class Usuario:
    def __init__(self, email, id=None):
        self.id = id
        self.email = email
        self.conectado = False

    def login(self, email):
        self.conectado = (email == self.email)
        return self.conectado

    def logout(self):
        self.conectado = False

    def __eq__(self, otro):
        return isinstance(otro, Usuario) and self.email == otro.email

    def __hash__(self):
        return hash(self.email)


class Cliente(Usuario):
    def __init__(self, email, nombre, telefono, id=None):
        super().__init__(email, id)
        self.nombre = nombre
        self.telefono = telefono

    def crearTicket(self, titulo, descripcion, producto):
        return Ticket(titulo, descripcion, self, producto)

    def registrarHito(self, ticket, contenido):
        if ticket.estaCerrado():
            raise TicketCerrado("El ticket está cerrado. Reabrilo para seguir la conversación.")
        hito = Hito(contenido, self)
        ticket.agregarHito(hito)
        return hito

    def __str__(self):
        return f"{self.nombre} <{self.email}>"


class RepresentanteTelefonico(Usuario):
    def __init__(self, email, legajo, especialidad, tiposProducto=None, id=None):
        super().__init__(email, id)
        self.legajo = legajo
        self.especialidad = especialidad
        self.tiposProducto = list(tiposProducto or [])

    def cambiarEstado(self, ticket, estado):
        ticket.cambiarEstado(estado)

    def registrarHito(self, ticket, contenido):
        if ticket.estaCerrado():
            raise TicketCerrado("El ticket está cerrado. Reabrilo para seguir la conversación.")
        hito = Hito(contenido, self)
        ticket.agregarHito(hito)
        return hito

    def listarTickets(self, tickets):
        return [t for t in tickets if t.representante == self]

    def atiende(self, tipo):
        return tipo in self.tiposProducto

    def __str__(self):
        return f"Legajo {self.legajo} ({self.especialidad}) <{self.email}>"


class Producto:
    def __init__(self, descripcion, tipo=None, id=None):
        self.id = id
        self.descripcion = descripcion
        self.tipo = tipo

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def __str__(self):
        rubro = self.tipo.getRubro() if self.tipo else "sin tipo"
        return f"{self.descripcion} ({rubro})"


class Hito:
    def __init__(self, contenido, autor, fecha=None, id=None):
        self.id = id
        self.contenido = contenido
        self.fecha = fecha or datetime.now()
        self.autor = autor


class Notificacion:
    def __init__(self, mensaje, ticket, destinatario, fecha=None, enviada=False, id=None):
        self.id = id
        self.mensaje = mensaje
        self.fecha = fecha or datetime.now()
        self.ticket = ticket
        self.destinatario = destinatario
        self.enviada = enviada

    def enviar(self, destinatario):
        self.destinatario = destinatario
        self.enviada = True

    def getDestinatario(self):
        return self.destinatario


class Ticket:
    def __init__(self, titulo, descripcion, cliente, producto,
                 representante=None, estado=None, fecha=None, id=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.cliente = cliente
        self.producto = producto
        self.representante = representante
        self.fecha = fecha or datetime.now()
        self.hitos = []
        self.notificaciones = []
        self.estado = None
        if estado is None:
            self.abrir()
        else:
            self.estado = estado

    def abrir(self):
        self.estado = Estado.ABIERTO

    def cerrar(self):
        self.cambiarEstado(Estado.CERRADO)

    def reabrir(self):
        if self.estado != Estado.CERRADO:
            raise TransicionInvalida("Solo se puede reabrir un ticket cerrado.")
        self.cambiarEstado(Estado.ABIERTO)

    def cambiarEstado(self, e):
        self.estado = self.estado.transicion(e)

    def agregarHito(self, h):
        self.hitos.append(h)

    def estaCerrado(self):
        return self.estado == Estado.CERRADO

    def agregarNotificacion(self, n):
        self.notificaciones.append(n)

    def getProducto(self):
        return self.producto

    def contraparte(self, usuario):
        return self.representante if usuario == self.cliente else self.cliente
