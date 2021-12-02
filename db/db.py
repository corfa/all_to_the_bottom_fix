from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from db.exception import DBnotFindException, ConnectionException

"""the class DataBase is responsible for working with the database and providing a session"""


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        try:
            self.connection.execute(self._test_query).fetchone()
        except OperationalError:
            raise DBnotFindException
        except:
            raise ConnectionException

    def make_session(self) -> Session:
        try:
            return Session(bind=self.connection)
        except:
            raise ConnectionException
