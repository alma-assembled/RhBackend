from flask import Flask
from flask_cors import CORS

# Routes
from .routes import AuthRoutes, IndexRoutes, EmpleadosRoutes , EmpleadosRoutesOlds

app = Flask(__name__)
#CORS(app, resources={r"/empleados/*": {"origins": "http://localhost:3000"}})
CORS(app)
def init_app(config):
    # Configuration
    app.config.from_object(config)
    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(EmpleadosRoutes.main, url_prefix='/empleados-olds')
    app.register_blueprint(EmpleadosRoutesOlds.main, url_prefix='/empleados')
    app.run(host='0.0.0.0', port=5050, debug=True)
    
    return app