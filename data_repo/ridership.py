from FinalProjectSimulator.models.simulation import Simulation
from db_pool import get_ridership_con


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
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
