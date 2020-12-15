from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql://root:CHRG!@#!@127.0.0.1/recipe',
                       pool_recycle=3600,
                       pool_size=5,
                       pool_pre_ping=True,
                       max_overflow=20,
                       convert_unicode=True)


def get_session():
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=True,
                                       bind=engine))


db_session = get_session()
Base = declarative_base()
Base.query = db_session.query_property()
