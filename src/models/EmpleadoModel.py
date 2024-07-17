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
    
class EmpleadoModel:
    def __init__(self, nombre, fecha_nacimiento=None, genero=None, progenitor=None, n_empleado=None, correo=None, pin=None, 
                   usuario=None, celular=None, clave=None, maquilador=None, sueldo=None, fecha_inicio=None, id_puesto=None, id_banco=None, 
                   clave_interbancaria=None):
        
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero
        self.progenitor = progenitor
        self.n_empleado = n_empleado
        self.pin = pin
        self.correo = correo
        self.usuario = usuario
        self.celular = celular
        self.clave = clave
        self.maquilador = maquilador
        self.sueldo = sueldo
        self.fecha_inicio =  fecha_inicio
        self.id_puesto = id_puesto
        self.id_banco = id_banco
        self.clave_interbancaria = clave_interbancaria

    def __repr__(self):
        return f'<Empleado(name={self.nombre})>'

    def serialize(self):
        from src.schemas.empleadoSchema import empleado_schema   
        return empleado_schema.dump(self)

    
    