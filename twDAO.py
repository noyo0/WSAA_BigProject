import mysql.connector
from config import config_mysql as cfg

class TruckwashDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
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

    def findByID(self, id):
        cursor = self.getcursor()
        sql="SELECT * FROM truckwash WHERE id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def create(self, truckwash):
        cursor = self.getcursor()
        sql="INSERT INTO truckwash (Date, FleetNumber, Reg, Type) VALUES (%s, %s, %s, %s)"
        values = (truckwash.get("Date"), truckwash.get("FleetNumber"), truckwash.get("Reg"), truckwash.get("Type"))
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        truckwash["id"] = newid
        self.closeAll()
        return truckwash

    def convertToDictionary(self, resultLine):
        attkeys=['id', 'Date', 'FleetNumber', 'Reg', 'Type']
        truckwash = {}
        for i, attrib in enumerate(resultLine):
            truckwash[attkeys[i]] = attrib
        return truckwash

truckwashDAO = TruckwashDAO()