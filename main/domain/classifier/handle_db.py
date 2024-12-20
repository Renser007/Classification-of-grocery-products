import psycopg2
import uuid

DB_HOST = "localhost"
DB_NAME = "model_state"
DB_USER = "postgres"
DB_PASSWORD = ""

class SaveDb:
    def insert_record(self, status, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()

            query = """
            INSERT INTO model_weights (id, status, file)
            VALUES (%s, %s, %s)
            """
            record_id = uuid.uuid4()
            record_id_str = str(record_id)
            cur.execute(query, (record_id_str, status, file_data))

            conn.commit()
            print(f"Record inserted with ID: {record_id_str}")

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")


    def retrieve_file(self, record_id, output_path):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()

            query = "SELECT file FROM model_weights WHERE id = %s"
            cur.execute(query, (record_id,))
            result = cur.fetchone()

            if result and result[0]:
                with open(output_path, 'wb') as file:
                    file.write(result[0])
                print(f"File saved to {output_path}")
            else:
                print("No file found for the given ID.")

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")