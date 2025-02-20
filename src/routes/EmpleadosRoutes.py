from flask import Blueprint, request, jsonify

# Logger
from src.utils.Logger import Logger
# Security
from src.utils.Security import Security
# Services
from src.services.Empleados import EmpleadosService
from src.schemas.empleadoSchema import empleado_schema


main = Blueprint('empleadosOlds_blueprint', __name__)


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
    
@classmethod
def update_evento(cls, id_evento, evento_data):
  try:
      # Validar datos
      evento = eventos_schema.load(evento_data)

      connection = get_connection()
      set_clause = []
      values = []

      if evento.tipo is not None:
          set_clause.append("TIPO = %s")
          values.append(evento.tipo)
      if evento.op is not None:
          set_clause.append("OP = %s")
          values.append(evento.op)
      if evento.titulo is not None:
          set_clause.append("TITULO = %s")
          values.append(evento.titulo)
      if evento.descripcion is not None:
          set_clause.append("DESCRIPCION = %s")
          values.append(evento.descripcion)
      if evento.fecha_inicio is not None:
          set_clause.append("FECHA_INICIO = %s")
          values.append(evento.fecha_inicio)
      if evento.fecha_fin is not None:
          set_clause.append("FECHA_FIN = %s")
          values.append(evento.fecha_fin)
      if evento.equipos is not None:
          set_clause.append("EQUIPOS = %s")
          values.append(evento.equipos)

      if not set_clause:
          raise ValueError("nada para actualizar")

      set_clause_str = ", ".join(set_clause)
      values.append(id_evento)

      with connection.cursor() as cursor:
          cursor.execute(f'''
              UPDATE assembled_db.Eventos
              SET {set_clause_str}
              WHERE ID_EVENTO = %s;
          ''', tuple(values))
      connection.commit()
      connection.close()
      return True
  except Exception as ex:
      Logger.add_to_log("error", str(ex))
      Logger.add_to_log("error", traceback.format_exc())
      return False
