from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

engine = create_engine("sqlite:///ua.db", echo=True)
db_session_maker = sessionmaker(engine)


def create_db():
    models.Base.metadata.create_all(engine)


def drop_db():
    models.Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # drop_db()
    create_db()
