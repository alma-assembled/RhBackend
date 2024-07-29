from marshmallow import Schema, fields, post_load

class EmpleadoSchema(Schema):
    nombre = fields.Str(required=False)
    fecha_nacimiento = fields.Str(required=False)
    genero = fields.Str(required=False)
    progenitor = fields.Bool(required=False)
    correo = fields.Str(required=False, allow_none=True)
    pin = fields.Int(required=False)
    usuario = fields.Str(required=False, allow_none=True)
    celular = fields.Str(required=False, allow_none=True)
    clave = fields.Str(required=False, allow_none=True)
    maquilador = fields.Bool(required=False)
    sueldo = fields.Decimal(required=False)
    fecha_ingreso = fields.Str(required=False)
    id_puesto = fields.Int(required=False)
    id_banco = fields.Str(required=False)
    clave_interbancaria = fields.Str(required=False)
    
    @post_load
    def make_empleado(self, data, **kwargs):
        from src.models.EmpleadoModel import EmpleadoModel
        return EmpleadoModel(**data)

empleado_schema = EmpleadoSchema()
empleados_schema = EmpleadoSchema(many=True)
