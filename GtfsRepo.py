import sqlalchemy as db


username = "admin"
password = "Hod#Hanit"
host = "drtservice-simulation.ch26o0a2okon.il-central-1.rds.amazonaws.com"
port = 3306
engine = db.create_engine(f"mysql://{username}:{password}@{host}")
connection = engine.connect()
