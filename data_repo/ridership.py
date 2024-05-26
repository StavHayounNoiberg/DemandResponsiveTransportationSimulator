import logging
from FinalProjectSimulator.models.simulation import Simulation
from db_pool import get_ridership_con
import pandas as pd


logger = logging.getLogger(__name__)


def fetch_ridership_data_by_primary_key(
    simulation: Simulation, station_id: str
) -> list | None:
    try:
        station = int(station_id)
        conn = get_ridership_con()
        with conn.cursor() as cursor:
            sql_query = f"SELECT * FROM `{simulation.line_id}` WHERE `תחנה` = %s"
            cursor.execute(sql_query, (station,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        logger.error(e)
    finally:
        if conn.is_connected():
            conn.close()


def fetch_stations_passengers_by_day(
    simulation: Simulation, day: int
) -> pd.DataFrame | None:
    try:
        line_id = simulation.line_id
        day = map_days(day)
        conn = get_ridership_con()
        sql_query = f"SELECT `תחנה`, `שם תחנה`, `סידורי תחנה`, `{day}` FROM `{line_id}`"
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
