import logging
import pandas as pd
from FinalProjectSimulator.data_repo.db_pool import get_ridership_con


logger = logging.getLogger(__name__)


def get_stations_passengers_by_day(line_id: str, day: int) -> pd.DataFrame | None:
    try:
        day_mapped = map_days(day)
        sql_query = f"SELECT `תחנה`, `שם תחנה`, `סידורי תחנה`, `{day_mapped}` FROM `{line_id}` ORDER BY `סידורי תחנה`"
        with get_ridership_con() as conn:
            df = pd.read_sql(sql_query, conn)
            return df
    except Exception as e:
        logger.error(e)
        raise e


def get_all_stations(line_id: str) -> pd.DataFrame | None:
    try:
        sql_query = f"SELECT `תחנה`, `שם תחנה`, `סידורי תחנה` FROM `{line_id}` ORDER BY `סידורי תחנה`"
        with get_ridership_con() as conn:
            df = pd.read_sql(sql_query, conn)
            return df
    except Exception as e:
        logger.error(e)
        raise e


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
