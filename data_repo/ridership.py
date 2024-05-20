import mysql.connector
import configparser
#from ..models.simulation import Simulation


def fetch_ridership_data_by_primary_key(simulation: str, station_id: str):
    config = configparser.ConfigParser()
    config.read("FinalProjectSimulator\data_repo\db_config.ini")

    host = config["mysql"]["host"]
    user = config["mysql"]["user"]
    password = config["mysql"]["password"]
    charset = config["mysql"]["charset"]
    database = "GTFS_Ridership"

    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host=host, user=user, password=password, database=database, charset=charset
    )

    try:
        with connection.cursor() as cursor:
            station = int(station_id)
            sql_query = f"SELECT * FROM {simulation} WHERE `תחנה` = %d"
            cursor.execute(sql_query, (station,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    simulation = "10003-1-#"
    data = fetch_ridership_data_by_primary_key(simulation, "42328")
    
    for row in data:
        print(row)

    