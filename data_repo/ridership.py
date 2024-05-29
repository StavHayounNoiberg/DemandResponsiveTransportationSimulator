import logging
import pandas as pd
from FinalProjectSimulator.data_repo.db_pool import get_ridership_con


logger = logging.getLogger(__name__)


def fetch_ridership_data_by_primary_key(line_id: str, station_id: str) -> list | None:
    conn = get_ridership_con()
    try:
        station = int(station_id)
        with conn.cursor() as cursor:
            sql_query = f"SELECT * FROM `{line_id}` WHERE `תחנה` = %s"
            cursor.execute(sql_query, (station,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        logger.error(e)
    finally:
        if conn.is_connected():
            conn.close()


def fetch_stations_passengers_by_day(line_id: str, day: int) -> pd.DataFrame | None:
    conn = get_ridership_con()
    try:
        day = map_days(day)
        sql_query = f"SELECT `תחנה`, `שם תחנה`, `סידורי תחנה`, `{day}` FROM `{line_id}` ORDER BY `סידורי תחנה`"
        df = pd.read_sql(sql_query, conn)
        return df
    except Exception as e:
        logger.error(e)
    finally:
        if conn.is_connected():
            conn.close()


def fetch_all_stations(line_id: str) -> pd.DataFrame | None:
    conn = get_ridership_con()
    try:
        sql_query = f"SELECT `תחנה`, `שם תחנה`, `סידורי תחנה` FROM `{line_id}` ORDER BY `סידורי תחנה`"
        df = pd.read_sql(sql_query, conn)
        return df
    except Exception as e:
        logger.error(e)
    finally:
        if conn.is_connected():
            conn.close()


def map_days(day: int) -> str:
    return {
        0: "ממוצע שבועי",
        1: "ממוצע יום א",
        2: "ממוצע יום ב",
        3: "ממוצע יום ג",
        4: "ממוצע יום ד",
        5: "ממוצע יום ה",
        6: "ממוצע יום ו",
        7: "ממוצע יום שבת",
    }.get(day)
