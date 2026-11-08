import unittest

from ticketing.controladores import (ControladorNotificacion, ControladorProducto,
                                     ControladorTicket, ControladorUsuario,
                                     PermisoDenegado, TicketNoEncontrado)
from ticketing.modelo import Estado, TipoProducto
from ticketing.persistencia import BaseDeDatos, UsuarioDuplicado


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.bd = BaseDeDatos(":memory:")
        self.usuarios = ControladorUsuario(self.bd)
        self.laura = self.usuarios.registrarRepresentante(
            "laura@soporte.com", "R-001", "Línea blanca",
            [TipoProducto.LINEA_BLANCA, TipoProducto.COCINA])
        self.martin = self.usuarios.registrarRepresentante(
            "martin@soporte.com", "R-002", "Electro", [TipoProducto.ELECTRO])
        self.ana = self.usuarios.registrarCliente("ana@mail.com", "Ana", "1155551234")
        self.notif = ControladorNotificacion(self.bd)
        self.ctrl = ControladorTicket(self.bd, self.notif)
        self.productos = ControladorProducto(self.bd, self.ctrl)

    def tearDown(self):
        self.bd.cerrar()

    def crear(self, tipo=TipoProducto.LINEA_BLANCA, cliente=None):
        return self.ctrl.crearTicket({
            "cliente": cliente or self.ana, "titulo": "No enfría",
            "descripcion": "La heladera dejó de enfriar", "producto": "Heladera", "tipo": tipo})


class TestUsuarios(BaseTest):
    def test_no_se_duplican_usuarios(self):
        with self.assertRaises(UsuarioDuplicado):
            self.usuarios.registrarCliente("ana@mail.com", "Otra Ana", "")

    def test_login_con_email_existente(self):
        self.assertTrue(self.usuarios.login("ana@mail.com"))
        self.assertEqual(self.usuarios.usuarioActual, self.ana)

    def test_login_con_email_inexistente(self):
        self.assertFalse(self.usuarios.login("nadie@mail.com"))
        self.assertIsNone(self.usuarios.usuarioActual)

    def test_listar_representantes(self):
        self.assertEqual(self.usuarios.listarRepresentantes(), [self.laura, self.martin])


class TestCrearTicket(BaseTest):
    def test_crea_el_ticket_abierto_y_con_id(self):
        ticket = self.crear()
        self.assertIsNotNone(ticket.id)
        self.assertEqual(ticket.estado, Estado.ABIERTO)
        self.assertEqual(ticket.cliente, self.ana)

    def test_asigna_representante_por_rubro(self):
        self.assertEqual(self.crear(TipoProducto.LINEA_BLANCA).representante, self.laura)
        self.assertEqual(self.crear(TipoProducto.ELECTRO).representante, self.martin)

    def test_sin_tipo_reparte_por_menor_carga(self):
        self.crear(TipoProducto.LINEA_BLANCA)
        self.assertEqual(self.crear(tipo=None).representante, self.martin)

    def test_notifica_al_representante(self):
        ticket = self.crear()
        notificaciones = self.ctrl.notificacionesDe(self.laura)
        self.assertEqual(len(notificaciones), 1)
        self.assertIn(f"#{ticket.id}", notificaciones[0].mensaje)
        self.assertTrue(notificaciones[0].enviada)

    def test_un_representante_no_crea_tickets(self):
        with self.assertRaises(PermisoDenegado):
            self.crear(cliente=self.laura)


class TestRegistrarHito(BaseTest):
    def test_hito_del_cliente_notifica_al_representante(self):
        ticket = self.crear()
        self.ctrl.registrarHito(ticket.id, "Sigue sin enfriar", self.ana)
        mensajes = [n.mensaje for n in self.ctrl.notificacionesDe(self.laura)]
        self.assertTrue(any("Sigue sin enfriar" in m for m in mensajes))

    def test_hito_del_representante_notifica_al_cliente(self):
        ticket = self.crear()
        self.ctrl.registrarHito(ticket.id, "Mañana pasa el técnico", self.laura)
        self.assertEqual(len(self.ctrl.notificacionesDe(self.ana)), 1)

    def test_alguien_ajeno_no_puede_escribir(self):
        ticket = self.crear()
        with self.assertRaises(PermisoDenegado):
            self.ctrl.registrarHito(ticket.id, "Hola", self.martin)

    def test_hito_vacio(self):
        ticket = self.crear()
        with self.assertRaises(ValueError):
            self.ctrl.registrarHito(ticket.id, "   ", self.ana)

    def test_ticket_inexistente(self):
        with self.assertRaises(TicketNoEncontrado):
            self.ctrl.registrarHito(999, "Hola", self.ana)


class TestCambiarEstado(BaseTest):
    def test_el_representante_lo_pasa_a_en_proceso(self):
        ticket = self.crear()
        self.ctrl.cambiarEstado(ticket.id, Estado.EN_PROCESO, self.laura)
        self.assertEqual(ticket.estado, Estado.EN_PROCESO)

    def test_deja_un_hito_automatico_y_notifica_al_cliente(self):
        ticket = self.crear()
        self.ctrl.cambiarEstado(ticket.id, Estado.EN_PROCESO, self.laura)
        self.assertIn("en proceso", ticket.hitos[-1].contenido)
        self.assertEqual(len(self.ctrl.notificacionesDe(self.ana)), 1)

    def test_el_cliente_puede_cerrar_y_reabrir(self):
        ticket = self.crear()
        self.ctrl.cambiarEstado(ticket.id, Estado.CERRADO, self.ana)
        self.ctrl.cambiarEstado(ticket.id, Estado.ABIERTO, self.ana)
        self.assertEqual(ticket.estado, Estado.ABIERTO)

    def test_el_cliente_no_lo_pasa_a_en_proceso(self):
        ticket = self.crear()
        with self.assertRaises(PermisoDenegado):
            self.ctrl.cambiarEstado(ticket.id, Estado.EN_PROCESO, self.ana)

    def test_estados_validos(self):
        ticket = self.crear()
        self.assertEqual(self.ctrl.solicitarEstadosValidos(ticket.id),
                         [Estado.EN_PROCESO, Estado.CERRADO])


class TestListarYProducto(BaseTest):
    def test_cada_uno_ve_sus_tickets(self):
        t1 = self.crear(TipoProducto.LINEA_BLANCA)
        t2 = self.crear(TipoProducto.ELECTRO)
        self.assertEqual(self.ctrl.listarTickets(self.ana), [t1, t2])
        self.assertEqual(self.ctrl.listarTickets(self.laura), [t1])
        self.assertEqual(self.ctrl.listarTickets(self.martin), [t2])

    def test_asignar_tipo_al_producto(self):
        ticket = self.crear(tipo=None)
        self.productos.asignarTipo(ticket.getProducto().id, TipoProducto.COCINA)
        self.assertEqual(ticket.getProducto().getTipo(), TipoProducto.COCINA)

    def test_tipos_disponibles(self):
        self.assertEqual(len(self.productos.solicitarTiposDisponibles()), 4)


if __name__ == "__main__":
    unittest.main()
