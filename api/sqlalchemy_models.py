from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    # id, login, registration_date
    pass


class Credits(Base):
    # id, user_id, issuance_date, return_date, actual_return_date, body, percent
    pass


class Dictionary(Base):
    # id, name
    pass


class Plans(Base):
    # id, period, sum, category_id
    pass


class Payments(Base):
    # id, sum, payment_date, credit_id, type_id
    pass
