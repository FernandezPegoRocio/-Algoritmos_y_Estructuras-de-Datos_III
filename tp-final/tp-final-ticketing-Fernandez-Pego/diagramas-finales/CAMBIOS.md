# Qué cambió en los diagramas y por qué

Revisé los hitos 1 a 6 contra la consigna, contra las correcciones que dio el profe en clase
y contra el código implementado. Esta carpeta tiene la versión final de todo. Los archivos
originales de cada hito no se tocaron: siguen en el repo tal como se entregaron.

Los .drawio se abren y se editan en draw.io. En `png/` están las mismas imágenes para ver
rápido o imprimir.

## Diagrama de clases (diagramaClases.drawio)

**Errores que tenía el del hito 6**

Había tres relaciones sueltas: Representante con Ticket, Ticket con Hito y Ticket con
Producto. Se veían bien en pantalla, pero la línea no estaba enganchada a la clase de origen,
así que al mover una caja la flecha quedaba colgando. Ahora todas las relaciones están
conectadas a sus dos clases.

La relación entre RepresentanteTelefonico y TipoProducto ("especializa por rubro") estaba
punteada, como dependencia. Es el mismo error que el profe marcó con TicketStatus: el
representante guarda `tiposProducto` como atributo, así que es una asociación. Ahora va con
línea continua, el nombre "atiende" y multiplicidad * a 1..*.

La secuencia 4 usa `agregarNotificacion(n)` sobre el Ticket, pero ese método no estaba en la
clase. Ahora está.

Las multiplicidades estaban escritas todas juntas en el medio de la línea ("1 *"). Ahora van
en cada punta, que es como se leen en UML.

**Cosas que faltaban y se agregaron**

Ticket ahora tiene `fecha` y `estado` como atributos, además de los métodos `estaCerrado()`,
`agregarNotificacion()` y `contraparte()`.

Notificacion tiene `enviada` y `destinatario`. Antes tenía `getDestinatario()` pero no había
dónde guardar el destinatario.

Producto tiene `tipo` y `setTipo()`, que es lo que usa la secuencia de asignar tipo.

Estado y TipoProducto ahora se marcan como «enumeration» y sus valores van en su propio
compartimento.

Los métodos que no tenían parámetros ahora los tienen, por ejemplo
`esValido(destino: Estado)`, `transicion(destino: Estado)`, `login(email: String)` y
`crearTicket(titulo, descripcion, p: Producto)`.

**La GUI ahora es web**

El objeto de borde GUI ahora se llama "GUI (web Flask / consola)". El mismo borde está
hecho dos veces, una con Flask y otra por consola, y las dos tienen los mismos métodos y
hablan con los mismos controladores. Eso muestra para qué sirve separar borde, control y
entidad: se cambió la interfaz sin tocar ni el dominio ni la base. Se sumaron
`mostrarRegistro()` y `mostrarNotificaciones()`, que son pantallas que ya existían en el
sistema.

**Clases nuevas que aparecieron al implementar**

ControladorUsuario es un objeto de control para el registro y el login. Sin él, la GUI
tendría que hablar con la base de datos, y eso rompe la regla de que el formulario nunca va
directo al dominio.

BaseDeDatos (SQLite), con el estereotipo «persistencia», es la clase que guarda y recupera
todo. Los controladores la usan, y ni la GUI ni el dominio la conocen.

## Diagrama de casos de uso (casoDeUso.drawio)

Se agregó Reabrir ticket. El requerimiento 3.6 existía y la ficha CU-03 lo nombra ("para eso
existe el caso de uso Reabrir ticket"), pero en el diagrama no estaba.

Se agregó Asignar tipo de producto, que viene del cambio del cliente del hito 4 y tiene su
secuencia en el hito 5.

Cambiar estado y Cerrar ticket estaban unidos a Enviar notificación con «extend», con la
flecha apuntando hacia notificación. Pero la ficha CU-03 dice que siempre se notifica al
cliente, y eso es un «include». Con «extend», además, la flecha tendría que ir al revés.
Ahora son «include».

Crear ticket no estaba unido a Enviar notificación, aunque la ficha CU-01 dice en el paso 5
que se notifica al representante. Ahora tiene su «include».

## Diagramas de secuencia

Ahora son cinco: los cuatro del hito 6 más el de asignar tipo de producto del hito 5. Los
nombres de archivo coinciden con el título. Antes `hito6_secuencia2` se titulaba
"secuencia-03" y `hito6_secuencia3` se titulaba "secuencia-02".

En todos se sumó la línea de vida BaseDeDatos, para que se vea dónde se guarda cada cosa en
SQLite, y los mensajes usan los mismos nombres y parámetros que el código.

**secuencia-01 Crear ticket.** Antes el representante aparecía de la nada en
`crearNotificacion(ticket, representante)`. Ahora el controlador llama a
`asignarRepresentante(tipo)`, que busca a los representantes del rubro. También se ve la
creación del Producto (composición con Ticket) y que el Ticket lo crea el Cliente con
`crearTicket(...)`, el método que ya estaba en el diagrama de clases.

**secuencia-02 Registrar hito.** Se ve el control de ticket cerrado (`estaCerrado()`, la
excepción E1 de la ficha) y cómo se elige a quién notificar con `contraparte(autor)`.

**secuencia-03 Cambiar estado.** El hito automático aparecía en `agregarHito(hitoAutomatico)`
sin que nadie lo creara. Ahora está el `new Hito('Estado cambiado de X a Y', autor)`. La
validación de la transición la hace `Estado.transicion(e)`.

**secuencia-04 Enviar notificación.** La notificación ahora se crea con su destinatario, y
el controlador la envía, la agrega al ticket y la guarda. Se sacó `getDestinatario()` sobre
Usuario, porque el destinatario ya viene como parámetro.

**secuencia-05 Asignar tipo de producto.** Es la versión actualizada de la del hito 5:
GUI, después ControladorProducto, después Producto con `setTipo(tipo)` y, al final, la base.

## Fichas de casos de uso (hito 2)

La versión corregida está en `fichas/hito2_fichas_actualizadas.docx`, con su PDF al lado.
Se mantuvo el formato original y solo se cambiaron cinco textos.

En CU-01 Crear ticket, el paso 2 decía "completa título y descripción". Desde el hito 4 el
cliente también carga el producto y, si lo sabe, el tipo de producto, así que ahora lo dice.
El paso 4 y la postcondición decían "asigna un Representante disponible". Ahora dicen que se
asigna uno que atienda ese tipo de producto, priorizando al que tenga menos tickets abiertos.

También en CU-01, la excepción E2 decía que si no hay representantes se "notifica al
administrador", pero en el sistema no existe ningún actor administrador. Ahora dice "El
sistema registra el ticket sin representante asignado", que es lo que hace el código.

En CU-03 Cambiar estado, el comentario decía que el flujo es ABIERTO, EN PROCESO, CERRADO.
Se agregó que también se puede cerrar directo desde ABIERTO (por ejemplo, si el cliente
resolvió solo el problema), que es lo que permite el sistema.

## Requerimientos

Están en `requerimientos-actualizados.md`: los del hito 1, los que faltaban del cambio del
hito 4 y los que salen de las fichas y del código, cada uno marcado como nuevo.
