from datetime import datetime
import logging
import pandas as pd
from FinalProjectSimulator.data_repo.db_pool import get_gtfs_con
from FinalProjectSimulator.utilities.datetime_utils import get_day_number


logger = logging.getLogger(__name__)


def get_stop_codes_and_arrival_times(trip_id: str) -> pd.DataFrame | None:
    try:
        sql_query = f'''SELECT stops.stop_code, stopTimes.arrival_time
        FROM stopTimes
        JOIN stops ON stopTimes.stop_id = stops.stop_id
        WHERE stopTimes.trip_id_prefix = '{trip_id}'
        '''
        with get_gtfs_con() as conn:
            df = pd.read_sql(sql_query, conn)
            df = df.drop_duplicates(subset=['stop_code'])
            return df
    except Exception as e:
        logger.error(e)
        return None


def get_stop_location(stop_code: str) -> tuple[float, float] | None:
    try:
        sql_query = f"SELECT stop_lat, stop_lon FROM stops WHERE stop_code = {stop_code}"
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


def get_trip_ids_and_departure_times(full_line_id: str, date: datetime) -> pd.DataFrame | None:
    try:
        line_id_parts = full_line_id.split("-")
        day = get_day_number(date)
        time = date.time()
        sql_query = f'''SELECT `TripId`, `DepartureTime` 
        FROM tripIdToDate 
        WHERE `OfficeLineId` = '{line_id_parts[0]}' 
        AND `Direction` = '{line_id_parts[1]}' 
        AND `LineAlternative` = '{line_id_parts[2]}' 
        AND DATE(`ToDate`) = '2200-01-01' 
        AND `DayInWeek` = {day}
        AND `DepartureTime` >= '{time}'
        '''
        with get_gtfs_con() as conn:
            df = pd.read_sql(sql_query, conn)

            # Convert `DepartureTime` from timedelta to datetime
            base_date = date.date()
            df['DepartureTime'] = df['DepartureTime'].apply(lambda td: datetime.combine(base_date, datetime.min.time()) + td)
            
            return df
        
    except Exception as e:
        logger.error(e)
        return None
