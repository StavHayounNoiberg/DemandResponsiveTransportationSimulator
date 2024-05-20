from FinalProjectSimulator.models.simulation import Simulation
from db_pool import get_timeseries_con


def fetch_timeseries_data_by_primary_key(
    simulation: Simulation, day: int, data_type: str
) -> list | None:
    try:
        line_parts = simulation.line_id.split("-")
        line_id = line_parts[0]
        extended_line_id = "-".join(line_parts[:2])
        day = map_days(day)
        data_type = map_data_type(data_type)
        conn = get_timeseries_con()
        with conn.cursor() as cursor:
            sql_query = f"SELECT * FROM `{line_id}` WHERE `קו` = %s AND `סוג יום` = %s AND ` חתך` = %s"
            cursor.execute(sql_query, (extended_line_id, day, data_type))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()


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
