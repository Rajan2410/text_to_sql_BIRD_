In this text_to_sql I used premsql pre-traned model with BIRD test dataset
Validated the SQL query by using sqlglot
Runs both the expected sql query and generated sql query on the bird test database on sqlite3 to compare both the results
(however the generated sql query need to be passed with error into generator again to comeup with correct sql query matching the database)
(Because other than syntax, the column and table name should match with the database we are using)
