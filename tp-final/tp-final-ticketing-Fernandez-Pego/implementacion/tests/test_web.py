import os
import tempfile
import unittest

try:
    import flask
except ImportError:
    raise unittest.SkipTest("Flask no está instalado (pip install -r requirements.txt)")

from ticketing.gui_web import crearApp


class TestWeb(unittest.TestCase):
    def setUp(self):
        self.ruta = os.path.join(tempfile.mkdtemp(), "web.db")
        self.app = crearApp(self.ruta)
        self.app.config["TESTING"] = True
        self.web = self.app.test_client()

    def tearDown(self):
        self.app.config["BD"].cerrar()

    def entrar(self, email):
        self.web.get("/logout")
        return self.web.post("/", data={"email": email}, follow_redirects=True)

    def crearTicket(self, tipo="LINEA_BLANCA"):
        self.entrar("ana@mail.com")
        return self.web.post("/tickets/nuevo", data={
            "titulo": "No enfría", "descripcion": "Dejó de enfriar ayer",
            "producto": "Heladera Patrick", "tipo": tipo}, follow_redirects=True)

    def texto(self, respuesta):
        return respuesta.get_data(as_text=True)

    def test_sin_sesion_redirige_al_login(self):
        r = self.web.get("/tickets", follow_redirects=True)
        self.assertIn("Iniciá sesión para continuar.", self.texto(r))

    def test_login_incorrecto(self):
        r = self.entrar("nadie@mail.com")
        self.assertIn("No existe un usuario con ese email.", self.texto(r))

    def test_registro_y_duplicado(self):
        datos = {"email": "beto@mail.com", "nombre": "Beto", "telefono": "11"}
        r = self.web.post("/registro", data=datos, follow_redirects=True)
        self.assertIn("Cliente registrado", self.texto(r))
        r = self.web.post("/registro", data=datos, follow_redirects=True)
        self.assertIn("Ya existe un usuario con el email beto@mail.com", self.texto(r))

    def test_cliente_crea_ticket_y_se_asigna_por_rubro(self):
        r = self.crearTicket("LINEA_BLANCA")
        html = self.texto(r)
        self.assertIn("Ticket #1 creado. Representante: R-001", html)
        self.assertIn("Heladera Patrick (línea blanca)", html)

    def test_campos_obligatorios(self):
        self.entrar("ana@mail.com")
        r = self.web.post("/tickets/nuevo", data={"titulo": "", "descripcion": "x", "producto": "y"})
        self.assertIn("obligatorios", self.texto(r))

    def test_representante_atiende_y_cliente_recibe_notificaciones(self):
        self.crearTicket()
        self.entrar("laura@soporte.com")
        r = self.web.post("/tickets/1/estado", data={"estado": "EN_PROCESO"}, follow_redirects=True)
        self.assertIn("Estado actualizado", self.texto(r))
        r = self.web.post("/tickets/1/hitos", data={"contenido": "Paso el jueves"}, follow_redirects=True)
        self.assertIn("Paso el jueves", self.texto(r))

        self.entrar("ana@mail.com")
        html = self.texto(self.web.get("/notificaciones"))
        self.assertIn("pasó a &#39;en proceso&#39;", html)
        self.assertIn("Nuevo hito en el ticket #1: Paso el jueves", html)

    def test_cliente_no_puede_pasar_a_en_proceso(self):
        self.crearTicket()
        r = self.web.post("/tickets/1/estado", data={"estado": "EN_PROCESO"}, follow_redirects=True)
        self.assertIn("Solo el representante", self.texto(r))

    def test_otro_representante_no_ve_el_ticket(self):
        self.crearTicket("LINEA_BLANCA")
        self.entrar("martin@soporte.com")
        r = self.web.get("/tickets/1", follow_redirects=True)
        self.assertIn("No participás de este ticket.", self.texto(r))

    def test_asignar_tipo_de_producto(self):
        self.crearTicket(tipo="")
        self.entrar("laura@soporte.com")
        r = self.web.post("/tickets/1/tipo", data={"tipo": "COCINA"}, follow_redirects=True)
        self.assertIn("Producto marcado como cocina", self.texto(r))

    def test_hito_en_ticket_cerrado(self):
        self.crearTicket()
        self.web.post("/tickets/1/estado", data={"estado": "CERRADO"})
        r = self.web.post("/tickets/1/hitos", data={"contenido": "Hola"}, follow_redirects=True)
        self.assertIn("El ticket está cerrado", self.texto(r))


if __name__ == "__main__":
    unittest.main()
