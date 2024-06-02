import logging
import pandas as pd
from FinalProjectSimulator.data_repo.db_pool import get_gtfs_con


logger = logging.getLogger(__name__)


def get_stop_codes_and_arrival_times(trip_id: str) -> pd.DataFrame | None:
    try:
        sql_query = f"SELECT stops.stop_code, stopTimes.arrival_time
        FROM stopTimes
        JOIN stops ON stopTimes.stop_id = stops.stop_id
        WHERE SUBSTRING_INDEX(stopTimes.trip_id, '_', 1) = '{trip_id}'"
        with get_gtfs_con() as conn:
            df = pd.read_sql(sql_query, conn)
            return df
    except Exception as e:
        logger.error(e)
        return None


def get_stop_location(stop_code: str) -> tuple[float, float] | None:
    try:
        sql_query = f"SELECT stop_lat, stop_lon FROM stops WHERE stop_code = '{stop_code}'"
        with get_gtfs_con() as conn:
            df = pd.read_sql(sql_query, conn)
            num_rows = df.shape[0]
            if num_rows == 0:
                logger.error("No location found for stop code %s", stop_code)
                return None
            elif num_rows > 1:
                logger.warning(
                    "More than one location found for stop code %s", stop_code)
            return df.iloc[0].values
    except Exception as e:
        logger.error(e)
        return None


def get_trip_ids_and_departure_times(full_line_id: str, day: int) -> pd.DataFrame | None:
    try:
        line_id = full_line_id.split("-")[0]
        sql_query = f"SELECT `TripId`, `DepartureTime` FROM tripIdToDate WHERE `OfficeLineId` = '{line_id}' AND DATE(`ToDate`) = '2200-01-01' AND `DayInWeek` = {day}"
        with get_gtfs_con() as conn:
            df = pd.read_sql(sql_query, conn)
            return df
    except Exception as e:
        logger.error(e)
        return None
