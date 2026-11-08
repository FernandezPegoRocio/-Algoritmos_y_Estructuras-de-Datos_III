# TP Final Integrador · Sistema de Ticketing

Rocío Fernández Pego · Analista en Sistemas, 3.er año · ISFT N°151
Algoritmos y Estructuras de Datos III · Prof. Lic. José Luis Oemig

Los pasos para correrlo están en [EJECUCION.md](EJECUCION.md).

## La consigna

La consigna de esta etapa fue implementar en Python el código de las clases que veníamos
modelando, con persistencia en SQLite. La entrega es individual.

El sistema es una herramienta de atención al cliente para una empresa de
electrodomésticos. El cliente abre un ticket con su problema y el sistema se lo asigna a un
representante telefónico. Los dos conversan dentro del ticket con mensajes que llamamos
hitos, y cada vez que uno escribe o cambia algo, al otro le llega una notificación. El
ticket pasa por abierto, en proceso y cerrado, y se puede reabrir si el problema vuelve.
Desde el hito 4, cada ticket tiene un producto con su rubro (línea blanca, cocina, electro
o pequeños electrodomésticos) y cada representante atiende los rubros de su
especialidad.

## Cómo lo hice

El trabajo se fue armando por hitos durante el cuatrimestre. En el hito 1 escribí los
requerimientos y el diagrama de casos de uso. En el 2, las fichas de crear ticket,
registrar hito y cambiar estado. El 3 fue el primer diagrama de clases, y en el 4 llegó el
cambio del cliente con el producto y el tipo de producto. En el 5 hice los diagramas de
secuencia, y el 6 fue el cierre del diseño con las correcciones de clase.

Con el diseño cerrado, pasé el diagrama de clases a Python casi línea por línea, con tests
desde el principio, y después le sumé la persistencia en SQLite. La primera interfaz fue por
consola. Después hice la web con Flask, que es la versión principal, sin tocar ni el modelo
ni los controladores. Al final volví a los diagramas y los corregí para que dijeran lo
mismo que el código. Lo que cambié y por qué está en `diagramas-finales/CAMBIOS.md`.

## Cómo está armado

Respeta la separación del diagrama de clases: borde, control y entidad.

- **`ticketing/modelo.py`**: las entidades (Usuario, Cliente, RepresentanteTelefonico,
  Ticket, Hito, Notificacion, Producto) y los enums Estado y TipoProducto.
- **`ticketing/controladores.py`**: ControladorTicket, ControladorNotificacion,
  ControladorProducto y ControladorUsuario.
- **`ticketing/persistencia.py`**: la clase BaseDeDatos con las tablas de SQLite.
- **`ticketing/gui_web.py`**, **`templates/`** y **`static/`**: la GUI web con Flask.
- **`ticketing/gui.py`**: la GUI por consola.
- **`ticketing/datos.py`**: arma la base, los controladores y los usuarios de prueba.
- **`tests/`**: 53 pruebas que cubren el modelo, los controladores, la persistencia, la
  consola y la web.

## Memoria del proyecto

### Dónde estoy

La implementación está terminada y probada. Andan las dos interfaces sobre la misma base,
pasan los 53 tests y los diagramas están al día con el código. Lo último que hice
(8/11/2026) fue probar todo de punta a punta: registré un cliente, creé un ticket de un
microondas, vi que se le asignara al representante de electro, cambié estados, cerré y
reabrí el ticket, y comprobé que otro representante no pudiera verlo.

### Decisiones que tomé y por qué

Usé `sqlite3`, que viene con Python, y no SQLAlchemy. En la Unidad 6 perdí bastante tiempo
con versiones de librerías que no andaban con Python nuevo (SQLAlchemy 2.1.3 y
Marshmallow 4), y para este TP preferí tener una sola dependencia, Flask.

Dejé los métodos con los mismos nombres que en el UML, en camelCase, aunque en Python se
use otro estilo. 

Estado y TipoProducto son enums, como se corrigió en clase. Las transiciones válidas las
guarda Estado: de abierto a en proceso o a cerrado, de en proceso a cerrado, y de cerrado
solo se vuelve a abierto.

El representante se asigna solo, según el rubro del producto. Si hay más de uno, gana el
que tiene menos tickets abiertos, y si nadie atiende ese rubro (o el cliente no sabe el
tipo), se reparte entre todos con el mismo criterio.

El cliente puede cerrar y reabrir su ticket, pero pasarlo a en proceso lo hace solo el
representante. Cada cambio de estado deja un hito automático, para que en el historial
quede quién cambió qué y cuándo.

Apareció un ControladorUsuario que no estaba en el diagrama. Lo necesité para el login y
el registro; sin él, la GUI tendría que hablar directo con la base. Lo agregué al diagrama
final.

El login es solo con el email. Los requerimientos piden iniciar sesión pero no hablan de
contraseñas, y no quise agregar algo que no estaba pedido.

### Errores que resolví

El hito automático de "cerrado" no se guardaba. Al principio el control de "no se pueden
escribir hitos en un ticket cerrado" estaba dentro del Ticket, y bloqueaba también el hito
que deja el sistema al cerrarlo. Lo pasé al método registrarHito del usuario, que es donde
corresponde, porque la regla es para las personas y no para el sistema.

Al pasar a Flask tuve que abrir la conexión con `check_same_thread=False`. Flask atiende
cada pedido en otro hilo, y SQLite por defecto no deja usar una conexión desde un hilo
distinto del que la creó.

La base `ticketing.db` se creaba en la carpeta desde donde se ejecutaba el comando, así
que si lo corría desde otro lado aparecía una base nueva y vacía. Ahora se crea siempre al
lado de `app.py`.

En los diagramas del hito 6 encontré relaciones que no estaban conectadas a la clase de
origen, un método (`agregarNotificacion`) que se usaba en una secuencia pero no estaba en la
clase, y notificaciones unidas con «extend» cuando en las fichas siempre se notifica. Los
corregí todos en `diagramas-finales/`.

### Lo que queda pendiente


- Si hubiera una segunda versión, agregaría contraseñas al login y la posibilidad de
  adjuntar fotos del producto al ticket.
