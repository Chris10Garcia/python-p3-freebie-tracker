from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref, reconstructor
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


company_dev = Table(
    'company_devs',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)

class Company(Base):
    __tablename__ = 'companies'

    all = []

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    #many to many
    devs = relationship('Dev', secondary=company_dev, back_populates = 'companies')
    #one to many
    freebies = relationship('Freebie', backref=backref('company'))

    def __init__(self):
        self.add_to_all(self)

    @reconstructor
    def init_on_load(self):
        self.add_to_all(self)

    @classmethod
    def add_to_all(cls, obj):
        cls.all.append(obj)

    def __repr__(self):
        return f'<Company {self.name}>'
    

    @classmethod
    def oldest_company(cls):
        return min(cls.all, key=lambda x : x.founding_year)


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    #one to many
    freebies = relationship('Freebie', backref=backref('dev'))
    #many to many
    companies = relationship('Company', secondary=company_dev, back_populates = 'devs')

    def __repr__(self):
        return f'<Dev {self.name}>'
    



class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    def __repr__(self):
        return f"<Freebie {self.item_name}>"

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"



