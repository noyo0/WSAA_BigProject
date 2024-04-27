# Web service for BigProject (Truckwash)
# Author: Norbert Antal

from flask import Flask, send_from_directory
from flask import Flask, render_template
from flask import jsonify
from flask import request
import time
from twDAO import truckwashDAO as DAO

def now(): #get timestamp
        current_timestamp = time.time()
        #current_timestamp += 3600
        current_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_timestamp))
        return(current_datetime)

app = Flask(__name__)

# HTML ROUTING ------------------------------------------------------------------------
@app.route('/') # this is the index page
def index():
        return render_template('index.html')
        #return send_from_directory("C:/Users/norbe/OneDrive/ATU_Galway/WSAA_BigProject/WSAA_BigProject/","index.html")

@app.route('/img/<filename>') #this is to display images from the img folder
def img(filename):
        return send_from_directory('img', filename)

@app.route('/washlist') # this is the wash list page
def washlist():
        return render_template('wash_list.html', title='Wash list')

@app.route('/addwash') # this is the wash list page
def addwash():
        return render_template('addwash.html', title='Add Wash')


# DATA ACCESS -----------------------------------------------------------------------------------------------------------------------
        # Read all ------------------
@app.route('/getallSQL', methods=['GET']) # this is getting mysql data for the washlikst at @/wash
def getallSQL():
    data = DAO.getAll()
    # Format the date to (06/Jun/24)
    for entry in data:
        entry['Date'] = entry['Date'].strftime('%d/%b/%Y')  # Assuming 'Date' is a datetime object
    return jsonify(data)
        
                # Read all with limit (default 5)------------------
@app.route('/getallLimSQL', methods=['GET']) # this is getting mysql data for the washlikst at @/wash
def getallLimSQL():
    data = DAO.getAll_limit(5)
    # Format the date to (06/Jun/24)
    for entry in data:
        entry['Date'] = entry['Date'].strftime('%d/%b/%Y')  # Assuming 'Date' is a datetime object
    return jsonify(data)

        # Add data -------------------
@app.route('/addwashSQL', methods=['POST'])  # This route handles form submissions
def addwashSQL():
    if request.method == 'POST':
        # Capture form data
        data = request.get_json()
        # Create a dictionary to store data entry to pass to DAO
        wash_data = {
            'Date': data['date'],
            'FleetNumber': data['fleetNumber'],
            'Reg': data['reg'],
            'Type': data['type']
        }
        # pass data to DAO.create function
        DAO.create(wash_data)
        return jsonify(wash_data)

        # DELETE ---------------
@app.route('/deleteWash', methods=['POST'])
def deleteWash():
    try:
        wash_id = request.json['wash_id']  # Assuming the ID is sent in the JSON request body
        DAO.deleteWash(wash_id)
        return jsonify({"message": "Wash deleted successfully"})
    except Exception as e:
        print("Error deleting wash:", e)  # Log the error to the console
        return jsonify({"error": "An internal server error occurred"}), 500
        
if __name__ == "__main__":
    app.run(debug = True)