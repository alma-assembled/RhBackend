from flask import Blueprint, request, jsonify

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.Empleados import EmpleadosService
from src.schemas.empleadoSchema import empleado_schema


main = Blueprint('empleados_blueprint', __name__)


@main.route('/')
def get_empleados():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            empleados = EmpleadosService.get_empleados()
            if (len(empleados) > 0):
                return jsonify({'Empleados': empleados, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
          #  Logger.add_to_log(f"Error routes getEmpleados: {str(ex)}")
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
@main.route('/', methods=['POST'])
def post_create_empleado():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            data = request.json
            errors = empleado_schema.validate(data)
            
            if errors:
                return jsonify(errors), 400
            
            empleado = EmpleadosService.save_empleado(data)
            if empleado:
                return jsonify({'success': True})
            else:
                return jsonify({'message': "Error al guardar el empleado", 'success': False}), 500
        except Exception as ex:
            Logger.add_to_log(f"Error routes POSTEmpleados: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
    
@main.route('/baja-empleado/<int:id_empleado>', methods=['PUT'])
def put_baja_empleado(id_empleado):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            empleado = EmpleadosService.baja_empleado(id_empleado)
            if empleado:
                return jsonify({'success': True})
            else:
                return jsonify({'message': "Error al dar de baja al empleado", 'success': False}), 500
        except Exception as ex:
            Logger.add_to_log(f"Error routes bajaEmpleados: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
@main.route('/puestos')
def get_puestos():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            puestos = EmpleadosService.get_puestos()
            if (len(puestos) > 0):
                return jsonify({'Puestos': puestos, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
          #  Logger.add_to_log(f"Error routes getEmpleados: {str(ex)}")
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@main.route('/bancos')
def get_bancos():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            puestos = EmpleadosService.get_bancos()
            if (len(puestos) > 0):
                return jsonify({'Bancos': puestos, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
          #  Logger.add_to_log(f"Error routes getEmpleados: {str(ex)}")
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
