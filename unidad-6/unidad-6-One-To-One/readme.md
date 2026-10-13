# Cómo ejecutar el proyecto One-To-One (Flask + SQLAlchemy)

**Materia:** Algoritmos y Estructuras de Datos III  
**Prof.:** Lic. José Luis Oemig — ISFT N°151, Mar del Plata

---

> **Nota:** Esta versión del proyecto usa **Flask puro** en lugar de Connexion,
> porque Connexion 2.x no es compatible con Python 3.14 (werkzeug 2.2.x usa
> `ast.Str`, que Python 3.14 eliminó). La API es idéntica en comportamiento;
> solo cambia que las rutas están definidas con `@app.route()` en lugar de
> en el archivo `swagger.yml`.

---

## Estructura del proyecto

```
One-To-One/
├── app.py
├── config.py
├── models.py
├── requirements.txt
└── templates/
    └── home.html
```

> **Importante:** el archivo `home.html` tiene que estar dentro de una subcarpeta
> llamada `templates`. Si no existe esa carpeta, créala y mové el archivo adentro.

---

## Paso 1 — Desinstalar lo que estaba y limpiar

Si ya habías instalado dependencias de la versión anterior (con Connexion),
desinstalalas primero para evitar conflictos:

```
pip uninstall connexion werkzeug flask -y
```

---

## Paso 2 — Instalar las dependencias nuevas

```
pip install -r requirements.txt
```

Esto instala Flask 3.x (con werkzeug 3.x, compatible con Python 3.14),
SQLAlchemy, Marshmallow y todo lo necesario.

Si querés instalar cada cosa por separado:

```
pip install flask
pip install flask-sqlalchemy
pip install "flask-marshmallow==0.15.0"
pip install "marshmallow==3.23.2"
pip install "marshmallow-sqlalchemy==0.29.0"
```

---

## Paso 3 — Ejecutar la aplicación

Desde la terminal, dentro de la carpeta del proyecto:

```
python app.py
```

Deberías ver algo así:

```
 * Running on http://0.0.0.0:8000
 * Debug mode: on
```

La aplicación quedó corriendo. No cierres esa terminal mientras la uses.

deja esa terminal y en una nueva pega:

curl -X POST http://localhost:8000/api/people -H "Content-Type: application/json" -d "{\"fname\": \"Maria\", \"lname\": \"Gonzalez\"}"

Esto sirve para cargar y vizualisar a Persona "Maria"
---

## Paso 4 — Abrir en el navegador

Con la app corriendo, abrí tu navegador y entrá a cualquiera de estas
direcciones:

| URL | Qué muestra |
|-----|-------------|
| `http://localhost:8000/` | Página de inicio con la tabla de personas |
| `http://localhost:8000/api/people` | JSON con todas las personas |

---

## Paso 5 — Probar la API

Como esta versión no tiene Swagger UI, podés probar la API de dos maneras:

### Desde el navegador (solo GET)

- `http://localhost:8000/api/people` — lista todas las personas
- `http://localhost:8000/api/people/Gonzalez` — busca por apellido

### Desde la terminal con curl (todos los métodos)

```bash
# Traer todas las personas
curl http://localhost:8000/api/people

# Crear una persona nueva
curl -X POST http://localhost:8000/api/people \
     -H "Content-Type: application/json" \
     -d "{\"fname\": \"María\", \"lname\": \"González\"}"

# Buscar por apellido
curl http://localhost:8000/api/people/González

# Actualizar el nombre
curl -X PUT http://localhost:8000/api/people/González \
     -H "Content-Type: application/json" \
     -d "{\"fname\": \"María Victoria\", \"lname\": \"González\"}"

# Eliminar
curl -X DELETE http://localhost:8000/api/people/González
```

> En Windows CMD, reemplazá las comillas simples por dobles y escapalas con `\"`.

---

## Base de datos

La primera vez que ejecutás `python app.py`, SQLAlchemy crea automáticamente
el archivo `people.db` en la misma carpeta. No hace falta crear nada manualmente.

Si querés ver el contenido, descargá **DB Browser for SQLite** (gratuito)
desde https://sqlitebrowser.org/ y abrí el archivo `people.db`.

---

## Para detener la aplicación

En la terminal donde está corriendo, presioná `Ctrl + C`.

---

## Errores comunes

**`ModuleNotFoundError: No module named 'flask'`**  
→ Las dependencias no están instaladas. Ejecutá `pip install -r requirements.txt`.

**`jinja2.exceptions.TemplateNotFound: home.html`**  
→ El archivo `home.html` no está dentro de la carpeta `templates/`. Creá esa
carpeta y mové el archivo adentro.

**`AttributeError: module 'ast' has no attribute 'Str'`**  
→ Quedó instalado werkzeug 2.2.x de antes. Ejecutá:
`pip uninstall werkzeug -y` y luego `pip install flask` de nuevo.

**`Address already in use` o el puerto 8000 está ocupado**  
→ Ya hay otra instancia corriendo. Cerrá la otra terminal o cambiá el puerto
en la última línea de `app.py`:  
`app.run(host="0.0.0.0", port=8080, debug=True)`  
y entrá a `http://localhost:8080`.