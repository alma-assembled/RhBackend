from flask import Flask
from flask_cors import CORS

# Routes
from .routes import AuthRoutes, IndexRoutes, EmpleadosRoutes

app = Flask(__name__)
CORS(app) 

def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(EmpleadosRoutes.main, url_prefix='/empleados')

    return app