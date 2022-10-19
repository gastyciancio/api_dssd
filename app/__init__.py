from os import environ
from flask import Flask, render_template
from config import config
from app import db
from flask_cors import CORS
from app.models.supplier import Supplier
from app.models.material import Material
from app.models.supplier_material import SupplierMaterial
from app.models.maker import Maker
from app.models.maker_material import MakerMaterial
from app.resources.supplier import supplier
from app.resources.auth import auth
from app.resources.maker import maker
from datetime import timedelta
#JWT
from flask_jwt_extended import JWTManager

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

    #Jwt
    app.config["JWT_SECRET_KEY"] = "wvf7QQwBHAj0u6BvDXhV0NXySu7f9R3qvvoAmh9zxLcfiLQSAsSjqm18ypRD29UN2fDpojt_jwdyToYzmiDull00N7lEasOl_EXaBiwwJNt"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
    jwt = JWTManager(app)

    # Rutas
    app.register_blueprint(supplier)
    app.register_blueprint(auth)
    app.register_blueprint(maker)

    @app.route("/")
    def home():
        # No dar bola a esto, es para que se cree las tablas cuando inicias por primera vez todo
        SupplierMaterial.get_supllier_material()
        Material.get_material()
        Supplier.get_suppliers('',None,None)
        Maker.get_makers()
        MakerMaterial.get_maker_material()
        return render_template("home.html")  
    return app