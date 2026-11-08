# Requerimientos actualizados · Sistema de Ticketing

TP Final Integrador · Algoritmos y Estructuras de Datos III · ISFT N°151

Versión final, con lo que se hizo en clase en el hito 1, el cambio del cliente del hito 4
(producto y tipo de producto) y lo que apareció al implementar. Lo nuevo está marcado con
*(nuevo)*.

## Requerimientos funcionales

```
1 — Gestión de usuarios
  1.1  El sistema deberá permitir registrar usuarios.
  1.2  El sistema deberá no permitir la duplicación de usuarios.
  1.3  El sistema deberá permitir listar usuarios.

2 — Gestión de representantes
  2.1  El sistema deberá permitir listar representantes.
  2.2  El sistema deberá registrar los tipos de producto que atiende
       cada representante.                                          (nuevo, hito 4)

3 — Gestión de tickets
  3.1  El sistema deberá permitir crear un ticket.
  3.2  El sistema deberá asociar un cliente con un ticket.
  3.3  El sistema deberá asociar un representante telefónico con un ticket.
  3.4  El sistema deberá gestionar el estado de cada ticket
       (abierto / en proceso / cerrado).
  3.5  El sistema deberá permitir cerrar un ticket.
  3.6  El sistema deberá permitir reabrir un ticket cerrado.
  3.7  El sistema deberá registrar el producto asociado a cada ticket. (nuevo, hito 4)
  3.8  El sistema deberá permitir asignar un tipo de producto
       (línea blanca, cocina, electro, pequeños electrodomésticos)
       al producto del ticket.                                      (nuevo, hito 4)
  3.9  El sistema deberá asignar el ticket a un representante que
       atienda el tipo de producto, priorizando al que tenga menos
       tickets abiertos.                                            (nuevo, hito 4)
  3.10 El sistema deberá validar que los cambios de estado respeten
       el flujo permitido.                                          (nuevo)

4 — Gestión de hitos
  4.1  El sistema deberá permitir registrar hitos dentro de un ticket.
  4.2  El sistema deberá listar los hitos de un ticket.
  4.3  El sistema deberá asociar cada hito con su ticket correspondiente.
  4.4  El sistema deberá registrar un hito automático cada vez que
       cambie el estado de un ticket.                               (nuevo, sale de la ficha CU-03)
  4.5  El sistema deberá no permitir registrar hitos en un ticket
       cerrado.                                                     (nuevo, sale de la ficha CU-02)

5 — Notificaciones
  5.1  El sistema deberá notificar al representante cuando el cliente
       registre un hito.
  5.2  El sistema deberá notificar al cliente cuando el representante
       actualice o cambie el estado del ticket.
  5.3  El sistema deberá notificar al representante cuando se le
       asigne un ticket nuevo.                                      (nuevo, sale de la ficha CU-01)
  5.4  El sistema deberá permitir a cada usuario consultar sus
       notificaciones.                                              (nuevo)

6 — Seguridad
  6.1  El sistema deberá requerir inicio de sesión para operar (login).
  6.2  El sistema deberá permitir operar sobre un ticket solo al
       cliente y al representante que participan de él.             (nuevo, sale de la ficha CU-03, E3)
```

## Requerimientos no funcionales

```
1  El sistema deberá ser codificado utilizando TDD.
2  El sistema no deberá permitir la duplicación de usuarios.
3  El sistema deberá ser accesible vía web.
4  El sistema deberá funcionar en Windows 10 en adelante.
5  El sistema deberá desarrollarse en Python con el framework Flask. (nuevo, consigna de implementación)
6  El sistema deberá persistir los datos en una base SQLite.        (nuevo, consigna de implementación)
```

El RNF 3 se cumple con la interfaz web hecha en Flask (`app.py`, en http://localhost:5000).
