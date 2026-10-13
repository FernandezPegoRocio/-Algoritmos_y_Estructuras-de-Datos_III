# Cómo ejecutar los ejemplos ORM SQLAlchemy 2+

**Materia:** Algoritmos y Estructuras de Datos III  
**Prof.:** Lic. José Luis Oemig — ISFT N°151, Mar del Plata

---

## Requisitos previos

Necesitás tener instalado **Python 3.10 o superior**. Podés verificarlo abriendo una terminal y escribiendo:

```
python --version
```

Si no tenés Python instalado, descargalo desde https://www.python.org/downloads/

---

## Instalación de SQLAlchemy

Los tres ejemplos usan únicamente SQLAlchemy. No necesitan ninguna otra librería externa. Para instalarla, abrí una terminal y ejecutá:

```
pip install sqlalchemy
```

Si en tu sistema Python y pip están como `python3` y `pip3`, usá:

```
pip3 install sqlalchemy
```
```
pip install --upgrade sqlalchemy
```
```
python.exe -m pip install --upgrade pip
```
---

## Estructura de archivos

Guardá los tres archivos en una misma carpeta, por ejemplo `orm_ejemplos/`:

```
orm_ejemplos/
├── orm_crud_completo.py
├── orm_one_to_many.py
└── orm_many_to_many.py
```

---

## Ejecución

Abrí una terminal, navegá hasta la carpeta donde guardaste los archivos y ejecutá cada uno por separado:

### Ejemplo 1 — CRUD completo

```
python orm_crud_completo.py
```

Este script crea una base de datos `crud_completo.db` y demuestra las cuatro operaciones básicas sobre un modelo `Producto`: crear productos, leerlos todos, buscar por ID, actualizar precio y stock, y eliminar un registro.

Salida esperada:

```
[CREATE] Producto(id=1, nombre='Laptop', precio=1200.00, stock=10)
[CREATE] Producto(id=2, nombre='Mouse inalámbrico', precio=25.50, stock=50)
...
[READ] Todos los productos:
  Producto(id=1, nombre='Laptop', precio=1200.00, stock=10)
  ...
[UPDATE] Precio actualizado: Producto(id=1, nombre='Laptop', precio=1099.00, stock=10)
[DELETE] Eliminado: 'Monitor 27"' (id=4)
```

---

### Ejemplo 2 — One to Many (un autor, muchos libros)

```
python orm_one_to_many.py
```

Crea la base de datos `one_to_many.db` con dos tablas: `author` y `book`. Demuestra cómo un autor puede tener varios libros, cómo actualizar el título de un libro y cómo al eliminar un autor sus libros se eliminan automáticamente (cascade delete).

Salida esperada:

```
Datos creados correctamente.

=== Autores y sus libros ===

Gabriel García Márquez:
  - Cien años de soledad
  - El amor en los tiempos del cólera

Jorge Luis Borges:
  - Ficciones
  - El Aleph
  - El libro de arena

Libro actualizado: El Aleph (edición revisada)
Autor y sus libros eliminados.
```

---

### Ejemplo 3 — Many to Many (estudiantes y materias)

```
python orm_many_to_many.py
```

Crea la base de datos `many_to_many.db` con tres tablas: `estudiante`, `materia` e `inscripcion` (tabla de asociación). Demuestra cómo un estudiante puede estar en varias materias y una materia puede tener varios estudiantes, y cómo agregar o quitar inscripciones.

Salida esperada:

```
Datos creados correctamente.

=== Estudiantes y sus materias ===
  Rocío: Algoritmos y Estructuras de Datos III, Redes de Computadoras
  Ana: Algoritmos y Estructuras de Datos III, Sistemas Operativos
  Carlos: Redes de Computadoras, Sistemas Operativos, Algoritmos y Estructuras de Datos III

Rocío inscripta en: Sistemas Operativos
Ana desinscripta de: Redes de Computadoras
```

---

## Archivos de base de datos generados

Cada script crea automáticamente su propio archivo `.db` en la misma carpeta donde lo ejecutás. No hace falta crear nada de antemano: SQLAlchemy genera las tablas al iniciar.

| Script | Base de datos creada |
|--------|----------------------|
| `orm_crud_completo.py` | `crud_completo.db` |
| `orm_one_to_many.py` | `one_to_many.db` |
| `orm_many_to_many.py` | `many_to_many.db` |

Si querés ver el contenido de esas bases de datos visualmente, podés descargar **DB Browser for SQLite** (gratuito) desde https://sqlitebrowser.org/ y abrir cualquiera de los archivos `.db` directamente.

---

## Si algo falla

**Error: `ModuleNotFoundError: No module named 'sqlalchemy'`**  
→ SQLAlchemy no está instalado. Ejecutá `pip install sqlalchemy` y volvé a intentarlo.

**Error: `database is locked`**  
→ Ya hay otro proceso usando el archivo `.db`. Cerrá cualquier otra terminal que esté ejecutando el mismo script y volvé a intentarlo.

**El script corre pero no muestra los datos esperados**  
→ Es posible que el archivo `.db` ya exista de una ejecución anterior con datos distintos. Borrá el archivo `.db` correspondiente y volvé a ejecutar el script.
