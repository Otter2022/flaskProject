import os
from flask import Flask, render_template, url_for, redirect, jsonify, request
import psycopg2
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    rows = getAverageWaitTime()
    data = [{"column1": f" {i[0]}", "column2": i[1], "column3": i[2]} for i in rows]
    return render_template('index.html', rows=len(rows), data=data)

@app.route('/refresh_data')
def refresh_data():
    rows = getAverageWaitTime()
    data = [{"column1": f" {i[0]}", "column2": i[1], "column3": i[2]} for i in rows]
    return jsonify(data)

class dataBaseWriter():
    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", dbname="amusmentPark", user="postgres",
                                password="???", port=5432)

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

def getAverageWaitTime():
    with dataBaseWriter() as db_writer:
        db_writer.execute(f"SELECT ride_name, average_wait_time, current_wait_time FROM ride_wait_times")
        rows = db_writer.fetchall()
    return rows

if __name__ == '__main__':
    app.run()
