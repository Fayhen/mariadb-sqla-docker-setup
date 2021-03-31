from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship


SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:dev@localhost:3306/dev_database?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, future=True)

# Declarative Base class instatiation
Base = declarative_base()

# Define tables through classes:
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  username = Column(String(30), nullable=False)

class Address(Base):
  __tablename__ = 'addresses'

  id = Column(Integer, primary_key=True)
  email = Column(String(30), nullable=False)
  address = Column(String(100), nullable=False)
  country = Column(String(2), nullable=False)

  user_id = relationship("User", back_populates="addresses")

# Emit DDL to the database
Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
