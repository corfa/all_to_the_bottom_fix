import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

from config.ConfigApp import ConfigApp
from db import models

"""this function, in cases where it is not possible to connect to the database, tries to create it"""


def create_new_data_base(config: ConfigApp):
    con = psycopg2.connect(dbname='postgres', port=config.port,

                           user=config.user, host=config.host,
                           password=config.password)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
    cur = con.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(config.db))
    )
    engine = create_engine(
        config.url,
    )
    models.Base.metadata.create_all(engine)
    print("a new database was created")
