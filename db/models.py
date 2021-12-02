from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userName = Column(String(10), nullable=False)
    lastIp = Column(String(50), nullable=False)
    web_id = Column(String(20), nullable=True)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    time_visit = Column(String(50), nullable=False)
    date_visit = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id']),
        ForeignKeyConstraint(['category_id'], ['categories.id']),
    )


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    web_id = Column(String(20), nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class ContentCarts(Base):
    __tablename__ = "contentCarts"
    id = Column(Integer, primary_key=True)

    cart_id = Column(Integer, nullable=False)
    goods_id = Column(Integer, nullable=False)
    amount = Column(String(20), nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        ForeignKeyConstraint(['goods_id'], ['goods.id']),
        ForeignKeyConstraint(['cart_id'], ['carts.id']),
    )


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    cart_id = Column(Integer, nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id']),
        ForeignKeyConstraint(['cart_id'], ['carts.id']),
    )


class Goods(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True)
    web_id = Column(String(20), nullable=False)
    name = Column(String(50), nullable=False)
    category_id = Column(Integer, nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id']),
    )