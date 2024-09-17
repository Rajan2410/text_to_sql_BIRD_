def generate_sql_from_text(nl_prompt):
    prompt = nl_prompt
    generated = generator(prompt)[0]['generated_text']

    sql_start = generated.find('SELECT')
    sql_query = generated[sql_start:].strip()

    if ";" in sql_query:
        sql_query = sql_query.split(";")[0].strip()+';'

    if "\n\n\n" in sql_query:
        sql_query = sql_query.split("\n\n\n")[-1].strip()

    if '$$ LANGUAGE plpgsql;' in sql_query:
        parts = sql_query.split('$$ LANGUAGE plpgsql;')
        for part in parts:
          part=part.strip()
          if part.startswith('SELECT'):
            print('part-1')
            sql_query = part
            break

    #print('Generated SQL is:\n',sql_query)
    return sql_query

def validate_sql(query):
    try:
        sqlglot.parse_one(query)
        return True, "Valid SQL"
    except Exception as e:
        return False, str(e)

def execute_query(db_id,sql_query):
  print(f'Executing query in {db_id}')
  executor = SQLiteExecutor()
  db_path = (
    f"/root/anindya/text2sql/data/bird/validation/dev_databases/{db_id}/{db_id}.sqlite"
  )
  sql = sql_query

  result = executor.execute_sql(
    sql=sql,
    dsn_or_db_path=db_path
  )

  return result


import random

def evaluate_bird_benchmark():
    # Picking a random example from the dataset
    random_example = random.choice(bird_test_dataset)

    # Extracting nl nd sql
    nl_query = random_example['question']
    nl_prompt= random_example['prompt']
    evidence = random_example['evidence']
    db_id = random_example['db_id']
    expected_sql = random_example['SQL']

    print(f"Evaluating Sample:")
    print('db_id: ',db_id)
    print(f"Question: {nl_query}")
    print(f"Expected SQL: {expected_sql}")

    generated_sql = generate_sql_from_text(nl_prompt)
    print("Generated SQL is:",generated_sql)

    is_valid, validation_msg = validate_sql(generated_sql)
    print(f"SQL Validation: {validation_msg}")
    if not is_valid:
        return

    print("Running expected SQL...")
    print("Expected SQL: ",expected_sql)
    expected_result = execute_query(db_id,expected_sql)
    print(f"Expected Result: {expected_result}")

    print("Running generated SQL...")
    print("Generated SQL: ",generated_sql)
    generated_result = execute_query(db_id,generated_sql)
    print(f"Generated Result: {generated_result}")

    if generated_result == expected_result:
        print("Success: Generated SQL matches expected output!")
    else:
        print("Failure: Mismatch in results.")

evaluate_bird_benchmark()
