from sqlalchemy import (
  create_engine, MetaData, Table,
  Column, Integer, String, ForeignKey
)

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:dev@localhost:3306/dev_database?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, future=True)

# Instantiate MetaData class
metadata = MetaData()

# Define tables through MetaData
user_table = Table(
  "users",
  metadata,
  Column('id', Integer, primary_key=True),
  Column('username', String(30), nullable=False),
)

address_table = Table(
  "addresses",
  metadata,
  Column('id', Integer, primary_key=True),
  Column('user_id', ForeignKey('users.id'), nullable=False),
  Column('email', String(30), nullable=False),
  Column('address', String(100), nullable=False),
  Column('country', String(2), nullable=False)
)

# Emit DDL to the database
metadata.create_all(engine)
# metadata.drop_all(engine)
