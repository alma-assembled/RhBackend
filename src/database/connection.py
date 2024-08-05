from decouple import config

import pymysql
import traceback

# Logger
from src.utils.Logger import Logger


def get_connection():
    try:
        #print(config('MYSQL_HOST'), ";", config('MYSQL_USER') ,";",config('MYSQL_PASSWORD'),";",config('MYSQL_DB'))
        return pymysql.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB')
        )
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())