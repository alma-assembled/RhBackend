from marshmallow import Schema, fields, post_load

class EmpleadoSchema(Schema):
    nombre = fields.Str(required=True)
    fecha_nacimiento = fields.Date(required=False)
    genero = fields.Str(required=True)
    progenitor = fields.Bool(required=True)
    n_empleado = fields.Str(required=False)
    correo = fields.Email(required=False)
    pin = fields.Int(required=False)
    usuario = fields.Str(required=False)
    celular = fields.Str(required=False)
    clave = fields.Str(required=False)
    maquilador = fields.Bool(required=True)
    sueldo = fields.Decimal(required=True)
    fecha_inicio = fields.Str(required=True)
    id_puesto = fields.Int(required=True)
    id_banco = fields.Int(required=True)
    clave_interbancaria = fields.Str(required=True)
    
    @post_load
    def make_empleado(self, data, **kwargs):
        from src.models.EmpleadoModel import EmpleadoModel
        return EmpleadoModel(**data)

empleado_schema = EmpleadoSchema()
empleados_schema = EmpleadoSchema(many=True)
