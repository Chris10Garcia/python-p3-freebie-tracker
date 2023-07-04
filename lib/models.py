from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)





# company_dev = Table(
#               'company_dev
# 
# 
# 
#               )

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # freebees (pural) = relationship(Freebee, backref=backref('comapny'), cascade= stuff)
    # devs = relationship('Dev', secondary=table_dev_company, back_populates='companys')

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'


# class Freebee(Base)
    # table name

    # id = Column Inte pk True
    # item_name = Column string
    # value = Column Inte



    # def repr (self):
        # return stuff

