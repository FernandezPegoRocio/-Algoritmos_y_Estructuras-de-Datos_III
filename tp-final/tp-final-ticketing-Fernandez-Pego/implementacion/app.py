import os

from ticketing.gui_web import crearApp

RUTA_BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticketing.db")

app = crearApp(RUTA_BD)

if __name__ == "__main__":
    app.run(port=5000)
