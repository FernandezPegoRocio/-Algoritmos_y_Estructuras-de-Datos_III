# Ejecución · Sistema de Ticketing

TP Final Integrador · Algoritmos y Estructuras de Datos III · ISFT N°151 · Rocío Fernández Pego

## Qué hay en la carpeta

- **`README.md`**: la consigna, cómo hice el trabajo y la memoria del proyecto.
- **`EJECUCION.md`**: este archivo, con los pasos para correrlo.
- **`implementacion/`**: el programa en Python. `app.py` es la versión web con Flask,
  `main.py` la versión por consola, `ticketing/` tiene el código y `tests/` las pruebas.
- **`diagramas-finales/`**: casos de uso, clases y 5 secuencias en .drawio y en PNG, las
  fichas del hito 2 corregidas, los requerimientos actualizados y `CAMBIOS.md`.
- **`capturas/`**: imágenes del sitio funcionando.

## Antes de empezar

Hace falta Python instalado. Para comprobarlo, abrí una terminal (PowerShell o la de VS
Code) y escribí:

```bash
python --version
```

Si muestra una versión (por ejemplo `Python 3.12.10`), está todo bien.

Carpeta:

cd "C:\Users\vboxuser\Desktop\tp-final-ticketing-Fernandez-Pego\implementacion"

## Paso 1 · Entrar a la carpeta del programa

Desde la carpeta donde descomprimiste el TP:

```bash
cd implementacion
```

## Paso 2 · Instalar Flask (solo la primera vez)

```bash
pip install -r requirements.txt
```

Instala Flask 3.1.3, que es lo único que hace falta. SQLite ya viene con Python.

## Paso 3 · Levantar el sitio

```bash
python app.py
```

En la terminal aparece `Running on http://127.0.0.1:5000`. Esa terminal tiene que quedar
abierta mientras se usa el sitio.

## Paso 4 · Abrirlo en el navegador

```
http://localhost:5000
```

La primera vez se crea sola la base `ticketing.db`, al lado de `app.py`, con estos
usuarios de prueba. No tienen contraseña: se entra con el email.

- **ana@mail.com**: clienta.
- **laura@soporte.com**: representante de línea blanca y cocina.
- **martin@soporte.com**: representante de electro y pequeños electrodomésticos.

## Paso 5 · Probar el recorrido completo

1. Entrar como `ana@mail.com` y crear un ticket desde "Nuevo ticket", por ejemplo una
   heladera con tipo "línea blanca".
2. Ver que el ticket se asignó a Laura (R-001), porque ella atiende ese rubro.
3. Escribir un hito, por ejemplo "Ya probé desenchufarla".
4. Tocar "Salir" y entrar como `laura@soporte.com`. En "Notificaciones" aparecen el aviso
   del ticket nuevo y el del hito de Ana.
5. Abrir el ticket, pasarlo a "en proceso" y contestar con otro hito.
6. Salir y volver a entrar como Ana: le llegaron las notificaciones del cambio de estado y
   de la respuesta.

## Paso 6 · Apagar el sitio

En la terminal donde corre, `Ctrl + C`.

## Correr los tests

Desde la carpeta `implementacion`:

```bash
python -m unittest -v
```

Tienen que dar **53 tests OK**. Si Flask no está instalado, los 10 de la web se saltean y
corren los otros 43.

## Versión por consola (opcional)

Usa la misma base y no necesita Flask:

```bash
python main.py
```

Se maneja con menús numerados: se escribe el número de la opción y Enter.

## Si algo falla

- **"python no se reconoce como comando"**: probar con `py` en lugar de `python`, por
  ejemplo `py app.py`.
- **"No module named flask"**: falta el paso 2. Si `pip` tampoco anda, usar
  `python -m pip install -r requirements.txt`.
- **"Address already in use"**: el puerto 5000 está ocupado, seguramente por otra ventana
  con el sitio abierto. Cerrarla con `Ctrl + C`, o cambiar `port=5000` por `port=5001` al
  final de `app.py` y entrar a http://localhost:5001.
- **Empezar con la base limpia**: apagar el sitio, borrar `ticketing.db` y volver a correr
  `python app.py`.
