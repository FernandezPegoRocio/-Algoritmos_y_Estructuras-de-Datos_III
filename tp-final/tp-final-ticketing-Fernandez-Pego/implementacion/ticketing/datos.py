from .controladores import (ControladorNotificacion, ControladorProducto,
                            ControladorTicket, ControladorUsuario)
from .modelo import TipoProducto
from .persistencia import BaseDeDatos


def cargarDatosIniciales(ctrlUsuario):
    if ctrlUsuario.listarUsuarios():
        return
    ctrlUsuario.registrarRepresentante(
        "laura@soporte.com", "R-001", "Línea blanca y cocina",
        [TipoProducto.LINEA_BLANCA, TipoProducto.COCINA])
    ctrlUsuario.registrarRepresentante(
        "martin@soporte.com", "R-002", "Electro",
        [TipoProducto.ELECTRO, TipoProducto.PEQUENOS_ELECTRODOMESTICOS])
    ctrlUsuario.registrarCliente("ana@mail.com", "Ana Gómez", "11-5555-1234")


def armarSistema(ruta="ticketing.db", datosIniciales=True):
    bd = BaseDeDatos(ruta)
    ctrlUsuario = ControladorUsuario(bd)
    if datosIniciales:
        cargarDatosIniciales(ctrlUsuario)
    ctrlTicket = ControladorTicket(bd, ControladorNotificacion(bd))
    ctrlProducto = ControladorProducto(bd, ctrlTicket)
    return bd, ctrlUsuario, ctrlTicket, ctrlProducto
