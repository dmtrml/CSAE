from sqlalchemy import create_engine, Column, Integer,Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///mybase.db')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    category = Column(String(100))
    comment = Column(String(200))
    outcome_account = Column(String(70))
    outcome = Column(Float)
    outcome_currency = Column(String(5))
    income_account = Column(String(70))
    income = Column(Float)
    income_currency = Column(String(5))

    def __init__(self, date=None, category=None, comment=None, outcome_account=None, outcome=None,
                 outcome_currency=None, income_account=None, income=None, income_currency=None):
        self.date = date
        self.category = category
        self.comment = comment
        self.outcome_account = outcome_account
        self.outcome = outcome
        self.outcome_currency = outcome_currency
        self.income_account = income_account
        self.income = income
        self.income_currency = income_currency

    def __repr__(self):
        return '<User {} {} {} {} {} {} {} {} {}>'.format(self.date, self.category, self.comment, self.outcome_account,
                                                          self.outcome, self.outcome_currency,
                                                          self.income_account, self.income,self.income_currency)


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    account = Column(String(70))

    def __init__(self,account=None):
        self.account = account

    def __repr__(self):
        return '<Account {}>'.format(self.account)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String(70))
    subcategories = relationship("Subcategory", backref='parent_category')

    def __init__(self,category=None):
        self.category = category

    def __repr__(self):
        return '<category {}>'.format(self.category)


class Subcategory(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True)
    subcategory = Column(String(70))
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self,subcategory=None, category_id=None):
        self.subcategory = subcategory
        self.category_id = category_id

    def __repr__(self):
        return '<subcategory {} {}>'.format(self.subcategory, self.category_id)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

