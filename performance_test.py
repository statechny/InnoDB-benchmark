import mysql.connector
import time
import csv

# Database connection setup
db_config = {
    'user': 'root',
    'host': '127.0.0.1',
    'database': 'test_db',
}

def run_query(cursor, query):
    start_time = time.time()
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()
    return end_time - start_time, len(result)

def run_benchmark():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    results = []

    # 1. Add dob_hash column if not exists
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN dob_hash CHAR(32);")
        connection.commit()
        print("Added dob_hash column")
    except mysql.connector.Error as err:
        print(f"Error adding dob_hash column (maybe it exists already): {err}")

    # 2. Populate dob_hash column with MD5 of date_of_birth
    try:
        cursor.execute("UPDATE users SET dob_hash = MD5(date_of_birth);")
        connection.commit()
        print("Populated dob_hash column with MD5 hashes")
    except mysql.connector.Error as err:
        print(f"Error populating dob_hash column: {err}")

    # 3. Drop BTREE index if exists
    try:
        cursor.execute("DROP INDEX idx_dob_btree ON users;")
        connection.commit()
        print("Dropped index idx_dob_btree")
    except mysql.connector.Error as err:
        print(f"Error dropping index: {err}")

    # 4. Run query without index
    exec_time, row_count = run_query(cursor, "SELECT * FROM users WHERE date_of_birth = '1990-01-01';")
    results.append(["no_index", exec_time, row_count])

    # 5. Create BTREE index and test with it
    cursor.execute("CREATE INDEX idx_dob_btree ON users(date_of_birth);")
    connection.commit()
    exec_time, row_count = run_query(cursor, "SELECT * FROM users WHERE date_of_birth = '1990-01-01';")
    results.append(["btree_index", exec_time, row_count])

    # 6. Run query on hashed date of birth (simulating a HASH index)
    exec_time, row_count = run_query(cursor, "SELECT * FROM users WHERE dob_hash = MD5('1990-01-01');")
    results.append(["hash_index", exec_time, row_count])

    connection.close()

    # Save results to CSV
    with open('select_benchmark.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Test", "Execution Time", "Rows Returned"])
        writer.writerows(results)

if __name__ == "__main__":
    run_benchmark()
