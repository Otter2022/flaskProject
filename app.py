import os
from flask import Flask
import psycopg2
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    with dataBaseWriter() as db_writer:
        db_writer.execute(f"SELECT * FROM ride_wait_times")
        rows = db_writer.fetchall()
    return rows

class dataBaseWriter():
    def __init__(self):
        print(os.getenv('PASSWORD'))
        self.conn = psycopg2.connect(host="localhost", dbname="amusmentPark", user="postgres",
                                password="Wack3yW8v37??", port=5432)

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("Error occurred:", exc_type, exc_value)
            self.conn.rollback()  # Rollback changes in case of errors
        else:
            self.conn.commit()
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    app.run()
