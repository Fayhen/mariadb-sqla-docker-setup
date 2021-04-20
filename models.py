from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Apply a naming convention to database constraints through the MetaData
metadata = MetaData(
    naming_convention={
      "ix": "ix_%(column_0_label)s",
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s"
    }
)

# Instantiate the Base class
Base = declarative_base(metadata=metadata)


# Define ORM models
class Gender(Base):
    __tablename__ = 'gender'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)

    accounts = relationship("Account")


class Login(Base):
    __tablename__ = 'login'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    email = Column(String(20), nullable=False, unique=True)

    account = relationship("Account", uselist=False, back_populates="login")


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    nat = Column(String(2), nullable=False)
    phone = Column(String(20), nullable=False)
    picture = Column(String(250), nullable=False)

    addresses = relationship("Address")

    gender_id = Column(Integer, ForeignKey('gender.id'))
    login_id = Column(Integer, ForeignKey('login.id'))
    login = relationship("Login", back_populates="account")


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    street = Column(String(30), nullable=False)
    postal = Column(String(10), nullable=False)
    number = Column(String(7), nullable=False)
    city = Column(String(30), nullable=False)
    state = Column(String(30), nullable=False)
    country = Column(String(30), nullable=False)

    account_id = Column(Integer, ForeignKey('account.id'))

