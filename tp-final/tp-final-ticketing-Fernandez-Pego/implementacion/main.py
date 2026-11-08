import os

from ticketing.datos import armarSistema
from ticketing.gui import GUI

RUTA_BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticketing.db")


def main():
    bd, ctrlUsuario, ctrlTicket, ctrlProducto = armarSistema(RUTA_BD)
    try:
        GUI(ctrlUsuario, ctrlTicket, ctrlProducto).ejecutar()
    finally:
        bd.cerrar()


if __name__ == "__main__":
    main()
