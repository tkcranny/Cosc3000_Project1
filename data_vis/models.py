from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


def get_session():
    """
    Provide a new database session.
    """

    engine = create_engine('sqlite:///courses.db')
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    return session_maker()


faculty_program_table = Table('faculty_program_association', Base.metadata,
                              Column('fac_code', String, ForeignKey('faculty.id')),
                              Column('prog_code', Integer, ForeignKey('programs.id'))
                              )


class Faculty(Base):
    """"""

    __tablename__ = 'faculty'

    id = Column(String(8), primary_key=True)
    title = Column(String(255), unique=True)

    programs = relationship('Program',
                            secondary=faculty_program_table,
                            backref='faculties'
                            )

    def __repr__(self):
        return "{}(id='{}', title='{}')".format(self.__class__.__name__, self.id, self.title)



class Program(Base):
    """UQ offered program."""

    __tablename__ = 'programs'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)

    units = Column(Integer)
    op = Column(Integer)
    predicted_fee = Column(Integer)
    location = Column(String(128))

    def __repr__(self):
        return "{}(id='{}', title='{}')".format(self.__class__.__name__, self.id, self.title)



class Major(Base):
    """"""

    __tablename__ = 'major'

    plan_id = Column(String(10), primary_key=True)
    title = Column(String(10), unique=True)

    def __repr__(self):
        return "{}(plan_id='{}', title='{}')".format(self.__class__.__name__, self.plan_id, self.title)


class Course(Base):
    """Course Database model"""

    __tablename__ = 'courses'

    code = Column(String(8), primary_key=True)
    title = Column(String(255))

    def __repr__(self):
        """
        String representation of this class.
        :return: Human readable string.
        """
        return "{}(code='{}', title='{}')".format(self.__class__.__name__, self.code, self.title)
