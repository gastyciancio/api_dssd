from os import environ
from flask import Flask, render_template, session
from config import config
from app import db
from flask_cors import CORS
from app.models.supplier import Supplier
from app.models.material import Material
from app.models.supplier_material import SupplierMaterial
from app.resources.supplier import supplier


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    CORS(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    #app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    # Funciones que se exportan al contexto de Jinja2
    
    # Rutas de Consultas

    app.register_blueprint(supplier)

    # Autenticación

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        # No dar bola a esto, es para cue se cree las tablas cuando inicias por primera vez todo
        SupplierMaterial.get_supllier_material()
        Material.get_material()
        Supplier.get_suppliers('') 
        return render_template("home.html")  
    return app