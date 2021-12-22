#import mysql.connector
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_IP = str(os.environ['DATABASE_IP'])
DATABASE_IP = "172.17.0.2"

DATABASE_USER = "root"
DATABASE_PASS = "root"


DATABASE = "tarea2"
PORT=3306

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_IP}:{PORT}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
