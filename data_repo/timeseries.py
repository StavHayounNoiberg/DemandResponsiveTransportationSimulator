import logging
import pandas as pd
from FinalProjectSimulator.data_repo.db_pool import get_timeseries_con


logger = logging.getLogger(__name__)


def get_timeseries_data_by_primary_key(
    full_line_id: str, day: int, data_type: str
) -> pd.DataFrame | None:
    try:
        line_parts = full_line_id.split("-")
        line_id = line_parts[0]
        extended_line_id = "-".join(line_parts[:2])
        day_mapped = map_days(day)
        data_type = map_data_type(data_type)
        with get_timeseries_con() as conn:
            sql_query = f"SELECT * FROM `{line_id}` WHERE `קו` = '{extended_line_id}' AND `סוג יום` = '{day_mapped}' AND ` חתך` = '{data_type}'"
            df = pd.read_sql(sql_query, conn)
            return df
    except Exception as e:
        logger.error(e)
        raise e


def map_days(day: int) -> str:
    return {
        1: "ראשון",
        2: "שני",
        3: "שלישי",
        4: "רביעי",
        5: "חמישי",
        6: "שישי",
        7: "שבת",
    }.get(day)


def map_data_type(data_type: str) -> str:
    return {
        "buses": "נסיעות אוטובוס",
        "passengers": "עליות נוסע",
    }.get(data_type)
