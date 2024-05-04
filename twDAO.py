import mysql.connector as connector
from config import TWlocal as cfg
import datetime

class TruckwashDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg['host']
        self.user=       cfg['user']
        self.password=   cfg['password']
        self.database=   cfg['database']
        
    def getcursor(self): 
        self.connection = connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()

    def getAlleq(self, offset, limit): #paginated fleetlist
        cursor = self.getcursor()
        #get the sql row max
        count_sql = "SELECT COUNT(*) FROM eq_table"
        cursor.execute(count_sql)
        total_count = cursor.fetchone()[0]
        # Adjust limit if it exceeds total count
        limit = min(limit, total_count)
        # fetch paginated results
        sql = "SELECT * FROM eq_table LIMIT %s, %s"
        cursor.execute(sql, (offset, limit))
        results = cursor.fetchall()

        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionaryEQ(result))

        self.closeAll()
        return returnArray
         
    def getAll(self):
        cursor = self.getcursor()
        sql="SELECT * FROM truckwash"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray
    
    def getAll_limit(self,lim=5):
        cursor = self.getcursor()
        sql="""SELECT * FROM (
                SELECT * FROM truckwash ORDER BY id DESC LIMIT %s
                ) AS bottom
                ORDER BY id ASC"""
        cursor.execute(sql,(lim,))
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def create(self, wash_data):
        cursor = self.getcursor()
        sql="INSERT INTO truckwash (Date, FleetNumber, Reg, Type) VALUES (%s, %s, %s, %s)"
        values = (wash_data['Date'], wash_data['FleetNumber'], wash_data['Reg'], wash_data['Type'])
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        return wash_data

    def deleteWash(self, wash_id):
        cursor = self.getcursor()
        sql = "DELETE FROM truckwash WHERE id = %s"
        cursor.execute(sql, (wash_id,))
        self.connection.commit()
        self.closeAll()
        return wash_id
    
    def changeWash(self, updatedData):
        # Convert date to MySQL-friendly format
        updatedData['Date'] = datetime.datetime.strptime(updatedData['Date'], '%d/%b/%Y').strftime('%Y-%m-%d')
        
        cursor = self.getcursor()
        sql = "UPDATE truckwash SET Date = %s, FleetNumber = %s, Reg = %s, Type = %s WHERE id = %s"
        values = (updatedData['Date'], updatedData['Fleet Number'], updatedData['Reg'], updatedData['Type'], updatedData['wash_id'])
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        return updatedData

    def convertToDictionary(self, resultLine):
        attkeys=['id', 'Date', 'FleetNumber', 'Reg', 'Type']
        truckwash = {}
        for i, attrib in enumerate(resultLine):
            truckwash[attkeys[i]] = attrib
        return truckwash
    
    def convertToDictionaryEQ(self, resultLine):
        attkeys=['id', 'FleetNumber', 'Reg', 'Type', 'Customer']
        truckwash = {}
        for i, attrib in enumerate(resultLine):
            truckwash[attkeys[i]] = attrib
        return truckwash

truckwashDAO = TruckwashDAO()