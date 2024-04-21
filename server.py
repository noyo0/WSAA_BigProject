# Web service for BigProject (Truckwash)
# Author: Norbert Antal

from flask import Flask
import time

def now():
        current_timestamp = time.time()
        current_timestamp += 3600
        current_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_timestamp))
        return(current_datetime)

app = Flask(__name__)

@app.route('/')
def index():
        return f"Hello world...     {now()}"

if __name__ == "__main__":
    app.run(debug = True)