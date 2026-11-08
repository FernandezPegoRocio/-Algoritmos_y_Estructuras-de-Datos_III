import os
from functools import wraps

from flask import Flask, flash, g, redirect, render_template, request, session, url_for

from .controladores import PermisoDenegado, TicketNoEncontrado
from .datos import armarSistema
from .modelo import Cliente, Estado, TicketCerrado, TransicionInvalida
from .persistencia import UsuarioDuplicado

ERRORES = (PermisoDenegado, TicketNoEncontrado, TicketCerrado,
           TransicionInvalida, UsuarioDuplicado, ValueError)


def crearApp(ruta="ticketing.db", datosIniciales=True):
    app = Flask(__name__)
    app.secret_key = os.environ.get("TICKETING_SECRET", "tp-final-algoritmos-iii")
    bd, ctrlUsuario, ctrlTicket, ctrlProducto = armarSistema(ruta, datosIniciales)
    app.config["BD"] = bd

    @app.before_request
    def cargarUsuario():
        email = session.get("email")
        g.usuario = ctrlUsuario.buscarUsuario(email) if email else None

    @app.context_processor
    def datosComunes():
        usuario = g.get("usuario")
        pendientes = len(ctrlTicket.notificacionesDe(usuario)) if usuario else 0
        return {"usuario": usuario, "esCliente": isinstance(usuario, Cliente),
                "cantNotificaciones": pendientes}

    def requiereLogin(vista):
        @wraps(vista)
        def envoltura(*args, **kwargs):
            if g.usuario is None:
                flash("Iniciá sesión para continuar.", "error")
                return redirect(url_for("login"))
            try:
                return vista(*args, **kwargs)
            except ERRORES as error:
                flash(str(error), "error")
                return redirect(request.referrer or url_for("mostrarTickets"))
        return envoltura

    def mostrarConfirmacion(msg):
        flash(msg, "ok")

    @app.route("/", methods=["GET", "POST"])
    def login():
        if g.usuario:
            return redirect(url_for("mostrarTickets"))
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            if ctrlUsuario.login(email):
                session["email"] = email
                mostrarConfirmacion(f"Hola, {ctrlUsuario.usuarioActual}")
                return redirect(url_for("mostrarTickets"))
            flash("No existe un usuario con ese email.", "error")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/registro", methods=["GET", "POST"])
    def mostrarRegistro():
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            nombre = request.form.get("nombre", "").strip()
            telefono = request.form.get("telefono", "").strip()
            try:
                if not (email and nombre):
                    raise ValueError("Email y nombre son obligatorios.")
                ctrlUsuario.registrarCliente(email, nombre, telefono)
            except ERRORES as error:
                flash(str(error), "error")
                return render_template("registro.html", form=request.form)
            mostrarConfirmacion("Cliente registrado. Ya podés iniciar sesión.")
            return redirect(url_for("login"))
        return render_template("registro.html", form={})

    @app.route("/tickets")
    @requiereLogin
    def mostrarTickets():
        tickets = ctrlTicket.listarTickets(g.usuario)
        return render_template("tickets.html", tickets=sorted(tickets, key=lambda t: -t.id))

    @app.route("/tickets/nuevo", methods=["GET", "POST"])
    @requiereLogin
    def mostrarFormularioNuevoTicket():
        tipos = ctrlProducto.solicitarTiposDisponibles()
        if request.method == "POST":
            f = request.form
            if not (f.get("titulo", "").strip() and f.get("descripcion", "").strip()
                    and f.get("producto", "").strip()):
                flash("Título, descripción y producto son obligatorios.", "error")
                return render_template("nuevo_ticket.html", tipos=tipos, form=f)
            tipo = next((t for t in tipos if t.name == f.get("tipo")), None)
            ticket = ctrlTicket.crearTicket({
                "cliente": g.usuario, "titulo": f["titulo"].strip(),
                "descripcion": f["descripcion"].strip(),
                "producto": f["producto"].strip(), "tipo": tipo})
            rep = ticket.representante.legajo if ticket.representante else "sin asignar"
            mostrarConfirmacion(f"Ticket #{ticket.id} creado. Representante: {rep}")
            return redirect(url_for("mostrarDetalleTicket", id=ticket.id))
        return render_template("nuevo_ticket.html", tipos=tipos, form={})

    @app.route("/tickets/<int:id>")
    @requiereLogin
    def mostrarDetalleTicket(id):
        ticket = ctrlTicket.buscarTicket(id)
        if g.usuario != ticket.cliente and g.usuario != ticket.representante:
            raise PermisoDenegado("No participás de este ticket.")
        estados = ctrlTicket.solicitarEstadosValidos(id)
        if isinstance(g.usuario, Cliente):
            estados = [e for e in estados if e != Estado.EN_PROCESO]
        return render_template("detalle.html", t=ticket, estados=estados,
                               tipos=ctrlProducto.solicitarTiposDisponibles())

    @app.route("/tickets/<int:id>/hitos", methods=["POST"])
    @requiereLogin
    def mostrarFormularioHito(id):
        ctrlTicket.registrarHito(id, request.form.get("contenido", ""), g.usuario)
        mostrarConfirmacion("Hito registrado")
        return redirect(url_for("mostrarDetalleTicket", id=id))

    @app.route("/tickets/<int:id>/estado", methods=["POST"])
    @requiereLogin
    def mostrarFormularioCambioEstado(id):
        nombre = request.form.get("estado")
        estado = next((e for e in Estado if e.name == nombre), None)
        if estado is None:
            raise ValueError("Elegí un estado válido.")
        ctrlTicket.cambiarEstado(id, estado, g.usuario)
        mostrarConfirmacion("Estado actualizado")
        return redirect(url_for("mostrarDetalleTicket", id=id))

    @app.route("/tickets/<int:id>/tipo", methods=["POST"])
    @requiereLogin
    def mostrarAsignarTipo(id):
        ticket = ctrlTicket.buscarTicket(id)
        if g.usuario != ticket.representante:
            raise PermisoDenegado("Solo el representante del ticket puede asignar el tipo.")
        tipo = next((t for t in ctrlProducto.solicitarTiposDisponibles()
                     if t.name == request.form.get("tipo")), None)
        if tipo is None:
            raise ValueError("Elegí un tipo de producto.")
        ctrlProducto.asignarTipo(ticket.getProducto().id, tipo)
        mostrarConfirmacion(f"Producto marcado como {tipo.getRubro()}")
        return redirect(url_for("mostrarDetalleTicket", id=id))

    @app.route("/notificaciones")
    @requiereLogin
    def mostrarNotificaciones():
        notificaciones = sorted(ctrlTicket.notificacionesDe(g.usuario),
                                key=lambda n: n.fecha, reverse=True)
        return render_template("notificaciones.html", notificaciones=notificaciones)

    @app.route("/usuarios")
    @requiereLogin
    def mostrarUsuarios():
        if isinstance(g.usuario, Cliente):
            raise PermisoDenegado("Solo los representantes pueden ver los usuarios.")
        return render_template("usuarios.html", usuarios=ctrlUsuario.listarUsuarios(),
                               representantes=ctrlUsuario.listarRepresentantes())

    return app
