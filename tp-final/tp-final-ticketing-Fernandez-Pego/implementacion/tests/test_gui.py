import unittest

from ticketing.controladores import (ControladorNotificacion, ControladorProducto,
                                     ControladorTicket, ControladorUsuario)
from ticketing.gui import GUI
from ticketing.modelo import Estado, TipoProducto
from ticketing.persistencia import BaseDeDatos


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.bd = BaseDeDatos(":memory:")
        self.usuarios = ControladorUsuario(self.bd)
        self.usuarios.registrarRepresentante("laura@s.com", "R-1", "Línea blanca",
                                             [TipoProducto.LINEA_BLANCA])
        self.usuarios.registrarCliente("ana@mail.com", "Ana", "11")
        self.ctrl = ControladorTicket(self.bd, ControladorNotificacion(self.bd))
        self.salida = []

    def tearDown(self):
        self.bd.cerrar()

    def correr(self, teclas):
        teclas = iter(teclas)
        gui = GUI(self.usuarios, self.ctrl, ControladorProducto(self.bd, self.ctrl),
                  entrada=lambda _: next(teclas), salida=self.salida.append)
        gui.ejecutar()

    def test_cliente_crea_ticket_y_representante_lo_atiende(self):
        self.correr([
            "1", "ana@mail.com",
            "6", "No enfría", "Dejó de enfriar", "Heladera", "1",
            "7",
            "1", "laura@s.com",
            "4", "1", "1",
            "3", "1", "Paso el jueves",
            "9",
            "3",
        ])
        ticket = self.ctrl.buscarTicket(1)
        self.assertEqual(ticket.estado, Estado.EN_PROCESO)
        self.assertEqual(ticket.hitos[-1].contenido, "Paso el jueves")
        self.assertIn("✔ Ticket #1 creado. Representante: R-1", self.salida)

    def test_los_errores_se_muestran_sin_cortar_el_programa(self):
        self.correr(["1", "ana@mail.com", "2", "99", "7", "3"])
        self.assertIn("✘ No existe el ticket #99.", self.salida)
        self.assertEqual(self.salida[-1], "Hasta luego.")


if __name__ == "__main__":
    unittest.main()
