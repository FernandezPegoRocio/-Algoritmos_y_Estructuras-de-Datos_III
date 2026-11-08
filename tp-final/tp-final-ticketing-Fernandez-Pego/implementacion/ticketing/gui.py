from .controladores import PermisoDenegado, TicketNoEncontrado
from .modelo import Cliente, TicketCerrado, TransicionInvalida
from .persistencia import UsuarioDuplicado

ERRORES = (PermisoDenegado, TicketNoEncontrado, TicketCerrado,
           TransicionInvalida, UsuarioDuplicado, ValueError)


class GUI:
    def __init__(self, ctrlUsuario, ctrlTicket, ctrlProducto, entrada=input, salida=print):
        self.ctrlUsuario = ctrlUsuario
        self.ctrlTicket = ctrlTicket
        self.ctrlProducto = ctrlProducto
        self.entrada = entrada
        self.salida = salida

    def preguntar(self, texto):
        return self.entrada(f"{texto}: ").strip()

    def elegir(self, titulo, opciones):
        self.salida(titulo)
        for i, op in enumerate(opciones, 1):
            self.salida(f"  {i}. {op}")
        respuesta = self.preguntar("Opción")
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(opciones):
            return opciones[int(respuesta) - 1]
        return None

    def pedirIdTicket(self):
        respuesta = self.preguntar("Número de ticket")
        if not respuesta.isdigit():
            raise ValueError("El número de ticket tiene que ser un entero.")
        return int(respuesta)

    def mostrarFormularioNuevoTicket(self):
        titulo = self.preguntar("Título")
        descripcion = self.preguntar("Descripción del problema")
        producto = self.preguntar("Producto (ej.: Heladera Patrick 300 L)")
        if not (titulo and descripcion and producto):
            raise ValueError("Título, descripción y producto son obligatorios.")
        tipos = self.ctrlProducto.solicitarTiposDisponibles()
        tipo = self.elegir("Tipo de producto (Enter si no sabés):", [t.getRubro() for t in tipos])
        tipo = next((t for t in tipos if t.getRubro() == tipo), None)
        ticket = self.ctrlTicket.crearTicket({
            "cliente": self.ctrlUsuario.usuarioActual, "titulo": titulo,
            "descripcion": descripcion, "producto": producto, "tipo": tipo})
        rep = ticket.representante.legajo if ticket.representante else "sin asignar"
        self.mostrarConfirmacion(f"Ticket #{ticket.id} creado. Representante: {rep}")

    def mostrarDetalleTicket(self, id):
        t = self.ctrlTicket.buscarTicket(id)
        self.salida(f"\n=== Ticket #{t.id} · {t.titulo} [{t.estado.getNombre()}] ===")
        self.salida(f"Cliente: {t.cliente}")
        self.salida(f"Representante: {t.representante or 'sin asignar'}")
        self.salida(f"Producto: {t.getProducto()}")
        self.salida(f"Descripción: {t.descripcion}")
        self.salida("Hitos:")
        for h in t.hitos or []:
            self.salida(f"  [{h.fecha:%d/%m/%Y %H:%M}] {h.autor.email}: {h.contenido}")
        if not t.hitos:
            self.salida("  (todavía no hay hitos)")

    def mostrarFormularioHito(self, id):
        contenido = self.preguntar("Escribí el hito")
        self.ctrlTicket.registrarHito(id, contenido, self.ctrlUsuario.usuarioActual)
        self.mostrarConfirmacion("Hito registrado")

    def mostrarConfirmacion(self, msg):
        self.salida(f"✔ {msg}")

    def mostrarFormularioCambioEstado(self, id):
        estados = self.ctrlTicket.solicitarEstadosValidos(id)
        nombre = self.elegir("Estados posibles:", [e.getNombre() for e in estados])
        estado = next((e for e in estados if e.getNombre() == nombre), None)
        if estado is None:
            raise ValueError("Opción inválida.")
        self.ctrlTicket.cambiarEstado(id, estado, self.ctrlUsuario.usuarioActual)
        self.mostrarConfirmacion("Estado actualizado")

    def mostrarAsignarTipo(self, id):
        ticket = self.ctrlTicket.buscarTicket(id)
        tipos = self.ctrlProducto.solicitarTiposDisponibles()
        rubro = self.elegir("Tipo de producto:", [t.getRubro() for t in tipos])
        tipo = next((t for t in tipos if t.getRubro() == rubro), None)
        if tipo is None:
            raise ValueError("Opción inválida.")
        self.ctrlProducto.asignarTipo(ticket.getProducto().id, tipo)
        self.mostrarConfirmacion(f"Producto marcado como {tipo.getRubro()}")

    def mostrarTickets(self):
        tickets = self.ctrlTicket.listarTickets(self.ctrlUsuario.usuarioActual)
        if not tickets:
            self.salida("No tenés tickets.")
        for t in tickets:
            self.salida(f"  #{t.id} [{t.estado.getNombre()}] {t.titulo} · {t.getProducto()}")

    def mostrarNotificaciones(self):
        notificaciones = self.ctrlTicket.notificacionesDe(self.ctrlUsuario.usuarioActual)
        if not notificaciones:
            self.salida("No tenés notificaciones.")
        for n in notificaciones:
            self.salida(f"  [{n.fecha:%d/%m/%Y %H:%M}] {n.mensaje}")

    def mostrarRegistro(self):
        email = self.preguntar("Email")
        nombre = self.preguntar("Nombre")
        telefono = self.preguntar("Teléfono")
        if not (email and nombre):
            raise ValueError("Email y nombre son obligatorios.")
        self.ctrlUsuario.registrarCliente(email, nombre, telefono)
        self.mostrarConfirmacion("Cliente registrado. Ya podés iniciar sesión.")

    def ejecutar(self):
        self.salida("=== Sistema de Ticketing ===")
        while True:
            try:
                if self.ctrlUsuario.usuarioActual is None:
                    if not self.menuInicio():
                        break
                else:
                    self.menuPrincipal()
            except ERRORES as error:
                self.salida(f"✘ {error}")
            except (EOFError, KeyboardInterrupt):
                break
        self.salida("Hasta luego.")

    def menuInicio(self):
        opcion = self.elegir("\n¿Qué querés hacer?", ["Iniciar sesión", "Registrarme como cliente", "Salir"])
        if opcion == "Iniciar sesión":
            if self.ctrlUsuario.login(self.preguntar("Email")):
                self.mostrarConfirmacion(f"Hola, {self.ctrlUsuario.usuarioActual}")
            else:
                self.salida("✘ No existe un usuario con ese email.")
        elif opcion == "Registrarme como cliente":
            self.mostrarRegistro()
        elif opcion == "Salir":
            return False
        return True

    def menuPrincipal(self):
        esCliente = isinstance(self.ctrlUsuario.usuarioActual, Cliente)
        opciones = ["Mis tickets", "Ver detalle de un ticket", "Registrar hito",
                    "Cambiar estado", "Mis notificaciones"]
        opciones += ["Crear ticket"] if esCliente else [
            "Asignar tipo de producto", "Listar usuarios", "Listar representantes"]
        opciones += ["Cerrar sesión"]
        opcion = self.elegir("\nMenú", opciones)

        if opcion == "Mis tickets":
            self.mostrarTickets()
        elif opcion == "Ver detalle de un ticket":
            self.mostrarDetalleTicket(self.pedirIdTicket())
        elif opcion == "Registrar hito":
            self.mostrarFormularioHito(self.pedirIdTicket())
        elif opcion == "Cambiar estado":
            self.mostrarFormularioCambioEstado(self.pedirIdTicket())
        elif opcion == "Mis notificaciones":
            self.mostrarNotificaciones()
        elif opcion == "Crear ticket":
            self.mostrarFormularioNuevoTicket()
        elif opcion == "Asignar tipo de producto":
            self.mostrarAsignarTipo(self.pedirIdTicket())
        elif opcion == "Listar usuarios":
            for u in self.ctrlUsuario.listarUsuarios():
                self.salida(f"  {u}")
        elif opcion == "Listar representantes":
            for r in self.ctrlUsuario.listarRepresentantes():
                rubros = ", ".join(t.getRubro() for t in r.tiposProducto)
                self.salida(f"  {r} · atiende: {rubros}")
        elif opcion == "Cerrar sesión":
            self.ctrlUsuario.logout()
