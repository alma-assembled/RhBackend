import unittest
from app import create_app, db
from app.models import Empleado
from flask_testing import TestCase

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class EmpleadoTestCase(BaseTestCase):
    def test_create_empleado(self):
        response = self.client.post('/empleados', json={
            'nombre': 'John Doe',
            'fecha_nacimiento': '1990-01-01',
            'genero': 'M',
            'progenitor': 'Jane Doe',
            'pin': '1234',
            'correo': 'johndoe@example.com',
            'usuario': 'jdoe',
            'clave': 'password',
            'maquilador': 'ABC Corp',
            'id_banco': 1,
            'clave_interbancaria': '123456789012345678',
            'celular': '555-5555',
            'id_puesto': 1,
            'sueldo': 50000,
            'fecha_ingreso': '2020-01-01'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Empleado creado exitosamente', response.json['message'])

    def test_update_empleado(self):
        response = self.client.post('/empleados', json={
            'nombre': 'John Doe',
            'fecha_nacimiento': '1990-01-01',
            'genero': 'M',
            'progenitor': 'Jane Doe',
            'pin': '1234',
            'correo': 'johndoe@example.com',
            'usuario': 'jdoe',
            'clave': 'password',
            'maquilador': 'ABC Corp',
            'id_banco': 1,
            'clave_interbancaria': '123456789012345678',
            'celular': '555-5555',
            'id_puesto': 1,
            'sueldo': 50000,
            'fecha_ingreso': '2020-01-01'
        })
        empleado_id = response.json['id']

        response = self.client.put(f'/empleados/{empleado_id}', json={
            'nombre': 'John Doe Updated',
            'sueldo': 60000
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Empleado actualizado correctamente', response.json['message'])

    def test_delete_empleado(self):
        response = self.client.post('/empleados', json={
            'nombre': 'John Doe',
            'fecha_nacimiento': '1990-01-01',
            'genero': 'M',
            'progenitor': 'Jane Doe',
            'pin': '1234',
            'correo': 'johndoe@example.com',
            'usuario': 'jdoe',
            'clave': 'password',
            'maquilador': 'ABC Corp',
            'id_banco': 1,
            'clave_interbancaria': '123456789012345678',
            'celular': '555-5555',
            'id_puesto': 1,
            'sueldo': 50000,
            'fecha_ingreso': '2020-01-01'
        })
        empleado_id = response.json['id']

        response = self.client.delete(f'/empleados/{empleado_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Empleado eliminado correctamente', response.json['message'])

if __name__ == '__main__':
    unittest.main()
