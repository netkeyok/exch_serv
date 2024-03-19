from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys


sys.path.append(os.path.join(sys.path[0], 'db_connections'))

load_dotenv()

ORACLE_PORT = os.environ.get("ORACLE_PORT")
ORACLE_USER = os.environ.get("ORACLE_USER")
ORACLE_PASS = os.environ.get("ORACLE_PASS")
ORACLE_HOST = os.environ.get("ORACLE_HOST")
ORACLE_BASE = os.environ.get("ORACLE_BASE")
# ORACLE_CONN = f'{ORACLE_HOST}/{ORACLE_BASE}'

url = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASS}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_BASE}"
engine = create_engine(url=url, thick_mode=True)
Session = sessionmaker(bind=engine)
session = Session()
