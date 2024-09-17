
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
    print("Generated SQL is:
",generated_sql)

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
