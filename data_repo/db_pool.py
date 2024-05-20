import configparser
import mysql.connector


config = configparser.ConfigParser()
config.read("db_config.ini")

gtfs_dbconfig = {
    "user": config["mysql"]["user"],
    "password": config["mysql"]["password"],
    "host": config["mysql"]["host"],
    "database": "GTFS",
    "charset": config["mysql"]["charset"],
}

timeseries_dbconfig = {
    "user": config["mysql"]["user"],
    "password": config["mysql"]["password"],
    "host": config["mysql"]["host"],
    "database": "GTFS_Timeseries",
    "charset": config["mysql"]["charset"],
}

ridership_dbconfig = {
    "user": config["mysql"]["user"],
    "password": config["mysql"]["password"],
    "host": config["mysql"]["host"],
    "database": "GTFS_Ridership",
    "charset": config["mysql"]["charset"],
}

analyzedLines_dbconfig = {
    "user": config["mysql"]["user"],
    "password": config["mysql"]["password"],
    "host": config["mysql"]["host"],
    "database": "AnalyzedLines",
    "charset": config["mysql"]["charset"],
}

simulation_dbconfig = {
    "user": config["mysql"]["user"],
    "password": config["mysql"]["password"],
    "host": config["mysql"]["host"],
    "database": "simulation",
    "charset": config["mysql"]["charset"],
}

gtfs_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="gtfs_pool", **gtfs_dbconfig
)
timeseries_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="timeseries_pool", **timeseries_dbconfig
)
ridership_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="ridership_pool", **ridership_dbconfig
)
analyzedLines_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="analyzedLines_pool", **analyzedLines_dbconfig
)
# simulation_pool = mysql.connector.pooling.MySQLConnectionPool(
#     pool_name="simulation_pool", **simulation_dbconfig
# )


def get_gtfs_con():
    return gtfs_pool.get_connection()


def get_timeseries_con():
    return timeseries_pool.get_connection()


def get_ridership_con():
    return ridership_pool.get_connection()


def get_analyzedLines_con():
    return analyzedLines_pool.get_connection()


# def get_simulation_con():
#     return simulation_pool.get_connection()
