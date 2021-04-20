# mariadb-sqla-docker-setup
A simple containerized MariaDB database setup using SQLAlchemy and Alembic

---

This repository is a study in setting up and modifying a MariaDB database within a Docker container, using [SQLAlchemy](https://www.sqlalchemy.org/) patterns and [Alembic](https://pypi.org/project/alembic/) migrations.

A `docker-composer` script initializer an empty database within a container, and a migration CLI command creates sample `login`, `account`, `gender` and `address` tables within it. Tables are related to each other by Foreign Keys and are ready to use, both through SQLAlchemy's ORM or thorough direct SQL statements within MariaDB's console within the container.

More details on how this is implemented are in the following section, and setup instructions are down below.

## Technical details

The database is initialized through a `docker-compose` command with a simple configuration. A connection is created through SQAlchemy's engine, which is then able to access and modify the database. An engine is an SQLAlchemy construct that consists of both Dialect Pool objects, that work together to connect to the database and interpret its behavior, as well as interpret DBAPI modules and functions on the Python side. An in-depth look into these is provided by the [documentation](https://docs.sqlalchemy.org/en/14/core/engines.html).

Engines are typically created using a database URL through SQLAlchmey's [create_engine method](https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine) using a [database URL](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls) with syntax: `dialect+driver://username:password@host:port/database`. The following URL (with additional charset parameter) can be used to create an engine with the containerized MariaDB database, assuming it was set up using the current configurations with the `docker-compose.yml` file:

```
mysql+pymysql://root:dev@localhost:3306/dev_database?charset=utf8mb4
```

An engine is also created by Alembic in order to connect to and manipulate the target database. As such, the URL must be included in the `sqlalchemy.url` variable within the `alembic.ini` file. 

SQLAlchemy provides different patterns to interact with the database, distributed within its [ORM](https://docs.sqlalchemy.org/en/14/orm/index.html) and [Core](https://docs.sqlalchemy.org/en/14/core/index.html) toolsets. In this project, Object Relational Mapping is used to declare models, namely, SQLAlchemy's [declarative mapping](https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#orm-declarative-mapping). These models are also integrated with Alembic's [migration environment](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment), allowing them to be used by migrations, as explained below.

SQLAlchemy's declarative mapping uses a `Base` class that handles several ORM aspects (see documentation [here](https://docs.sqlalchemy.org/en/14/orm/declarative_tables.html)). Models that inherit from the `Base` class are all mapped to the database. By integrating the `Base` class with Alembic's migration environment, it becomes possible to auto-generate migration scripts by modifying the model classes. Detailed about his information can be found [here](https://alembic.sqlalchemy.org/en/latest/autogenerate.html).

Table constraints throughout the database are automatically generated. This is possible by using the [naming conventions](https://docs.sqlalchemy.org/en/14/core/constraints.html#configuring-constraint-naming-conventions) feature from SQLAlchemy, which can be [integrated with Alembic through the Base class metadata](https://alembic.sqlalchemy.org/en/latest/naming.html). The provided links contain detailed information about this. In this project, the definition naming convention can be found in the `models.py` file.    

## Setup

To run this project locally, first clone this repository. Next, create a Python 3 virtual environment for the dependencies to be installed. For example, the following commands will create and activate and virtual environment named `env`:

```
python -m venv env
./env/bin/activate
```

Use `pip` to install the requirements:

```
pip install -r requirements.txt
```

To setup MariaDB in a Docker container, ensure you have [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed. Then, simply execute the following command in you command line:

```
docker-compose up -d
```

To check if the container is set up and running, use the `docker ps` command. Provided the `docker-compose.yml` remains unedited, the output should list a MariaDB container running on the `3306` port, named `test-mariadb`.

At this point you should have an empty MariaDB database named `dev_database` within your container, whose root user has `dev` as password (these too are configured in the `docker-composer.yml` file). You can connect to this database using the TCP protocol, and browse it through SQL statements. To do so, enter the following in your command line and type in `dev` when prompted for the password. You'll end up in MariaDB's console.

```
mysql -h localhost -P 3306 -u root -p dev_database --protocol=tcp
```

Finally, this repository has a starter migration to set up a few tables in this database through SQAlchemy and Alembic. The resulting tables will correspond to the ORM classes found within `models.py`. For more information on how they work, check the details section above.

To run the migration, execute the following line on your virtual environment:

```
alembic upgrade head
```

This command applies migrations in chronological order up to the most recent one (referred to as `head`). Migrations are stored in the `alembic/versions/` directory, where you can find our single migration file. This file was autogenerated by Alembic by reading the ORMs models. Details on this can be read in the details section above.

The migration results in tables corresponding to our models, including Foreign Keys and named constraints, that are ready to use. They can be queried for in MariaDB's console, as exemplified below: 

```
SHOW TABLES;
+------------------------+
| Tables_in_dev_database |
+------------------------+
| account                |
| address                |
| alembic_version        |
| gender                 |
| login                  |
+------------------------+

SHOW COLUMNS FROM account;
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| first_name | varchar(30)  | NO   |     | NULL    |                |
| last_name  | varchar(30)  | NO   |     | NULL    |                |
| nat        | varchar(2)   | NO   |     | NULL    |                |
| phone      | varchar(20)  | NO   |     | NULL    |                |
| picture    | varchar(250) | NO   |     | NULL    |                |
| gender_id  | int(11)      | YES  | MUL | NULL    |                |
| login_id   | int(11)      | YES  | MUL | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
```

You're all set at this point. The database may be manipulated directly through SQLAlchemy's ORM, by use of [engines](https://docs.sqlalchemy.org/en/14/tutorial/engine.html#tutorial-engine), [sessions and our model classes](https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html#tutorial-orm-data-manipulation).

New migrations can be quickly written through [Alembic's operations](https://alembic.sqlalchemy.org/en/latest/ops.html) and through modifications to the model classes and [Alembic's auto-generation](https://alembic.sqlalchemy.org/en/latest/autogenerate.html). Do note that autogenerated migration must always be reviewed to ensure precision and for alteration cases that are unable to be detected by Alembic ([see this in-depth here](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)).

Finally, if you are done and have no need for the database, not that container data is persisted by Docker within its [volumes](https://docs.docker.com/storage/volumes/). Stop the running MariaDB container and remove its volume with the following commands:

```
docker-compose down
docker volume rm VOLUME_NAME
```

Use `docker volume ls` to list the containers stored on your machine. If you have several volumes and/or are unsure of which one corresponds to the one used by the MariaDB container, run the container again with `docker-compose up -d`  and use `docker ps` to list it. Get its `CONTAINER ID` attribute from the output and run the following line:

```
docker inspect -f '{{ .Mounts }}' CONTAINER_ID
```

This outputs information about the container which includes its volume name. Simply run `docker volume rm VOLUME_NAME` afterwards.


### Other setup examples

While the declarative base is used in the main, there are a few other SQLAlchemy pattern examples provided within the `setup_examples/` directory. These are standalone scripts that connect to the database and add tables through different SQLAlchemy patterns. More details can be read on a dedicated README within that folder.

Do note, however, that these scripts are standalone and meant to be used individually. Being standalone means they are *not* integrated with Alembic and are *not* isolated from the main database. Instead, they connect and modify the same database straight through SQAlchemy in a single run. This means they interfere with the main database setup and with each other. Therefore, the database should be dropped between runs, and its better not to run the if you already ran the main setup.

Each example has a commented-out `drop_all()` or `DROP TABLE` line that will drop all tables from the database. These can be un-commented, and the script rerun. This allows to run each example without need to remove and recreate the docker container.

Should you wish to drop the container in any case, stop its running and delete its volume, as detailed at the end of the main setup section.
