import logging
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from FinalProjectSimulator.data_repo.db_pool import get_simulation_con
from FinalProjectSimulator.models.simulation_analysis import SimulationAnalysis


logger = logging.getLogger(__name__)

Base = declarative_base()


class SimulationData(Base):
    __tablename__ = 'Simulations'
    simulation_id = Column(String(255), primary_key=True)
    line_id = Column(String(50))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    express_rate = Column(Float)
    reporting_rate = Column(Float)
    started_at = Column(DateTime)
    duration_in_mins = Column(Float)
    success = Column(Boolean)

    def __init__(self, simulation: "Simulation"):
        self.simulation_id = simulation.id
        self.line_id = simulation.line_id
        self.start_time = simulation.start_time
        self.end_time = simulation.end_time
        self.express_rate = simulation.express_rate
        self.reporting_rate = simulation.reporting_rate
        self.started_at = simulation.started_at
        self.duration_in_mins = simulation.duration.total_seconds() / 60
        self.success = simulation.success


class BusData(Base):
    __tablename__ = 'Buses'
    simulation_id = Column(String(255), primary_key=True)
    bus_id = Column(Integer, primary_key=True)
    is_express = Column(Boolean)
    leave_time = Column(DateTime)
    final_dest_arrival_time = Column(DateTime)
    route = Column(JSON)
    passengers_enroute = Column(JSON)

    def __init__(self, simulation_id, bus: "Bus"):
        self.simulation_id = simulation_id
        self.bus_id = bus.id
        self.is_express = type(bus) is ExpressBus
        self.leave_time = bus.leave_time
        self.final_dest_arrival_time = bus.route[-1][1]
        self.route = bus.prepare_route_for_json()
        self.passengers_enroute = bus.prepare_passengers_enroute_for_json()


class PassengerData(Base):
    __tablename__ = 'Passengers'
    simulation_id = Column(String(255), primary_key=True)
    passenger_id = Column(Integer, primary_key=True)
    stop_src = Column(Integer)
    stop_dest = Column(Integer)
    reporting_time = Column(DateTime)
    leaving_time = Column(DateTime)
    aboard_time = Column(DateTime)
    arrival_time = Column(DateTime)
    bus_id = Column(String(50))
    assignment_reason = Column(Integer)

    def __init__(self, simulation_id, passenger: "Passenger"):
        self.simulation_id = simulation_id
        self.passenger_id = passenger.id
        self.stop_src = passenger.stop_src.ordinal_number
        self.stop_dest = passenger.stop_dest.ordinal_number
        self.reporting_time = passenger.reporting_time
        self.leaving_time = passenger.leaving_time
        self.aboard_time = passenger.aboard_time
        self.arrival_time = passenger.arrival_time
        self.bus_id = passenger.bus.id if passenger.bus is not None else -1
        self.assignment_reason = passenger.assignment_reason.value if passenger.assignment_reason is not None else -1


class AnalysisData(Base):
    __tablename__ = 'Analysis'
    analysis_id = Column(String(255), primary_key=True)
    line_id = Column(String(50))
    report_rate = Column(Float)
    express_rate = Column(Float)
    avg_passenger_travel_time = Column(Float)
    avg_passenger_travel_time_percent = Column(Float)
    avg_bus_travel_time = Column(Float)
    avg_bus_travel_time_percent = Column(Float)
    avg_passenger_waiting_time = Column(Float)
    avg_passenger_waiting_time_percent = Column(Float)
    rejected_passengers = Column(Integer)
    passengers_in_assignment = Column(JSON)

    def __init__(self, analysis_data: "SimulationAnalysis"):
        self.analysis_id = analysis_data.id
        self.line_id = analysis_data.line_id
        self.report_rate = analysis_data.report_rate
        self.express_rate = analysis_data.express_rate
        self.avg_passenger_travel_time = analysis_data.avg_passenger_travel_time
        self.avg_passenger_travel_time_percent = analysis_data.avg_passenger_travel_time_percent
        self.avg_bus_travel_time = analysis_data.avg_bus_travel_time
        self.avg_bus_travel_time_percent = analysis_data.avg_bus_travel_time_percent
        self.avg_passenger_waiting_time = analysis_data.avg_passenger_waiting_time
        self.avg_passenger_waiting_time_percent = analysis_data.avg_passenger_waiting_time_percent
        self.rejected_passengers = analysis_data.rejected_passengers
        self.passengers_in_assignment = analysis_data.passengers_in_assignment


engine = get_simulation_con()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, future=True)


def save_simulation(simulation: "Simulation"):
    session = Session()
    try:
        simulation_data = SimulationData(simulation)
        session.add(simulation_data)
        session.commit()
        logger.info("Simulation data committed successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while committing to the database: {e}")
        raise

    finally:
        session.close()


def get_simulation(simulation_id: str):
    session = Session()
    try:
        simulation_data: SimulationData = session.query(SimulationData).filter(
            SimulationData.simulation_id == simulation_id).first()
        logger.info("Simulation data executed successfully")
        return simulation_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while executing to the database: {e}")
        raise

    finally:
        session.close()


def get_iteration_ids(simulation_ids: list[str]):
    session = Session()
    try:
        iteration_ids = []
        for simulation_id in simulation_ids:
            simulation_pattern = f"{simulation_id}/%"
            simulation_data = session.query(SimulationData).filter(
                SimulationData.simulation_id.like(simulation_pattern)).all()
            iteration_ids.extend(
                [iteration_data.simulation_id for iteration_data in simulation_data])

        logger.info("Iteration IDs executed successfully")
        return iteration_ids

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while executing to the database: {e}")
        raise

    finally:
        session.close()


def save_buses(simulation_id, buses: list["Bus"]):
    session = Session()
    try:
        buses_data: list[BusData] = []
        for bus in buses:
            bus_data = BusData(simulation_id, bus)
            buses_data.append(bus_data)

        session.add_all(buses_data)
        session.commit()
        logger.info("Buses data committed successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while committing to the database: {e}")
        raise

    finally:
        session.close()


def get_buses(simulation_id: str):
    session = Session()
    try:
        buses_data: list[BusData] = []
        buses_data = session.query(BusData)\
            .filter(BusData.simulation_id == simulation_id)\
            .all()

        logger.info("Buses data executed successfully")
        return buses_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while executing to the database: {e}")
        raise

    finally:
        session.close()


def save_passengers(simulation_id, passengers: list["Passenger"]):
    session = Session()
    try:
        passengers_data: list[PassengerData] = []
        for passenger in passengers:
            passengers_data.append(PassengerData(simulation_id, passenger))

        session.add_all(passengers_data)
        session.commit()
        logger.info("Passengers data committed successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while committing to the database: {e}")
        raise

    finally:
        session.close()


def get_passengers_by_simulation_id_and_assignment_reasons_to_exclude(simulation_id: str,
                                                                      assignment_reasons_to_exclude: list[int]):
    session = Session()
    try:
        passengers_data: list[PassengerData] = []
        passengers_data = session.query(PassengerData)\
            .filter(PassengerData.simulation_id == simulation_id)\
            .filter(PassengerData.arrival_time.is_not(None))\
            .filter(PassengerData.aboard_time.is_not(None))\
            .filter(PassengerData.assignment_reason.notin_(assignment_reasons_to_exclude))\
            .all()

        logger.info("Passengers data executed successfully")
        return passengers_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while executing to the database: {e}")
        raise

    finally:
        session.close()


def get_passengers_by_simulation_id_and_assignment_reasons(simulation_id: str,
                                                           assignment_reasons: list[int]):
    session = Session()
    try:
        passengers_data: list[PassengerData] = []
        passengers_data = session.query(PassengerData)\
            .filter(PassengerData.simulation_id == simulation_id)\
            .filter(PassengerData.arrival_time.is_not(None))\
            .filter(PassengerData.aboard_time.is_not(None))\
            .filter(PassengerData.assignment_reason.in_(assignment_reasons))\
            .all()

        logger.info("Passengers data executed successfully")
        return passengers_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while executing to the database: {e}")
        raise

    finally:
        session.close()


def save_analysis(analysis_data: "SimulationAnalysis"):
    session = Session()
    try:
        analysis = AnalysisData(analysis_data)
        session.add(analysis)
        session.commit()
        logger.info("Analysis data committed successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while committing to the database: {e}")
        raise

    finally:
        session.close()


def get_analysis(analysis_id: str):
    session = Session()
    try:
        analysis_data: AnalysisData = session.query(AnalysisData).filter(
            AnalysisData.analysis_id == analysis_id).first()
        logger.info("Analysis data executed successfully")
        return analysis_data

    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred while executing to the database: {e}")
        raise

    finally:
        session.close()


from FinalProjectSimulator.models.simulation import Simulation
from FinalProjectSimulator.simulation_runner.package_models.express_bus import ExpressBus, Bus
from FinalProjectSimulator.simulation_runner.package_models.passenger import Passenger
