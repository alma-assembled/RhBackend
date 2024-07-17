from decouple import config

import datetime
import jwt
import pytz
import traceback

# Logger
from src.utils.Logger import Logger


class Security():

    secret = config('JWT_KEY')
    tz = pytz.timezone("America/Mexico_City")

    @classmethod
    def generate_token(cls, authenticated_user):
        try:
            payload = {
                'iat': datetime.datetime.now(tz=cls.tz),
                'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(days=3),
                'username': authenticated_user.username,
                'fullname': authenticated_user.nombre,
                'roles': ['Administrator', 'Editor']
            }
            return jwt.encode(payload, cls.secret, algorithm="HS256")
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def verify_token(cls, headers):
        try:
            if 'Authorization' in headers:
                authorization = headers['Authorization']
                encoded_token = authorization.split(" ")[1]  # Obtiene el token JWT codificado
                if len(encoded_token) > 0 and encoded_token.count('.') == 2:
                    try:
                        # Decodifica el token JWT usando la clave secreta
                        payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                        roles = payload.get('roles', [])

                        # Verifica si el rol 'Administrator' está presente en los roles del payload
                        if 'Administrator' in roles:
                            return True
                        else:
                            return False
                    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as e:
                        # Captura de errores relacionados con la firma del token JWT
                        Logger.add_to_log(f"Error decoding token: {str(e)}")
                        return False
                else:
                    Logger.add_to_log("Invalid token format")
                    return False
            else:
                Logger.add_to_log("Authorization header not found")
                return False
        except Exception as ex:
            # Manejo de excepciones generales y registro en el logger
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            return False

    