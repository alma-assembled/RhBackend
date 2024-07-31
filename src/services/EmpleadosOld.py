import traceback
from flask import jsonify
# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger
from src.schemas.empleadoSchema import empleado_schema  
from src.models.EmpleadoModel import EmpleadoModel 

from src.models.EmpleadoModel import Empleado
from datetime import datetime,  date

class EmpleadosServiceOlds():

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
    def get_empleados_inactivos(cls):
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
                WHERE e.ACTIVO = FALSE  AND (rhc.ACTIVO = TRUE OR rhc.ID_RHCPUESTO IS NULL) 
                UNION
                SELECT e.ID_CEMPLEADO, e.NOMBRE,COALESCE(e.Pin , "NO ASIGNADO") AS N_EMPLEADO,  COALESCE(rhc.PUESTO, "") AS PUESTO
                FROM OPS.Catalogo_Empleados e
                RIGHT JOIN OPS.RH_Cat_Puestos rhc ON e.ID_RHCPUESTO = rhc.ID_RHCPUESTO
                WHERE e.ACTIVO = FALSE  AND rhc.ACTIVO = TRUE order by NOMBRE;  
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
    def get_empleado_by_id(cls, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''
                SELECT 
                `Catalogo_Empleados`.`ID_CEMPLEADO`,
                `Catalogo_Empleados`.`NOMBRE`,
                `Catalogo_Empleados`.`PIN`,
                `Catalogo_Empleados`.`CORREO`,
                `Catalogo_Empleados`.`USUARIO`,
                `Catalogo_Empleados`.`CLAVE`,
                `Catalogo_Empleados`.`MAQUILADOR`,
                `RH_Cat_Puestos`.`PUESTO`,
                `Catalogo_Empleados`.`GENERO`,
                `Catalogo_Empleados`.`PROGENITOR`,
                `Catalogo_Empleados`.`FECHA_NACIMIENTO`,
                `Catalogo_Empleados`.`CELULAR`,
                COALESCE(`Catalogo_Empleados`.`BANCO`, '') AS BANCO,
                COALESCE(`Catalogo_Empleados`.`CLAVE_INTERBANCARIA`, '') AS CLAVE_INTER,
                Catalogo_Empleados.ID_RHCPUESTO
                FROM
                `Catalogo_Empleados`
                JOIN `RH_Cat_Puestos` 
                ON `Catalogo_Empleados`.`ID_RHCPUESTO` = `RH_Cat_Puestos`.`ID_RHCPUESTO`
                WHERE `Catalogo_Empleados`.`ID_CEMPLEADO` = %s;
                ''', (id,))
                resultset = cursor.fetchone()

                if resultset:
                    cursor.execute('''
                        SELECT `ID_CEMPLEADOT` FROM `Catalogo_EmpleadosT` WHERE `NOMBRE`=%s;
                    ''', (resultset[1],))
                    empleado_result = cursor.fetchone()
                    id_empleadoT = empleado_result[0] if empleado_result else None
                    cursor.execute('''
                        SELECT ID_BSUELDO, SUELDO, FECHA 
                        FROM OPS.Base_Sueldos 
                        WHERE ACTIVO = TRUE 
                        AND ID_CEMPLEADOT = %s;
                    ''', (id_empleadoT,))
                    sueldo_result = cursor.fetchone()
                    sueldo = sueldo_result[1] if sueldo_result else None
                    fecha = sueldo_result[2] if sueldo_result else None

                    if isinstance(fecha, date):
                        fecha = fecha.strftime('%Y-%m-%d')
                    else:
                        fecha = datetime.strptime(fecha, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')

                    fecha_nacimiento = resultset[10]
                    if isinstance(fecha_nacimiento, str):
                        try:
                            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()  # O el formato adecuado
                        except ValueError:
                            # Manejar el caso en que la fecha no tiene el formato esperado
                            fecha_nacimiento = None
                    
                    if isinstance(fecha_nacimiento, date):
                        fecha_nacimiento = fecha_nacimiento.strftime('%Y-%m-%d')

                    
                    empleado = Empleado.empleado_by_id_serializer(
                        resultset[1], resultset[2], resultset[3],
                        resultset[4], resultset[5], resultset[6], 
                        resultset[8], resultset[9], fecha_nacimiento, resultset[11],
                        resultset[12], resultset[13], sueldo, fecha,resultset[14]
                    )
                    return empleado
                else:
                    print("No se encontró el empleado con ID:", id)
            connection.close()
            return None
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return None

    @classmethod
    def save_empleado(cls, empleado_data):
        try:
            # Deserializar datos
            empleado = empleado_schema.load(empleado_data)

            connection = get_connection()
            campos = []
            valores = []
            update_campos = []


            if empleado.nombre:
                campos.append("NOMBRE")
                valores.append(empleado.nombre.upper())
            if empleado.fecha_nacimiento:
                campos.append("FECHA_NACIMIENTO")
                valores.append(empleado.fecha_nacimiento)
            if empleado.genero:
                campos.append("GENERO")
                valores.append(empleado.genero)
            if empleado.progenitor:
                campos.append("PROGENITOR")
                valores.append(empleado.progenitor)
            if empleado.pin:
                campos.append("PIN")
                valores.append(empleado.pin)
            if empleado.correo:
                campos.append("CORREO")
                valores.append(empleado.correo)
            if empleado.usuario:
                campos.append("USUARIO")
                valores.append(empleado.usuario)
            if empleado.clave:
                campos.append("CLAVE")
                valores.append(empleado.clave)
            if empleado.maquilador:
                campos.append("MAQUILADOR")
                valores.append(empleado.maquilador)
            if empleado.id_banco:
                campos.append("BANCO")
                valores.append(empleado.id_banco)
            if empleado.clave_interbancaria:
                campos.append("CLAVE_INTERBANCARIA")
                valores.append(empleado.clave_interbancaria)
            if empleado.celular:
                campos.append("CELULAR")
                valores.append(empleado.celular)
            if empleado.id_puesto:
                campos.append("ID_RHCPUESTO")
                valores.append(empleado.id_puesto)
            campos_str = ", ".join(campos)
            valores_placeholder = ", ".join(["%s"] * len(valores))
            update_campos_str = ", ".join(update_campos)

            with connection.cursor() as cursor:

                cursor.execute('''
                SELECT ID_CEMPLEADO FROM OPS.Catalogo_Empleados WHERE NOMBRE=%s;
                ''', (empleado.nombre))
                empleado_buscar = cursor.fetchone()
                if empleado_buscar :
                    return "Empleado Existente en Sistema"  #jsonify({"message": "Empleado Existente en Sistema"})

                cursor.execute(f'''
                INSERT INTO OPS.Catalogo_Empleados ({campos_str})
                    VALUES ({valores_placeholder});
                ''', tuple(valores))
                if cursor.lastrowid:
                    idEmpleado = cursor.lastrowid
                else:
                    cursor.execute('''
                        SELECT ID_CEMPLEADO FROM OPS.Catalogo_Empleados WHERE NOMBRE=%s AND PIN=%s;
                    ''', (empleado.nombre, empleado.pin))
                    idEmpleado = cursor.fetchone()[0]

            with connection.cursor() as cursor:
                
                #EmpleadosT 
                cursor.execute('''
               INSERT INTO `Catalogo_EmpleadosT` (`NOMBRE`)
                VALUES (%s);
                ''', (empleado.nombre))

                if cursor.lastrowid:
                    idEmpleadoT = cursor.lastrowid
                else:
                    cursor.execute('''
                    SELECT ID_CEMPLEADOT FROM OPS.Catalogo_EmpleadosT WHERE NOMBRE="%s";
                    ''', (empleado.nombre))
                    empleado.idEmpleado = cursor.fetchone()[0]

                #INSERT Base_Sueldo  ID_CEMPLEADOT
                cursor.execute('''
                INSERT INTO `OPS`.`Base_Sueldos` (`SUELDO`, `FECHA`, `ID_CEMPLEADOT`)
                VALUES (%s, %s, %s);
                ''', (empleado.sueldo, empleado.fecha_ingreso , idEmpleadoT))

                #INSERT RH_Cat_Sueldos  ID_CEMPLEADOT
                cursor.execute('''
                INSERT INTO `RH_Cat_Sueldos` (`SUELDO`,`ID_CEMPLEADO`)
                VALUES (%s, %s);
                ''', (empleado.sueldo, idEmpleado))
                

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
                # Actualizar el registro del empleado en `Catalogo_Empleados`
                cursor.execute('''
                    UPDATE `OPS`.`Catalogo_Empleados` SET `ACTIVO` = '0' WHERE `ID_CEMPLEADO` = %s;
                ''', (id_empleado,))

                # Actualizar el sueldo del empleado en `RH_Cat_Sueldos`
                cursor.execute('''
                    UPDATE `RH_Cat_Sueldos` SET `ACTIVO` = '0' WHERE ID_CEMPLEADO = %s AND ACTIVO = 1;
                ''', (id_empleado,))
                
                # Obtener ID_CEMPLEADOT.
                print(f"Executing SELECT query with id_empleado: {id_empleado}")
                cursor.execute(f'''
                    SELECT ET.ID_CEMPLEADOT 
                    FROM OPS.Catalogo_EmpleadosT ET
                    JOIN OPS.Catalogo_Empleados E ON E.NOMBRE = ET.NOMBRE 
                    WHERE E.ID_CEMPLEADO = {id_empleado} AND E.ACTIVO = TRUE AND ET.ACTIVO = TRUE;
                ''')
                result = cursor.fetchone()
                print(f'''
                    SELECT ET.ID_CEMPLEADOT 
                    FROM OPS.Catalogo_EmpleadosT ET
                    JOIN OPS.Catalogo_Empleados E ON E.NOMBRE = ET.NOMBRE 
                    WHERE E.ID_CEMPLEADO = {id_empleado} AND E.ACTIVO = TRUE AND ET.ACTIVO = TRUE;
                ''')
                if result:
                    id_empleadoT = result[0]
                    print(f"ID_CEMPLEADOT recuperado: {id_empleadoT}")
                    # Actualizar el registro del empleado en `Catalogo_EmpleadosT`
                    
                    cursor.execute('''
                        UPDATE `OPS`.`Catalogo_EmpleadosT` SET `ACTIVO` = '0' WHERE `ID_CEMPLEADOT` = %s;
                    ''', (id_empleadoT,))


                    # Actualizar el sueldo del empleado en `Base_Sueldos`
                    cursor.execute('''
                        UPDATE `OPS`.`Base_Sueldos` SET `ACTIVO` = '0' WHERE ID_CEMPLEADOT = %s AND ACTIVO = 1;
                    ''', (id_empleadoT,))
                else:
                    print("No se encontró ningún EmpleadoT.")

                
            connection.commit()
            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False
        finally:
            connection.close()

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
            SELECT ID_CBANCO, BANCO FROM OPS.Catalogo_Bancos WHERE ACTIVO= TRUE order by BANCO; 
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

    @classmethod
    def update_empleado(cls, id_empleado, empleado_data):
        try:
            # Validar datos
            empleado = empleado_schema.load(empleado_data)

            connection = get_connection()
            set_clause = []
            values = []

            if empleado.nombre is not None:
                set_clause.append("NOMBRE = %s")
                values.append(empleado.nombre)
            if empleado.pin is not None:
                set_clause.append("PIN = %s")
                values.append(empleado.pin)
            if empleado.fecha_nacimiento is not None:
                set_clause.append("FECHA_NACIMIENTO = %s")
                values.append(empleado.fecha_nacimiento)
            if empleado.genero is not None:
                set_clause.append("GENERO = %s")
                values.append(empleado.genero)
            if empleado.progenitor is not None:
                set_clause.append("PROGENITOR = %s")
                values.append(empleado.progenitor)
            if empleado.correo is not None:
                set_clause.append("CORREO = %s")
                values.append(empleado.correo)
            if empleado.usuario is not None:
                set_clause.append("USUARIO = %s")
                values.append(empleado.usuario)
            if empleado.celular is not None:
                set_clause.append("CELULAR = %s")
                values.append(empleado.celular)
            if empleado.clave is not None:
                set_clause.append("CLAVE = %s")
                values.append(empleado.clave)
            if empleado.maquilador is not None:
                set_clause.append("MAQUILADOR = %s")
                values.append(empleado.maquilador)
            if empleado.id_banco is not None:
                set_clause.append("BANCO = %s")
                values.append(empleado.id_banco)
            if empleado.clave_interbancaria is not None:
                set_clause.append("CLAVE_INTERBANCARIA = %s")
                values.append(empleado.clave_interbancaria)
            if empleado.id_puesto is not None:
                set_clause.append("ID_RHCPUESTO = %s")
                values.append(empleado.id_puesto)
                

            if not set_clause:
                raise ValueError("nada para actualizar")

            set_clause_str = ", ".join(set_clause)
            values.append(id_empleado)

            with connection.cursor() as cursor:
                cursor.execute(f'''
                    UPDATE OPS.Catalogo_Empleados
                    SET {set_clause_str}
                    WHERE ID_CEMPLEADO = %s;
                ''', tuple(values))

                # Actualizar campos en la tabla OPS.Base_Sueldos  
                if empleado.sueldo is not None:
                    #id EmpleadoT
                    cursor.execute('''
                        SELECT ID_CEMPLEADOT FROM OPS.Catalogo_EmpleadosT ET, OPS.Catalogo_Empleados E
                        where E.ID_CEMPLEADO = '%s' AND E.NOMBRE  = ET.NOMBRE AND E.ACTIVO = 1 AND ET.ACTIVO =1 ;
                        ''', (id_empleado))
                    if cursor.fetchone() :
                        id_empleadoT = cursor.fetchone()[0]
                        # Verificar si el sueldo ha cambiado
                        cursor.execute('''
                            SELECT SUELDO FROM OPS.Base_Sueldos WHERE ID_CEMPLEADOT = %s AND ACTIVO = 1;
                        ''', (id_empleadoT,))
                        current_sueldo = cursor.fetchone()

                        if float(current_sueldo[0]) != float(empleado.sueldo):
                            # Actualizar sueldo en la tabla OPS.Base_Sueldos
                            cursor.execute('''
                                UPDATE OPS.Base_Sueldos
                                SET ACTIVO= False
                                WHERE ID_CEMPLEADOT = %s;
                            ''', (empleado.sueldo, id_empleadoT))
                            # Actualizar sueldo en la tabla RH_Cat_Sueldos (con ID_CEMPLEADOT)
                            cursor.execute('''
                                UPDATE RH_Cat_Sueldos
                                SET ACTIVO=FALSE
                                WHERE ID_CEMPLEADO = %s;
                            ''', (empleado.sueldo, id_empleado))

                            #INSERT Base_Sueldo  ID_CEMPLEADOT
                            cursor.execute('''
                            INSERT INTO `OPS`.`Base_Sueldos` (`SUELDO`, `FECHA`, `ID_CEMPLEADOT`)
                            VALUES (%s, %s, %s);
                            ''', (empleado.sueldo, empleado.fecha_ingreso , id_empleadoT))

                            #INSERT RH_Cat_Sueldos  ID_CEMPLEADOT
                            cursor.execute('''
                            INSERT INTO `RH_Cat_Sueldos` (`SUELDO`,`ID_CEMPLEADO`)
                            VALUES (%s, %s);
                            ''', (empleado.sueldo, id_empleado))

            connection.commit()
            connection.close()

            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False
    
    @classmethod
    def get_resumen(cls ):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT COUNT( NOMBRE) TOTAL FROM OPS.Catalogo_Empleados WHERE ACTIVO = 1;
                ''')
                total_empleados = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT COUNT( NOMBRE ) TOTAL FROM OPS.Catalogo_Empleados 
                        WHERE ACTIVO = 1 AND ID_RHCPUESTO=17;
                ''')
                total_maquiladores = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT COUNT( NOMBRE ) TOTAL FROM OPS.Catalogo_Empleados 
                    WHERE ACTIVO = 1 AND ID_RHCPUESTO=17 AND GENERO="H";
                ''')
                total_maquiladores_mujeres = cursor.fetchone()[0]

                cursor.execute('''
                    SELECT COUNT( NOMBRE ) TOTAL FROM OPS.Catalogo_Empleados 
                        WHERE ACTIVO = 1 AND ID_RHCPUESTO=17 AND GENERO="M";
                ''')
                total_maquiladores_hombres = cursor.fetchone()[0]

                
            return {
                "total_empleados": total_empleados,
                "total_maquiladores": total_maquiladores,
                "maquiladores_mujeres":total_maquiladores_mujeres,
                "maquiladores_hombres":total_maquiladores_hombres
            }
        
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def get_cumpleaños_mes(cls):
        cumpleaneros= []
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT 
                        ID_CEMPLEADO, 
                        NOMBRE, 
                        DATE_FORMAT(FECHA_NACIMIENTO, '%d %M') AS DIA_MES_NACIMIENTO
                    FROM 
                        OPS.Catalogo_Empleados 
                    WHERE 
                        ACTIVO = 1 
                        AND MONTH(FECHA_NACIMIENTO) = MONTH(CURRENT_DATE);
                ''')
                cumpleaños = cursor.fetchall()
                for row in cumpleaños:
                    empleado = Empleado.cumpleañeros_serializers(row[1], row[2])
                    cumpleaneros.append(empleado)
            connection.close()
            return cumpleaños
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def update_reingreso(cls, id_empleado, empleado_data):
        try:
            # Validar datos
            empleado = empleado_schema.load(empleado_data)

            connection = get_connection()
            set_clause = []
            values = []

            if empleado.nombre is not None:
                set_clause.append("NOMBRE = %s")
                values.append(empleado.nombre)
            if empleado.pin is not None:
                set_clause.append("PIN = %s")
                values.append(empleado.pin)
            if empleado.fecha_nacimiento is not None:
                set_clause.append("FECHA_NACIMIENTO = %s")
                values.append(empleado.fecha_nacimiento)
            if empleado.genero is not None:
                set_clause.append("GENERO = %s")
                values.append(empleado.genero)
            if empleado.progenitor is not None:
                set_clause.append("PROGENITOR = %s")
                values.append(empleado.progenitor)
            if empleado.correo is not None:
                set_clause.append("CORREO = %s")
                values.append(empleado.correo)
            if empleado.usuario is not None:
                set_clause.append("USUARIO = %s")
                values.append(empleado.usuario)
            if empleado.celular is not None:
                set_clause.append("CELULAR = %s")
                values.append(empleado.celular)
            if empleado.clave is not None:
                set_clause.append("CLAVE = %s")
                values.append(empleado.clave)
            if empleado.maquilador is not None:
                set_clause.append("MAQUILADOR = %s")
                values.append(empleado.maquilador)
            if empleado.id_banco is not None:
                set_clause.append("BANCO = %s")
                values.append(empleado.id_banco)
            if empleado.clave_interbancaria is not None:
                set_clause.append("CLAVE_INTERBANCARIA = %s")
                values.append(empleado.clave_interbancaria)
            if empleado.id_puesto is not None:
                set_clause.append("ID_RHCPUESTO = %s")
                values.append(empleado.id_puesto)
                

            if not set_clause:
                raise ValueError("nada para actualizar")

            set_clause_str = ", ".join(set_clause)
            values.append(id_empleado)

            with connection.cursor() as cursor:
                cursor.execute(f'''
                    UPDATE OPS.Catalogo_Empleados
                    SET {set_clause_str} , ACTIVO = TRUE
                    WHERE ID_CEMPLEADO = %s;
                ''', tuple(values))

                #id EmpleadoT
                cursor.execute('''
                    SELECT ID_CEMPLEADOT FROM OPS.Catalogo_EmpleadosT ET, OPS.Catalogo_Empleados E
                    where E.ID_CEMPLEADO = '%s' AND E.NOMBRE  = ET.NOMBRE;
                    ''', (id_empleado))
                id_empleadoT = cursor.fetchone()[0]
                cursor.execute(f'''
                    UPDATE OPS.Catalogo_EmpleadosT
                    SET NOMBRE = %s, ACTIVO = TRUE
                    WHERE ID_CEMPLEADOT = %s;
                ''', (empleado.nombre, id_empleadoT))
                
                #INSERT Base_Sueldo  ID_CEMPLEADOT
                cursor.execute('''
                INSERT INTO `OPS`.`Base_Sueldos` (`SUELDO`, `FECHA`, `ID_CEMPLEADOT`)
                VALUES (%s, %s, %s);
                ''', (empleado.sueldo, empleado.fecha_ingreso , id_empleadoT))
                #INSERT RH_Cat_Sueldos  ID_CEMPLEADOT
                cursor.execute('''
                INSERT INTO `RH_Cat_Sueldos` (`SUELDO`,`ID_CEMPLEADO`)
                VALUES (%s, %s);
                ''', (empleado.sueldo, id_empleado))

            connection.commit()
            connection.close()

            return True
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False
    