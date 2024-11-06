# GiG

from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

# DO NOT REMOVE THIS LINE
# This will import all the db_schemas and "register" them
# so that we can call create_all if necessary
# Due to this, I am disabling the pylint and ruff checks
# pylint: disable=unused-import
from digio.models.config_models import DatabaseConfigs

engine = None


# By default, SQLite3 database does not check for foreign key violations
# See Sec2 of https://www.sqlite.org/foreignkeys.html
# this is especially the case for in-memory database that we use for testing
# so you can insert a child tuple even if the corresponding entry
# in parent does not exist.
# we prevent this using this hack
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def get_db_session():
    with Session(engine) as session:
        yield session


def initialize_dbs(db_configs: DatabaseConfigs):
    engine = create_db_engine(db_configs)
    assert engine is not None
    SQLModel.metadata.create_all(engine)
    return engine


def create_db_engine(db_configs: DatabaseConfigs):
    global engine
    connect_args = {"check_same_thread": False}
    engine = create_engine(
        db_configs.get_db_url(), echo=True, connect_args=connect_args
    )
    return engine
