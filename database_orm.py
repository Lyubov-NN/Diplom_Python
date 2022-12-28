import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()


def get_class(table_name):
    class GenericTable(Base):
        __tablename__ = table_name
        id = sq.Column(sq.Integer, primary_key=True)
        choice = sq.Column(sq.String(length=40), unique=True)
    return GenericTable


def insert_table(tablename, choice):
    tnew = tablename(choice=choice)
    session.add_all([tnew])
    session.commit()


# insert_table('6186222', 11111)


DSN = "postgresql://postgres:!2345Qwert@localhost:5432/bot_user"
engine = sq.create_engine(DSN)
Base.metadata.create_all(engine)

# get_class('user').__table__.create(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# insert_table(6186222, 11111)
t1 = user(choice='111')
session.add_all([t1])
session.commit()

session.close()
