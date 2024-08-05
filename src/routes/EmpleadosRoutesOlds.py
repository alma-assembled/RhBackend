from flask import Blueprint, request, jsonify

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.EmpleadosOld import EmpleadosServiceOlds
from src.schemas.empleadoSchema import empleado_schema


main = Blueprint('empleados_blueprint', __name__)


@main.route('/')
def get_empleados():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            empleados = EmpleadosServiceOlds.get_empleados()
            if (len(empleados) > 0):
                return jsonify({'Empleado': empleados, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
          #  Logger.add_to_log(f"Error routes getEmpleados: {str(ex)}")
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
@main.route('/inactivos')
def get_empleados_inactivos():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            empleados = EmpleadosServiceOlds.get_empleados_inactivos()
            if (len(empleados) > 0):
                return jsonify({'Empleado': empleados, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
          #  Logger.add_to_log(f"Error routes getEmpleados: {str(ex)}")
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
@main.route('/<int:id>', methods=['GET'])
def get_empleado_by_id(id):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            empleado = EmpleadosServiceOlds.get_empleado_by_id(id)
            if empleado:
                return jsonify({'Empleado': empleado, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
            print(f"Error: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False})
    else:
        return jsonify({'message': 'Unauthorized'}), 401
    
@main.route('/', methods=['POST'])
def post_create_empleado():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            data = request.json
            errors = empleado_schema.validate(data)
            
            if errors:
                return jsonify(errors), 400
            
            empleado = EmpleadosServiceOlds.save_empleado(data)
            if empleado == True  :
                return jsonify({'success': True})
            elif empleado ==  False :
                return jsonify({'message': "Error al guardar el empleado", 'success': False}), 500
            else :
                return jsonify({'message': empleado , 'success': False}), 200
        except Exception as ex:
            Logger.add_to_log(f"Error routes POSTEmpleados: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@main.route('/reingreso/<int:id_empleado>', methods=['PUT'])
def editar_reingreso_empleado(id_empleado):    
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            data = request.json
            if EmpleadosServiceOlds.update_reingreso(id_empleado, data):
                return jsonify({'success': True, "message": "Empleado actualizado correctamente"}), 200
            else:
                return jsonify({'success': False, "message": "Error  al actualizar empleado"}), 500
        except Exception as ex:
            Logger.add_to_log(f"Error: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False}), 500

    
@main.route('/baja-empleado/<int:id_empleado>', methods=['PUT'])
def put_baja_empleado(id_empleado):
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            empleado = EmpleadosServiceOlds.baja_empleado(id_empleado)
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
            puestos = EmpleadosServiceOlds.get_puestos()
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
            puestos = EmpleadosServiceOlds.get_bancos()
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
    
@main.route('/<int:id_empleado>', methods=['PUT'])
def editar_empleado(id_empleado):    
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            data = request.json
            if EmpleadosServiceOlds.update_empleado(id_empleado, data):
                return jsonify({'success': True, "message": "Empleado actualizado correctamente"}), 200
            else:
                return jsonify({'success': False, "message": "Error  al actualizar empleado"}), 500
        except Exception as ex:
            Logger.add_to_log(f"Error: {str(ex)}")
            return jsonify({'message': "ERROR", 'success': False}), 500

@main.route('/resumen')
def get_resumen():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            resumen = EmpleadosServiceOlds.get_resumen()
            if resumen:
                return jsonify({'data': resumen, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except Exception as ex:
          #  Logger.add_to_log(f"Error routes getEmpleados: {str(ex)}"))
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401    

@main.route('/cumple')
def get_cumpleaños():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            data = EmpleadosServiceOlds.get_cumpleaños_mes()
            if (len(data) > 0):
                return jsonify({'data': data, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'data': "NOTFOUND", 'success': True})
        except Exception as ex:
          #  Logger.add_to_log(f"Error routes getEmpleados: {str(ex)}")
            print(ex)
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
