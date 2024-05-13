# Web service for BigProject (Truckwash)
# Author: Norbert Antal
# Backend, handling routing for HTML pages and providing API endpoints to interact with the database.

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

@app.route('/img/<filename>') #allow displaying images from the img folder
def img(filename):
        return send_from_directory('img', filename)

@app.route('/test') 
def test():
        return render_template('test.html', title='test')

@app.route('/washlist')
def washlist():
        return render_template('wash_list.html', title='Wash history')

@app.route('/fleetlist')
def fleetlist():
        return render_template('fleet_list.html', title='Fleet list')

@app.route('/addwash')
def addwash():
        return render_template('addwash.html', title='Add Wash')

# DATA ACCESS -----------------------------------------------------------------------------------------------------------------------
        # Read all fleet, a paginated fleet list------------------
@app.route('/getall_eqSQL', methods=['GET']) 
def getall_eqSQL():
    offset = request.args.get('offset', default=0, type=int) #where to start paginated list
    limit = request.args.get('limit', default=20, type=int) #number of rows in the list
    data = DAO.getAlleq(offset, limit)
    return jsonify(data)

        # Read all wash paginated------------------
@app.route('/getallSQL', methods=['GET']) # get mysql data for wash history
def getallSQL():
    offset = request.args.get('offset', default=0, type=int) #where to start
    limit = request.args.get('limit', default=20, type=int) #number of rows
    data = DAO.getAll(offset, limit)
    # Format the date to (06/Jun/24)
    for entry in data:
        entry['Date'] = entry['Date'].strftime('%d/%b/%Y')
    return jsonify(data)
        
        # Read all with limit (default 5) for recent washes------------------
@app.route('/getallLimSQL', methods=['GET'])
def getallLimSQL():
    data = DAO.getAll_limit(5)
    # Format the date to (06/Jun/24)
    for entry in data:
        entry['Date'] = entry['Date'].strftime('%d/%b/%Y')
    return jsonify(data)

        # CREATE -------------------
@app.route('/addwashSQL', methods=['POST'])  # Add wash to truckwash data table
def addwashSQL():
    if request.method == 'POST':
        data = request.get_json() # Captured form data from AJAX
        # Create a dictionary to store data entry from form to pass to DAO
        wash_data = {
            'Date': data['date'],
            'FleetNumber': data['fleetNumber'],
            'Reg': data['reg'],
            'Type': data['type']
        }
        # pass data to DAO.create function
        DAO.create(wash_data) # call python DAO function to write into the SQL table 
        return jsonify(wash_data)
    
    # UPDATE --------------------------------------------
@app.route('/updateWash', methods=['POST'])
def update_wash():
    if request.method == 'POST':
        data = request.get_json() # Captured form data from AJAX
        # pass data to DAO.changeWash function
        updated_data = DAO.changeWash(data)
        return jsonify(updated_data)

        # DELETE wash entry---------------
@app.route('/deleteWash', methods=['POST'])
def deleteWash():
    try:
        wash_id = request.json['wash_id']  # wash_id extracted from form data by AJAX
        DAO.deleteWash(wash_id)
        return jsonify({"message": "Wash deleted successfully"}) # check if it's working
    except Exception as e:
        print("Error deleting wash:", e)  # Log the error to the console
        return jsonify({"error": "An internal server error occurred"}), 500
    
    # Wash summary for Plotly chart  & details matrix (per month per Eq type per customer) ---------------------------------------------------------
@app.route('/getWashSumJSON', methods=['GET'])
def getWashSumJSON():
    data = DAO.getWashSum()
    for entry in data:
        month = entry['Month'] # select Month from SQL output
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] # set month names
        entry['Month'] = month_names[month - 1] # rename months as above for for X axis/ matrix table
    return jsonify(data)

    # Wash summary for Plotly chart + sum matrix(per month per customer)---------------------------------------------------------
@app.route('/getWashSumMonth', methods=['GET'])
def getWashSumMonth():
    data = DAO.getWashSumMonth()
    for entry in data:
        month = entry['Month']
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        entry['Month'] = month_names[month - 1]
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug = True)