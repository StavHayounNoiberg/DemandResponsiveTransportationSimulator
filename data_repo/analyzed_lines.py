from datetime import datetime
import logging
import pandas as pd
from FinalProjectSimulator.data_repo.db_pool import get_analyzedLines_con
from FinalProjectSimulator.utilities.datetime_utils import get_day_number


logger = logging.getLogger(__name__)


def get_green_stations(line_id: str, leave_time: datetime) -> pd.DataFrame | None:
    try:
        day_mapped = map_days(get_day_number(leave_time))
        day_column_name = f"{day_mapped} {leave_time.hour}"
        sql_query = f"SELECT `תחנה` , `סידורי תחנה` FROM `{line_id}` WHERE `{day_column_name}` >= 0.3 ORDER BY `סידורי תחנה`"
        with get_analyzedLines_con() as conn:
            df = pd.read_sql(sql_query, conn)
            return df
    except Exception as e:
        logger.error(e)
        return None


def map_days(day: int) -> str:
    return {
        1: "ממוצע יום א",
        2: "ממוצע יום ב",
        3: "ממוצע יום ג",
        4: "ממוצע יום ד",
        5: "ממוצע יום ה",
        6: "ממוצע יום ו",
        7: "ממוצע יום שבת",
    }.get(day)
