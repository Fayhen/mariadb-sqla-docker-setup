# SQAlchemy - MySql/MariaDB connection examples #

This directory contains a few simple examples of establishing a SQLAlchemy connection to a MySQL/MariaDB database running on a Docker container, as well as manipulating schemas and data on it.

These examples are all self-contained and can be run by executing their respective scripts. You'll need Python 3 and docker-compose on your machine.

---

To be able to execute these scripts at the current version:

1. Setup a local MariaDB container by running docker-compose on the root of this repository:

   ```
   docker-compose up -d
   ```

2. Create and activate a Python virtual environment to install the required packages:

   On Linux: 
   ```
   python -m venv venv
   source venv/bin/activate
   pip install requirements.txt
   ```

   On Windows:
   ```
   python -m venv venv
   .\venv\Scripts\activate.bat
   pip install requirements.txt
   ```

3. cd to the ./setup_examples on your terminal and run any of them through Python:

   ```
   python setup_example_name.py
   ```

SQLAlchemy will log progress info to the terminal as it runs through the code.

---
Each example is detailed bellow:

#### setup_with_sql ####

This example connects to the test database and creates a simple test table through SQL statements. This is done by means of SQLAlchemy's `text` construct, which represents a textual SQL expression.

#### setup_with_metadata ####

This example connects to the test database and uses SQLAlchemy's `MetaData` class to create two simple tables, one related to the other by a Foreign Key.

The MetaData class is detached from SQLAlchemy's ORM, being within SQLAlchemy's Core set of utilities. It provides the developer with the SQL Expression Language, an easy-to-use syntax for quick database manipulation, without additional mapping.

#### setup_with_orm_registry and setup_with_orm_declarative ####

These two create the same schema as the `setup_with_metadata` example above, but use SQLAlchemy's ORM in order to do so. The only difference between both is in the instantiation of the Base class.

The Base class is the foundation of SQLAlchemy's ORM. Python classes mapped to the database tables all inherit from the Base class.

The Base class can be instantiated thourgh the ORM's `registry` object. This is how the instanation is made in the `setup_with_orm_registry` example.

```
from sqlalchemy.orm import registry

mapper_registry = registry()
Base = mapper_registry.generate_base()
```

Alternatively, there is a shortcut to instantiate the Base class by using SQLAlchemy's `declarative_base` function, which is how it is done in the `setup_with_orm_declarative` example. This function setups the registry for you. More details are available in [SQLAlchemy's documentation](https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm).

```
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```
