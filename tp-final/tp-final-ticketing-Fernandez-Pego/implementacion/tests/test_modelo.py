import unittest

from ticketing.modelo import (Cliente, Estado, Producto, RepresentanteTelefonico,
                              TicketCerrado, TipoProducto, TransicionInvalida)


def armarTicket():
    cliente = Cliente("ana@mail.com", "Ana", "1155551234", id=1)
    producto = Producto("Heladera Patrick", TipoProducto.LINEA_BLANCA)
    return cliente, cliente.crearTicket("No enfría", "Dejó de enfriar ayer", producto)


class TestEstado(unittest.TestCase):
    def test_un_ticket_nuevo_arranca_abierto(self):
        _, ticket = armarTicket()
        self.assertEqual(ticket.estado, Estado.ABIERTO)

    def test_transiciones_validas_desde_abierto(self):
        self.assertEqual(Estado.ABIERTO.getTransicionesValidas(),
                         [Estado.EN_PROCESO, Estado.CERRADO])

    def test_cerrado_solo_puede_reabrirse(self):
        self.assertEqual(Estado.CERRADO.getTransicionesValidas(), [Estado.ABIERTO])

    def test_transicion_invalida_lanza_error(self):
        with self.assertRaises(TransicionInvalida):
            Estado.EN_PROCESO.transicion(Estado.ABIERTO)

    def test_get_nombre(self):
        self.assertEqual(Estado.EN_PROCESO.getNombre(), "en proceso")


class TestTicket(unittest.TestCase):
    def test_cerrar_y_reabrir(self):
        _, ticket = armarTicket()
        ticket.cerrar()
        self.assertEqual(ticket.estado, Estado.CERRADO)
        ticket.reabrir()
        self.assertEqual(ticket.estado, Estado.ABIERTO)

    def test_no_se_reabre_un_ticket_abierto(self):
        _, ticket = armarTicket()
        with self.assertRaises(TransicionInvalida):
            ticket.reabrir()

    def test_el_cliente_registra_un_hito(self):
        cliente, ticket = armarTicket()
        hito = cliente.registrarHito(ticket, "Hace ruido raro")
        self.assertEqual(ticket.hitos, [hito])
        self.assertEqual(hito.autor, cliente)

    def test_no_se_registran_hitos_en_un_ticket_cerrado(self):
        cliente, ticket = armarTicket()
        ticket.cerrar()
        with self.assertRaises(TicketCerrado):
            cliente.registrarHito(ticket, "¿Hola?")

    def test_get_producto_y_tipo(self):
        _, ticket = armarTicket()
        self.assertEqual(ticket.getProducto().getTipo(), TipoProducto.LINEA_BLANCA)

    def test_contraparte(self):
        cliente, ticket = armarTicket()
        rep = RepresentanteTelefonico("laura@soporte.com", "R-001", "Línea blanca", id=2)
        ticket.representante = rep
        self.assertEqual(ticket.contraparte(cliente), rep)
        self.assertEqual(ticket.contraparte(rep), cliente)


class TestUsuarios(unittest.TestCase):
    def test_login_y_logout(self):
        cliente = Cliente("ana@mail.com", "Ana", "1155551234")
        self.assertFalse(cliente.login("otro@mail.com"))
        self.assertTrue(cliente.login("ana@mail.com"))
        cliente.logout()
        self.assertFalse(cliente.conectado)

    def test_representante_atiende_sus_rubros(self):
        rep = RepresentanteTelefonico("m@s.com", "R-2", "Electro", [TipoProducto.ELECTRO])
        self.assertTrue(rep.atiende(TipoProducto.ELECTRO))
        self.assertFalse(rep.atiende(TipoProducto.COCINA))

    def test_representante_lista_solo_sus_tickets(self):
        _, t1 = armarTicket()
        _, t2 = armarTicket()
        rep = RepresentanteTelefonico("m@s.com", "R-2", "Electro")
        t1.representante = rep
        self.assertEqual(rep.listarTickets([t1, t2]), [t1])


class TestTipoProducto(unittest.TestCase):
    def test_rubros_validos(self):
        self.assertTrue(TipoProducto.esValido("cocina"))
        self.assertFalse(TipoProducto.esValido("jardinería"))

    def test_desde_id(self):
        self.assertEqual(TipoProducto.desdeId(3), TipoProducto.ELECTRO)
        self.assertIsNone(TipoProducto.desdeId(99))


if __name__ == "__main__":
    unittest.main()
