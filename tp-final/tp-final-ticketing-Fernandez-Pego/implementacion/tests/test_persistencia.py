import os
import tempfile
import unittest

from ticketing.controladores import (ControladorNotificacion, ControladorProducto,
                                     ControladorTicket, ControladorUsuario)
from ticketing.modelo import Estado, RepresentanteTelefonico, TipoProducto
from ticketing.persistencia import BaseDeDatos


def armar(ruta):
    bd = BaseDeDatos(ruta)
    ctrl = ControladorTicket(bd, ControladorNotificacion(bd))
    return bd, ControladorUsuario(bd), ctrl, ControladorProducto(bd, ctrl)


class TestPersistencia(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.mkdtemp()
        self.ruta = os.path.join(carpeta, "prueba.db")

    def test_los_datos_sobreviven_al_reinicio(self):
        bd, usuarios, ctrl, productos = armar(self.ruta)
        laura = usuarios.registrarRepresentante("laura@s.com", "R-1", "Cocina",
                                                [TipoProducto.COCINA])
        ana = usuarios.registrarCliente("ana@mail.com", "Ana", "11")
        ticket = ctrl.crearTicket({"cliente": ana, "titulo": "Horno", "descripcion": "No prende",
                                   "producto": "Horno eléctrico", "tipo": None})
        ctrl.registrarHito(ticket.id, "Probé otro enchufe", ana)
        ctrl.cambiarEstado(ticket.id, Estado.EN_PROCESO, laura)
        productos.asignarTipo(ticket.getProducto().id, TipoProducto.COCINA)
        bd.cerrar()

        bd, usuarios, ctrl, _ = armar(self.ruta)
        recuperado = ctrl.buscarTicket(ticket.id)
        self.assertEqual(recuperado.titulo, "Horno")
        self.assertEqual(recuperado.estado, Estado.EN_PROCESO)
        self.assertEqual(recuperado.cliente, ana)
        self.assertEqual(recuperado.representante, laura)
        self.assertEqual(recuperado.getProducto().getTipo(), TipoProducto.COCINA)
        self.assertEqual([h.contenido for h in recuperado.hitos][0], "Probé otro enchufe")
        self.assertEqual(len(recuperado.hitos), 2)
        self.assertEqual(len(recuperado.notificaciones), 3)
        bd.cerrar()

    def test_el_representante_recupera_sus_rubros(self):
        bd, usuarios, _, _ = armar(self.ruta)
        usuarios.registrarRepresentante("m@s.com", "R-2", "Electro",
                                        [TipoProducto.ELECTRO, TipoProducto.PEQUENOS_ELECTRODOMESTICOS])
        rep = bd.buscarUsuarioPorEmail("m@s.com")
        self.assertIsInstance(rep, RepresentanteTelefonico)
        self.assertEqual(rep.tiposProducto,
                         [TipoProducto.ELECTRO, TipoProducto.PEQUENOS_ELECTRODOMESTICOS])
        bd.cerrar()

    def test_los_tipos_de_producto_quedan_cargados(self):
        bd = BaseDeDatos(self.ruta)
        filas = bd.conexion.execute("SELECT rubro FROM tipo_producto ORDER BY id").fetchall()
        self.assertEqual([f["rubro"] for f in filas],
                         ["línea blanca", "cocina", "electro", "pequeños electrodomésticos"])
        bd.cerrar()


if __name__ == "__main__":
    unittest.main()
