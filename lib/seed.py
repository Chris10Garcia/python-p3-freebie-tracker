#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie


if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind = engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()

    fake = Faker()

    