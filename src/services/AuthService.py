import traceback

# Database
from src.database.connection import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.UsuarioModel import Usuario


class AuthService():

    @classmethod
    def login_user(cls, user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM OPS.Catalogo_Empleados where USUARIO=%s and CLAVE=%s;", (user.username, user.password))
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = Usuario(int(row[0]), row[5], None, row[2])
            connection.close()
            return authenticated_user
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())