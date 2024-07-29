class Empleado():

    def empleadosAll_serializers(ID_CEMPLEADO, NOMBRE, PIN,PUESTO):
        return {
            'id': ID_CEMPLEADO,
            'nombre': NOMBRE,
            'pin':PIN ,
            'puesto': PUESTO,
        }
    
    def bancos_all(id_banco, banco):
       return {
            'id': id_banco,
            'banco': banco
        }

    def puestos_all(id_puesto, puesto):
        return {
            'id': id_puesto,
            'puesto': puesto
        }
    
    def empleado_by_id_serializer( nombre, pin, correo, usuario, clave, maquilador,
                                genero, progenitor, fecha_nacimiento, celular, banco, 
                                   clave_inter, sueldo,fecha_ingreso,id_puesto):
        return {
            "nombre": nombre,
            "pin": pin,
            "correo": correo,
            "usuario": usuario,
            "clave": clave,
            "maquilador": maquilador,
            "genero": genero,
            "progenitor": progenitor,
            "fecha_nacimiento": fecha_nacimiento,
            "celular": celular,
            "id_banco": banco,
            "clave_interbancaria": clave_inter,
            "sueldo": sueldo,
            "fecha_ingreso": fecha_ingreso,
            "id_puesto": id_puesto
        }
    
    def cumpleañeros_serializers(nombre, fecha ):
        return {
            "nombre": nombre,
            "fecha": fecha
        }
    
class EmpleadoModel:
    def __init__(self, nombre=None, fecha_nacimiento=None, genero=None, progenitor=None, correo=None, pin=None, 
                   usuario=None, celular=None, clave=None, maquilador=None, sueldo=None, fecha_ingreso=None, id_puesto=None, id_banco=None, 
                   clave_interbancaria=None):
        
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.progenitor = progenitor
        self.pin = pin
        self.correo = correo
        self.usuario = usuario
        self.celular = celular
        self.clave = clave
        self.maquilador = maquilador
        self.sueldo = sueldo
        self.fecha_ingreso =  fecha_ingreso
        self.id_puesto = id_puesto
        self.id_banco = id_banco
        self.clave_interbancaria = clave_interbancaria

    def __repr__(self):
        return f'<Empleado(name={self.nombre})>'

    def serialize(self):
        from src.schemas.empleadoSchema import empleado_schema   
        return empleado_schema.dump(self)
    