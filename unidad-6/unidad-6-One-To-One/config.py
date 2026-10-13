"""
config.py — Configuración de la aplicación Flask + SQLAlchemy + Marshmallow
(versión sin Connexion, compatible con Python 3.14)
"""

import pathlib
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Directorio base del proyecto
basedir = pathlib.Path(__file__).parent.resolve()

# Crear la aplicación Flask directamente
app = Flask(__name__, template_folder=str(basedir / "templates"))

# Configurar SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'people.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar extensiones
db = SQLAlchemy(app)
ma = Marshmallow(app)