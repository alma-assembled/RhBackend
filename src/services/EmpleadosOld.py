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
                SELECT e.ID_CEMPLEADO, 
                e.NOMBRE,COALESCE(e.Pin , "NO ASIGNADO") AS N_EMPLEADO, 
                COALESCE(rhc.PUESTO, "") AS PUESTO
                FROM OPS.Catalogo_Empleados e
                LEFT JOIN OPS.RH_Cat_Puestos rhc ON e.ID_RHCPUESTO = rhc.ID_RHCPUESTO
                WHERE e.ACTIVO = TRUE  AND (rhc.ACTIVO = TRUE OR rhc.ID_RHCPUESTO IS NULL) 
                UNION
                SELECT e.ID_CEMPLEADO, e.NOMBRE,COALESCE(e.Pin , "NO ASIGNADO") AS N_EMPLEADO,  COALESCE(rhc.PUESTO, "") AS PUESTO
                FROM OPS.Catalogo_Empleados e
                RIGHT JOIN OPS.RH_Cat_Puestos rhc ON e.ID_RHCPUESTO = rhc.ID_RHCPUESTO
                WHERE e.ACTIVO = TRUE  AND rhc.ACTIVO = TRUE order by NOMBRE; 
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
               INSERT INTO ops.catalogo_empleados (`NOMBRE`, `FECHA_NACIMIENTO`, `GENERO`, `PROGENITOR`,  `PIN`, `CORREO`, `USUARIO`, `CLAVE`, `MAQUILADOR`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE NOMBRE=VALUES(NOMBRE);
                ''', (empleado.nombre, empleado.fecha_nacimiento, empleado.genero, empleado.progenitor, empleado.pin, empleado.correo, empleado.usuario, empleado.clave, empleado.maquilador))

                if cursor.lastrowid:
                    idEmpleado = cursor.lastrowid
                else:
                    cursor.execute('''
                    SELECT ID_CEMPLEADO FROM OPS.Catalogo_Empleados WHERE NOMBRE=%s AND PIN=%s;
                    ''', (empleado.nombre, empleado.pin))
                    empleado.idEmpleado = cursor.fetchone()[0]
                #EmpleadosT 
                cursor.execute('''
               INSERT INTO `Catalogo_EmpleadosT` (`NOMBRE`) VALUES
                VALUES (%s)
                ON DUPLICATE KEY UPDATE NOMBRE=VALUES(NOMBRE);
                ''', (empleado.nombre))

                if cursor.lastrowid:
                    idEmpleadoT = cursor.lastrowid
                else:
                    cursor.execute('''
                    SELECT ID_CEMPLEADOT FROM OPS.Catalogo_EmpleadosT WHERE NOMBRE=%s;
                    ''', (empleado.nombre))
                    empleado.idEmpleado = cursor.fetchone()[0]

                
                #INSERT Base_Sueldo  ID_CEMPLEADO
                cursor.execute('''
                INSERT INTO `OPS`.`Base_Sueldos` (`SUELDO`, `FECHA`, `ID_CEMPLEADO`)
                VALUES (%s, %s, %s);
                ''', (empleado.sueldo, empleado.fecha_inicio , idEmpleado))

                #INSERT RH_Cat_Sueldos  ID_CEMPLEADOT
                cursor.execute('''
                INSERT INTO `RH_Cat_Sueldos` (`SUELDO`,`ID_CEMPLEADO`)
                VALUES (%s, %s);
                ''', (empleado.sueldo, idEmpleadoT))
                

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

            