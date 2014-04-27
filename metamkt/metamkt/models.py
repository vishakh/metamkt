from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class Action(Base):
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    description = Column(Text, unique=True)
    points = Column(Integer)
    timestamp = Column(TIMESTAMP)

class EntityType(Base):
    __tablename__ = 'entitytype'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    timestamp = Column(TIMESTAMP)

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    entityType_id = Column(Integer, ForeignKey('entitytype.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    parent_id = Column(Integer, ForeignKey('entity.id'))
    price = Column(Numeric)
    timestamp = Column(TIMESTAMP)

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('entity.id'))
    action_id = Column(Integer, ForeignKey('action.id'))
    quantity = Column(Integer)
    description = Column(Text)
    timestamp = Column(TIMESTAMP)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    timestamp = Column(TIMESTAMP)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('entity.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    quantity = Column(Integer)
    minPrice = Column(Numeric)
    maxPrice = Column(Numeric)
    buyOrSell = Column(Text, unique=True)
    active = Column(Integer)
    timestamp = Column(TIMESTAMP)

class Points(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    event_id = Column(Integer, ForeignKey('entity.id'))
    amount = Column(Integer)
    timestamp = Column(TIMESTAMP)

class PointsChange(Base):
    __tablename__ = 'pointschange'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    term = Column(Text)
    value = Column(Numeric)
    timestamp = Column(TIMESTAMP)

class PriceChange(Base):
    __tablename__ = 'pricechange'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('entity.id'))
    term = Column(Text)
    value = Column(Numeric)
    timestamp = Column(TIMESTAMP)

class Shares(Base):
    __tablename__ = 'shares'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    entity_id = Column(Integer, ForeignKey('entity.id'))
    quantity = Column(Integer)
    cost = Column(Numeric)
    active = Column(Integer)
    startTime = Column(TIMESTAMP)
    endTime = Column(TIMESTAMP)
    timestamp = Column(TIMESTAMP)

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey('entity.id'))
    from_user_id = Column(Integer, ForeignKey('user.id'))
    to_user_id = Column(Integer, ForeignKey('user.id'))
    quantity = Column(Integer)
    price = Column(Numeric)
    buy_order_id = Column(Integer, ForeignKey('orders.id'))
    sell_order_id = Column(Integer, ForeignKey('orders.id'))
    timestamp = Column(TIMESTAMP)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    email = Column(Text, unique=True)
    salt = Column(Text, unique=True)
    password = Column(Text, unique=True)
    cash = Column(Numeric)
    value = Column(Numeric)
    points = Column(Integer)
    timestamp = Column(TIMESTAMP)

class ValueChange(Base):
    __tablename__ = 'valuechange'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    term = Column(Text)
    value = Column(Numeric)
    timestamp = Column(TIMESTAMP)

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

from pyramid.security import Allow
from pyramid.security import Everyone

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'view'),
                (Allow, 'group:editors', 'edit') ]
    def __init__(self, request):
        pass