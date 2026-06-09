# PROCESO — HITO 1
## Trabajo Práctico Final Integrador 2026 — Sistema de Ticketing
### ISFT N°151 · Algoritmos y Estructuras de Datos III

________________________________________________________________________________________________________________

## Consigna_____________________________________________________________________________________________________

El sistema de ticketing es una herramienta de atención al cliente que ayuda a las empresas
a administrar sus casos de servicio y soporte. 
Crea un «ticket» para documentar solicitudes e interacciones de los clientes, 
facilitando la resolución de problemas.

**Dinámica del sistema:**_______________________________________________________________________________________
--- El ticket se comparte entre el cliente y el representante telefónico.
---La comunicación queda registrada en un hilo continuo llamado **Hitos**.
--- Cuando hay actualizaciones, el sistema notifica a la parte correspondiente.
--- El ticket puede cerrarse y volver a abrirse si hay seguimiento adicional.
--- El cliente siempre trabaja con el mismo representante que atendió su caso.

**Se pide en el Hito 1:**______________________________________________________________________________________
1. Escribir los Requerimientos.
2. Desarrollar el Modelo de Casos de Uso en UML.

___

## Resolución en clases_________________________________________________________________________________________

### 1. Identificar actores y casos de uso

+ Se identifican quiénes interactúan con el sistema y qué acciones realizan.

```
Actores identificados:
  Cliente             → crea tickets, registra hitos, consulta, cierra ticket
  Representante       → atiende tickets, registra hitos, cambia estado, lista usuarios
  Telefónico

Funcionalidades clave detectadas en la consigna:
  - Gestión de usuarios (login, sin duplicados)
  - Gestión de representantes
  - Gestión de tickets (crear, consultar, cambiar estado, cerrar, reabrir)
  - Gestión de hitos (registrar, listar, asociar al ticket)
  - Notificaciones (al registrar hito, al cambiar estado)
  - Seguridad (login obligatorio para operar)
```

___

## Requerimientos Funcionales realizadas en clase________________________________________________________________

```
1 — Gestión de usuarios__________________________________________________________________________________________
  1.1  El sistema deberá permitir registrar usuarios.
  1.2  El sistema deberá no permitir la duplicación de usuarios.
  1.3  El sistema deberá permitir listar usuarios.

2 — Gestión de representantes_____________________________________________________________________________________
  2.1  El sistema deberá permitir listar representantes

3 — Gestión de tickets____________________________________________________________________________________________
  3.1  El sistema deberá permitir crear un ticket.
  3.2  El sistema deberá asociar un cliente con un ticket.
  3.3  El sistema deberá asociar un representante telefónico con un ticket.
  3.4  El sistema deberá gestionar el estado de cada ticket
         (abierto / en proceso / cerrado).
  3.5  El sistema deberá permitir cerrar un ticket.
  3.6  El sistema deberá permitir reabrir un ticket cerrado.

4 — Gestión de hitos_______________________________________________________________________________________________
  RF4.1  El sistema deberá permitir registrar hitos dentro de un ticket.
  RF4.2  El sistema deberá listar los hitos de un ticket.
  RF4.3  El sistema deberá asociar cada hito con su ticket correspondiente.

5 — Notificaciones_________________________________________________________________________________________________
  5.1  El sistema deberá notificar al representante cuando el cliente
         registre un hito.
  5.2  El sistema deberá notificar al cliente cuando el representante
         actualice o cambie el estado del ticket.

6 — Seguridad______________________________________________________________________________________________________
  6.1  El sistema deberá requerir inicio de sesión para operar (login).
```

___

## Requerimientos No Funcionales__________________________________________________________________________________

```
1  El sistema deberá ser codificado utilizando TDD.
2  El sistema no deberá permitir la duplicación de usuarios.
3  El sistema deberá ser accesible vía web.
4  El sistema deberá funcionar en Windows 10 en adelante.
```

### Actores_________________________________________________________________________________________________________

```
Cliente                → usuario final que solicita soporte
Representante          → agente que gestiona y resuelve los tickets
Telefónico
```

### Casos de uso por actor__________________________________________________________________________________________

```
Cliente:
  - Registrar cliente
  - Iniciar sesión              (compartido con Representante)
  - Crear ticket                (compartido con Representante)
  - Consultar ticket            (compartido con Representante)
  - Registrar hito              (compartido con Representante)
  - Cerrar ticket               (compartido con Representante)

Representante Telefónico:
  - Iniciar sesión
  - Crear ticket
  - Consultar ticket
  - Registrar hito
  - Cambiar estado ticket
  - Cerrar ticket
  - Listar usuarios
  - Listar representantes
```
