from .modelo import (Cliente, Estado, Hito, Notificacion, Producto,
                     RepresentanteTelefonico, TipoProducto)


class TicketNoEncontrado(Exception):
    pass


class PermisoDenegado(Exception):
    pass


class ControladorUsuario:
    def __init__(self, bd):
        self.bd = bd
        self.usuarioActual = None

    def registrarCliente(self, email, nombre, telefono):
        return self.bd.guardarUsuario(Cliente(email, nombre, telefono))

    def registrarRepresentante(self, email, legajo, especialidad, tiposProducto):
        return self.bd.guardarUsuario(
            RepresentanteTelefonico(email, legajo, especialidad, tiposProducto))

    def login(self, email):
        usuario = self.bd.buscarUsuarioPorEmail(email)
        if usuario and usuario.login(email):
            self.usuarioActual = usuario
            return True
        return False

    def buscarUsuario(self, email):
        return self.bd.buscarUsuarioPorEmail(email)

    def logout(self):
        if self.usuarioActual:
            self.usuarioActual.logout()
        self.usuarioActual = None

    def listarUsuarios(self):
        return self.bd.listarUsuarios()

    def listarRepresentantes(self):
        return self.bd.listarRepresentantes()


class ControladorNotificacion:
    def __init__(self, bd):
        self.bd = bd
        self.notificaciones = []

    def crearNotificacion(self, ticket, destinatario, mensaje):
        return Notificacion(mensaje, ticket, destinatario)

    def enviarNotificacion(self, n, destinatario):
        n.enviar(destinatario)
        n.ticket.agregarNotificacion(n)
        self.bd.guardarNotificacion(n)
        self.notificaciones.append(n)

    def notificar(self, ticket, destinatario, mensaje):
        if destinatario is None:
            return None
        n = self.crearNotificacion(ticket, destinatario, mensaje)
        self.enviarNotificacion(n, destinatario)
        return n


class ControladorTicket:
    def __init__(self, bd, controladorNotificacion):
        self.bd = bd
        self.controladorNotificacion = controladorNotificacion
        self.tickets = bd.cargarTickets()

    def crearTicket(self, datos):
        cliente = datos["cliente"]
        if not isinstance(cliente, Cliente):
            raise PermisoDenegado("Solo un cliente puede crear tickets.")
        producto = Producto(datos["producto"], datos.get("tipo"))
        ticket = cliente.crearTicket(datos["titulo"], datos["descripcion"], producto)
        ticket.representante = self.asignarRepresentante(producto.getTipo())
        self.bd.guardarTicket(ticket)
        self.tickets.append(ticket)
        self.controladorNotificacion.notificar(
            ticket, ticket.representante,
            f"Se te asignó el ticket #{ticket.id}: {ticket.titulo}")
        return ticket

    def asignarRepresentante(self, tipo):
        representantes = self.bd.listarRepresentantes()
        especialistas = [r for r in representantes if tipo and r.atiende(tipo)]
        candidatos = especialistas or representantes
        if not candidatos:
            return None
        return min(candidatos, key=lambda r: (self._carga(r), r.id))

    def _carga(self, representante):
        return sum(1 for t in self.tickets
                   if t.representante == representante and not t.estaCerrado())

    def buscarTicket(self, id):
        for t in self.tickets:
            if t.id == id:
                return t
        raise TicketNoEncontrado(f"No existe el ticket #{id}.")

    def listarTickets(self, usuario=None):
        if usuario is None:
            return list(self.tickets)
        if isinstance(usuario, RepresentanteTelefonico):
            return usuario.listarTickets(self.tickets)
        return [t for t in self.tickets if t.cliente == usuario]

    def solicitarEstadosValidos(self, id):
        return self.buscarTicket(id).estado.getTransicionesValidas()

    def cambiarEstado(self, id, e, autor):
        ticket = self.buscarTicket(id)
        self._verificarParticipante(ticket, autor)
        if isinstance(autor, Cliente) and e == Estado.EN_PROCESO:
            raise PermisoDenegado("Solo el representante puede pasar el ticket a 'en proceso'.")
        anterior = ticket.estado
        ticket.cambiarEstado(e)
        hito = Hito(f"Estado cambiado de '{anterior.getNombre()}' a '{e.getNombre()}'.", autor)
        ticket.agregarHito(hito)
        self.bd.guardarTicket(ticket)
        self.bd.guardarHito(ticket, hito)
        self.controladorNotificacion.notificar(
            ticket, ticket.contraparte(autor),
            f"El ticket #{ticket.id} pasó a '{e.getNombre()}'.")
        return ticket

    def registrarHito(self, id, contenido, autor):
        ticket = self.buscarTicket(id)
        self._verificarParticipante(ticket, autor)
        if not contenido.strip():
            raise ValueError("El hito no puede estar vacío.")
        hito = autor.registrarHito(ticket, contenido.strip())
        self.bd.guardarHito(ticket, hito)
        self.controladorNotificacion.notificar(
            ticket, ticket.contraparte(autor),
            f"Nuevo hito en el ticket #{ticket.id}: {hito.contenido}")
        return hito

    def notificacionesDe(self, usuario):
        return [n for t in self.tickets for n in t.notificaciones
                if n.getDestinatario() == usuario]

    def _verificarParticipante(self, ticket, usuario):
        if usuario != ticket.cliente and usuario != ticket.representante:
            raise PermisoDenegado("No participás de este ticket.")


class ControladorProducto:
    def __init__(self, bd, controladorTicket):
        self.bd = bd
        self.controladorTicket = controladorTicket

    @property
    def productos(self):
        return [t.getProducto() for t in self.controladorTicket.tickets]

    def solicitarTiposDisponibles(self):
        return list(TipoProducto)

    def buscarProducto(self, id):
        for p in self.productos:
            if p.id == id:
                return p
        return None

    def asignarTipo(self, idProd, tipo):
        producto = self.buscarProducto(idProd)
        if producto is None:
            raise ValueError(f"No existe el producto #{idProd}.")
        producto.setTipo(tipo)
        self.bd.actualizarProducto(producto)
        return producto
