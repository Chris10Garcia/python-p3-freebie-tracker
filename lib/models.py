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

    # this is a sqlalchemy thing.
    # on load, this acts like __init__
    @reconstructor
    def init_on_load(self):
        self.add_to_all(self)

    @classmethod
    def add_to_all(cls, obj):
        cls.all.append(obj)
    
    @classmethod
    def oldest_company(cls):
        return min(cls.all, key=lambda x : x.founding_year)

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name = item_name, value = value)

        self.freebies.append(freebie)
        dev.freebies.append(freebie)
        dev.companies.append(self)

        return freebie

    def __repr__(self):
        return f'<Company {self.name}>'


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    #one to many
    freebies = relationship('Freebie', backref=backref('dev'))
    #many to many
    companies = relationship('Company', secondary=company_dev, back_populates = 'devs')

    def received_one(self, item):
        for freebie in self.freebies:
            if freebie.item_name == item:
                return True
        return False

    def give_away(self, dev, freebie):
        if self == freebie.dev:
            freebie.dev = dev
            return "Sucessful"
        else:
            return f"The {freebie} does not belong to {self}. This person can not give it away"

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



