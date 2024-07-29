from decouple import config

import pymysql
import traceback

# Logger
from src.utils.Logger import Logger


def get_connection():
    try:
        print(config('MYSQLL_HOST'), ";", config('MYSQLL_USER') ,";",config('MYSQLL_PASSWORD'),";",config('MYSQLL_DB'))
        return pymysql.connect(
            host=config('MYSQLL_HOST'),
            user=config('MYSQLL_USER'),
            password=config('MYSQLL_PASSWORD'),
            db=config('MYSQLL_DB')
        )
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())