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

    
    companies = [Company(name=fake.company(), founding_year=random.randint(1980,2022)) for i in range(25)]

    devs = [Dev(name = fake.name()) for i in range(50)]

    freebies = [Freebie(item_name = fake.job(), value = random.randint(1,25)) for i in range(100)]

    session.add_all(companies + devs + freebies)
    session.commit()

    for dev in devs:
        for i in range(random.randint(1,8)):
            company = random.choice(companies)
            if dev not in company.devs:
                company.devs.append(dev)
                session.add(company)
                session.commit()
            
    for freebie in freebies:
        freebie.company = random.choice(companies)
        freebie.dev = random.choice(devs)

    session.add_all(freebies)
    session.commit()