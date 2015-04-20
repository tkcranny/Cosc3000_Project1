from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation


Base = declarative_base()


def get_session():
    """
    Provide a new database session.
    """

    engine = create_engine('sqlite:///courses.db')
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    return session_maker()


class Course(Base):
    """Course Database model"""

    __tablename__ = "courses"

    code = Column(String(8), primary_key=True)
    title = Column(String(100))

    def __repr__(self):
        """
        String representation of this class.
        :return: Human readable string.
        """
        return "{}(code='{}', title='{}')".format(self.__class__.__name__, self.code, self.title)