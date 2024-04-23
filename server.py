# Web service for BigProject (Truckwash)
# Author: Norbert Antal

from flask import Flask, send_from_directory
from flask import jsonify
import time
from twDAO import truckwashDAO as DAO

def now(): #get timestamp
        current_timestamp = time.time()
        #current_timestamp += 3600
        current_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_timestamp))
        return(current_datetime)

app = Flask(__name__)

@app.route('/') # this is the index page
def index():
        return send_from_directory("C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/","index.html")
        #return f"Hello world...     {now()}"

@app.route('/img/<filename>') #this is to display images from the img folder
def img(filename):
        img_dir ="C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/img"
        return send_from_directory(img_dir,filename)

@app.route('/getall', methods=['GET']) # this is getting mysql data for the washlikst at @/wash
def getall():
    data = DAO.getAll()
    # Format the date to (06/Jun/24)
    for entry in data:
        entry['Date'] = entry['Date'].strftime('%d/%b/%Y')  # Assuming 'Date' is a datetime object
    return jsonify(data)


@app.route('/wash', methods=['GET']) # this will list all the washes
def washlist():
        dir ="C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/"
        return send_from_directory(dir, 'washlist.html')
        
if __name__ == "__main__":
    app.run(debug = True)