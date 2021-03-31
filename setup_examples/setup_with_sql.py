from sqlalchemy import create_engine, text

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:dev@localhost:3306/dev_database?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, future=True)

# Open database connection
with engine.connect() as conn:
  # Create a table
  conn.execute(
    text(
      "CREATE TABLE test_table (id INT, test_name VARCHAR(10), comment VARCHAR (500))"
    )
  )

  # Insert data
  conn.execute(
    text(
      "INSERT INTO test_table (id, test_name, comment) VALUES (:id, :test_name, :comment)"
    ),
    [
      {"id": 1, "test_name": "Test 1", "comment": "Comment 1"},
      {"id": 2, "test_name": "Test 2", "comment": "Comment 2"},
      {"id": 3, "test_name": "Test 3", "comment": "Comment 3"},
      {"id": 4, "test_name": "Test 4", "comment": "Comment 4"},
      {"id": 5, "test_name": "Test 5", "comment": "Comment 5"}
    ]
  )

  # Commit changes
  conn.commit()

# Un-comment to DROP table, if desired
# with engine.connect() as conn:
#   conn.execute(text("DROP TABLE test_table"))
#   conn.commit()
