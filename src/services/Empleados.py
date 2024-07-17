import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger
from src.schemas.empleadoSchema import empleado_schema   

from src.models.EmpleadoModel import Empleado

class EmpleadosService():

    @classmethod
    def get_empleados(cls):
        try:
            connection = get_connection()
            empleados = []
            with connection.cursor() as cursor:
                cursor.execute('''
                SELECT e.ID_CEMPLEADO, e.NOMBRE,COALESCE(e.N_EMPLEADO , "NO ASIGNADO") AS N_EMPLEADO, COALESCE(rhc.PUESTO, "") AS PUESTO
                FROM ops.catalogo_empleados e
                LEFT JOIN OPS.Base_EmpleadosPuestos p ON e.ID_CEMPLEADO = p.ID_CEMPLEADO
                LEFT JOIN OPS.RH_Cat_puestos rhc ON p.ID_RHCPUESTO = rhc.ID_RHCPUESTO
                WHERE e.ACTIVO = TRUE AND (p.ACTIVO = TRUE OR p.ID_CEMPLEADO IS NULL) AND (rhc.ACTIVO = TRUE OR rhc.ID_RHCPUESTO IS NULL) 
                UNION
                SELECT e.ID_CEMPLEADO, e.NOMBRE,COALESCE(e.N_EMPLEADO , "NO ASIGNADO") AS N_EMPLEADO,  COALESCE(rhc.PUESTO, "") AS PUESTO
                FROM ops.catalogo_empleados e
                RIGHT JOIN OPS.Base_EmpleadosPuestos p ON e.ID_CEMPLEADO = p.ID_CEMPLEADO
                RIGHT JOIN OPS.RH_Cat_puestos rhc ON p.ID_RHCPUESTO = rhc.ID_RHCPUESTO
                WHERE e.ACTIVO = TRUE AND p.ACTIVO = TRUE AND rhc.ACTIVO = TRUE order by NOMBRE; 
                ''')
                resultset = cursor.fetchall()
                for row in resultset:
                    empleado = Empleado.empleadosAll_serializers(int(row[0]), row[1], row[2], row[3])
                    empleados.append(empleado)
            connection.close()
            return empleados
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def save_empleado(cls, empleado_data):
        try:
            # Deserializar datos
            empleado = empleado_schema.load(empleado_data)

            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''
               INSERT INTO ops.catalogo_empleados (`NOMBRE`, `FECHA_NACIMIENTO`, `GENERO`, `PROGENITOR`, `N_EMPLEADO`, `PIN`, `CORREO`, `USUARIO`, `CLAVE`, `MAQUILADOR`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE NOMBRE=VALUES(NOMBRE), N_EMPLEADO=VALUES(N_EMPLEADO);
                ''', (empleado.nombre, empleado.fecha_nacimiento, empleado.genero, empleado.progenitor, empleado.n_empleado, empleado.pin, empleado.correo, empleado.usuario, empleado.clave, empleado.maquilador))

                if cursor.lastrowid:
                    idEmpleado = cursor.lastrowid
                else:
                    cursor.execute('''
                    SELECT ID_CEMPLEADO FROM ops.catalogo_empleados WHERE NOMBRE=%s AND N_EMPLEADO=%s;
                    ''', (empleado.nombre, empleado.n_empleado))
                    empleado.idEmpleado = cursor.fetchone()[0]

                cursor.execute('''
                INSERT INTO `OPS`.`Base_Sueldos` (`SUELDO`, `FECHA`, `ID_CEMPLEADO`)
                VALUES (%s, %s, %s);
                ''', (empleado.sueldo, empleado.fecha_inicio , idEmpleado))
                
                cursor.execute('''
                INSERT INTO OPS.Base_EmpleadosPuestos (`FECHA_INGRESO`, `ID_CEMPLEADO`, `ID_RHCPUESTO`)
                VALUES (%s, %s, %s);
                ''', (empleado.fecha_inicio, idEmpleado , empleado.id_puesto))

                cursor.execute('''
                INSERT INTO `OPS`.`Catalogo_ClavesInterbancarias` (`CLAVE`, `ID_CBANCO`, `ID_CEMPLEADO`) 
                VALUES (%s, %s, %s);
                ''', (empleado.clave_interbancaria , empleado.id_banco, idEmpleado))

            connection.commit()
            connection.close()
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False
        
    @classmethod
    def baja_empleado(cls, id_empleado):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                # Actualizar el registro del empleado en `catalogo_empleados`
                cursor.execute('''
                    UPDATE `OPS`.`Catalogo_Empleados` SET `ACTIVO` = '0' WHERE (`ID_CEMPLEADO` = '%s');
                ''', (id_empleado ))

                # Actualizar el sueldo del empleado en `Base_Sueldos`
                cursor.execute('''
                    UPDATE `OPS`.`Base_Sueldos` SET `ACTIVO` = '0' WHERE (ID_CEMPLEADO=%s AND ACTIVO=1);
                ''', (id_empleado))

                # Actualizar el puesto del empleado en `Base_EmpleadosPuestos`
                cursor.execute('''
                   UPDATE `OPS`.`Base_EmpleadosPuestos` SET `FECHA_BAJA` = '2024-06-26', `ACTIVO` = '0' WHERE (ID_CEMPLEADO=%s AND ACTIVO=1);
                ''', (id_empleado))

                # Actualizar la clave interbancaria del empleado en `Catalogo_ClavesInterbancarias`
                cursor.execute('''
                    UPDATE `OPS`.`Catalogo_ClavesInterbancarias` SET `ACTIVO` = '0' WHERE (ID_CEMPLEADO=%s AND ACTIVO=1);
                ''', (id_empleado))

            connection.commit()
            connection.close()
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    @classmethod
    def get_puestos(cls):
        try:
            connection = get_connection()
            puestos = []
            with connection.cursor() as cursor:
                cursor.execute('''
               SELECT ID_RHCPUESTO, PUESTO FROM OPS.RH_Cat_Puestos WHERE ACTIVO= TRUE ORDER BY PUESTO; 
                ''')
                resultset = cursor.fetchall()
                for row in resultset:
                    puesto = Empleado.puestos_all(int(row[0]), row[1])
                    puestos.append(puesto)
            connection.close()
            return puestos
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def get_bancos(cls):
        try:
            connection = get_connection()
            bancos = []
            with connection.cursor() as cursor:
                cursor.execute('''
            SELECT ID_CBANCO, BANCO FROM OPS.Catalogo_bancos WHERE ACTIVO= TRUE order by BANCO; 
                ''')
                resultset = cursor.fetchall()
                for row in resultset:
                    banco = Empleado.bancos_all(int(row[0]), row[1])
                    bancos.append(banco)
            connection.close()
            return bancos
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

            