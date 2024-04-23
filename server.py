# Web service for BigProject (Truckwash)
# Author: Norbert Antal

from flask import Flask, send_from_directory
from flask import jsonify
import time
from twDAO import truckwashDAO as DAO

def now():
        current_timestamp = time.time()
        #current_timestamp += 3600
        current_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_timestamp))
        return(current_datetime)

app = Flask(__name__)

@app.route('/')
def index():
        return send_from_directory("C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/","index.html")
        #return f"Hello world...     {now()}"

@app.route('/img/<filename>')
def img(filename):
        img_dir ="C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/img"
        return send_from_directory(img_dir,filename)

@app.route('/getall', methods=['GET'])
def getall():
    data = DAO.getAll()
    # Format the date strings to short date format (e.g., '20/04/24')
    for entry in data:
        entry['Date'] = entry['Date'].strftime('%d/%b/%Y')  # Assuming 'Date' is a datetime object
    return jsonify(data)


@app.route('/wash', methods=['GET'])
def washlist():
        dir ="C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/"
        return send_from_directory(dir, 'washlist.html')
        #img_dir ="C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/img"
        #return send_from_directory(img_dir,'wash_list.html', data=data)
        
if __name__ == "__main__":
    app.run(debug = True)