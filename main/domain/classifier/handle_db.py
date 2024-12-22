import psycopg2
import uuid

DB_HOST = "localhost"
DB_NAME = "model_state"
DB_USER = "postgres"
DB_PASSWORD = "Ren3265933VlVA"

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


    def retrieve_file(self, record_id):
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
                return result
            else:
                print("No file found for the given ID.")

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")

    def retrieve_price(self, products):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()

            query = "SELECT product_name, product_price FROM product_info WHERE product_name = ANY(%s)"
            cur.execute(query, (products,))
            prices = cur.fetchall()

            if prices and prices[0]:
                return prices
            else:
                print("No prices found for the given input.")

            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error: {e}")