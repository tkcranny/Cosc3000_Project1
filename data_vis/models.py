from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()
engine = create_engine('sqlite:///courses.db')
get_session = sessionmaker(bind=engine)


faculty_program_table = Table('faculty_program_association', Base.metadata,
                              Column('fac_code', String, ForeignKey('faculty.id')),
                              Column('prog_code', Integer, ForeignKey('programs.id'))
                              )

# program_major_table = Table('program_major_association', Base.metadata,
#                             Column('prog_code', String, ForeignKey('programs.id')),
#                             Column('major_code', String, ForeignKey('majors.id'))
#                             )


class Faculty(Base):
    """"""

    __tablename__ = 'faculty'

    id = Column(String(8), primary_key=True)
    title = Column(String(255), unique=True)
    html_reference = Column(String(128), unique=True)


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
    title = Column(String(255))
    abbr = Column(String(128))

    units = Column(Integer)
    op = Column(Integer)
    annual_fee = Column(Integer)
    location = Column(String(128))
    semesters = Column(Integer)

    @property
    def cost(self):
        """Return the cost of the entire degree."""
        return int(self.semesters * (self.annual_fee / 2))

    majors = relationship('Major', backref='program')


    def __repr__(self):
        return "{}(id='{}', title='{}')".format(self.__class__.__name__, self.id, self.title)


class Major(Base):
    """"""

    __tablename__ = 'majors'

    id = Column(String(10), primary_key=True)
    title = Column(String(10), unique=True)
    program_id = Column(Integer, ForeignKey('programs.id'))

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
