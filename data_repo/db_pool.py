import configparser
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config = configparser.ConfigParser()
root_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(root_dir, "db_config.ini")
config.read(config_file)


def create_engine_from_config(config_section, database):
    return create_engine(
        f"mysql+mysqldb://{config_section['user']}:{config_section['password']}@{config_section['host']}/{database}?charset={config_section['charset']}",
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )


gtfs_engine = create_engine_from_config(config["mysql"], "GTFS")
timeseries_engine = create_engine_from_config(
    config["mysql"], "GTFS_Timeseries")
ridership_engine = create_engine_from_config(config["mysql"], "GTFS_Ridership")
analyzedLines_engine = create_engine_from_config(
    config["mysql"], "AnalyzedLines")
simulation_engine = create_engine_from_config(config["mysql"], "SimulationResults")


def get_gtfs_con():
    return gtfs_engine.connect()


def get_timeseries_con():
    return timeseries_engine.connect()


def get_ridership_con():
    return ridership_engine.connect()


def get_analyzedLines_con():
    return analyzedLines_engine.connect()


def get_simulation_con():
    return simulation_engine.connect()
