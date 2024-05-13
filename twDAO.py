# WSAA 2024 - End of Semester Project (Truckwash) Author: Norbert Antal
# Truckwas DAO for accessing and manipulation SQL data

import mysql.connector as connector # mysql-connector-python python module to interact with SQL
import datetime

class TruckwashDAO: # create DAO class with external config details as cfg
    def __init__(self, cfg):
        self.cfg = cfg

    def connect(self):
        return connector.connect(**self.cfg) # connect to database with the stored config
# get data for equipment list
    def getAlleq(self, offset, limit): #offset and limit for pagination
        connection = self.connect()
        cursor = connection.cursor()
        try:
            count_sql = "SELECT COUNT(*) FROM eq_table" # count max row number for pagination (max limit)
            cursor.execute(count_sql)
            total_count = cursor.fetchone()[0]
            limit = min(limit, total_count) # calculate max limit for the SQL query
            sql = "SELECT * FROM eq_table LIMIT %s, %s" # get limited length equipment list
            cursor.execute(sql, (offset, limit))
            results = cursor.fetchall()
            returnArray = [self.convertToDictionaryEQ(result) for result in results] # call function to convert SQL output to dictionary
            return returnArray
        finally: # close everything
            cursor.close()
            connection.close()

    def getAll(self, offset, limit): # get paginated wash entries with rates for each wash
        connection = self.connect()
        cursor = connection.cursor()
        try:
            count_sql = "SELECT COUNT(*) FROM truckwash"
            cursor.execute(count_sql)
            total_count = cursor.fetchone()[0]
            limit = min(limit, total_count)
            # SQL query to get combnined data from truckwash table and rates table
            sql = """SELECT
                        truckwash.id, truckwash.Date, truckwash.FleetNumber, truckwash.Reg, truckwash.Type, rates.Rate
                    FROM 
                        truckwash
                    LEFT JOIN 
                        rates ON truckwash.Type = rates.Type
                        ORDER BY truckwash.date DESC       
                    LIMIT %s, %s"""
            cursor.execute(sql, (offset, limit))
            results = cursor.fetchall()
            returnArray = [self.convertToDictionaryHist(result) for result in results]
            return returnArray
        finally:
            cursor.close()
            connection.close()

    def getAll_limit(self, lim=5):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = """SELECT * FROM (
                    SELECT * FROM truckwash ORDER BY id DESC LIMIT %s
                    ) AS bottom
                    ORDER BY id ASC"""
            cursor.execute(sql, (lim,))
            results = cursor.fetchall()
            returnArray = [self.convertToDictionary(result) for result in results]
            return returnArray
        finally:
            cursor.close()
            connection.close()

    def create(self, wash_data):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO truckwash (Date, FleetNumber, Reg, Type) VALUES (%s, %s, %s, %s)"
            values = (wash_data['Date'], wash_data['FleetNumber'], wash_data['Reg'], wash_data['Type'])
            cursor.execute(sql, values)
            connection.commit()
            return wash_data
        finally:
            cursor.close()
            connection.close()

    def deleteWash(self, wash_id):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = "DELETE FROM truckwash WHERE id = %s"
            cursor.execute(sql, (wash_id,))
            connection.commit()
            return wash_id
        finally:
            cursor.close()
            connection.close()

    def changeWash(self, updatedData):
        # Convert date to MySQL-friendly format
        updatedData['Date'] = datetime.datetime.strptime(updatedData['Date'], '%d/%b/%Y').strftime('%Y-%m-%d')
        
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = "UPDATE truckwash SET Date = %s, FleetNumber = %s, Reg = %s, Type = %s WHERE id = %s"
            values = (updatedData['Date'], updatedData['Fleet Number'], updatedData['Reg'], updatedData['Type'], updatedData['wash_id'])
            cursor.execute(sql, values)
            connection.commit()
            return updatedData
        finally:
            cursor.close()
            connection.close()
# ----------------------------- wash summary ---------------------------------------
    def getWashSum(self): #per customer per type monthly
        connection = self.connect()
        cursor = connection.cursor()
        try:
            sql = """SELECT 
                    YEAR(truckwash.Date) AS Year,
                    MONTH(truckwash.Date) AS Month,
                    IFNULL(eq_table.CUSTOMER_CODE, 'Third Party') AS Customer,
                    truckwash.Type, 
                    SUM(rates.Rate) AS TotalRate,
                    SUM(SUM(rates.Rate)) OVER (PARTITION BY IFNULL(eq_table.CUSTOMER_CODE, 'Third Party'), YEAR(truckwash.Date), MONTH(truckwash.Date)) AS CustomerMonthly
                FROM 
                    truckwash
                LEFT JOIN 
                    eq_table ON truckwash.FleetNumber = eq_table.CODE
                LEFT JOIN 
                    rates ON truckwash.Type = rates.Type
                GROUP BY 
                    YEAR(truckwash.Date), 
                    MONTH(truckwash.Date),
                    Customer,
                    truckwash.Type
                ORDER BY 
                    Year DESC, 
                    Month DESC,
                    Customer"""
            cursor.execute(sql)
            results = cursor.fetchall()
            returnArray = [self.convertToDictionaryWash(result) for result in results]
            return returnArray
        finally:
            cursor.close()
            connection.close()

    def getWashSumMonth(self): #per customer per month
            connection = self.connect()
            cursor = connection.cursor()
            try:
                sql = """SELECT 
                        YEAR(truckwash.Date) AS Year,
                        MONTH(truckwash.Date) AS Month,
                        IFNULL(eq_table.CUSTOMER_CODE, 'Third Party') AS Customer,
                        SUM(rates.Rate) AS TotalRate,
                        SUM(SUM(rates.Rate)) OVER (PARTITION BY IFNULL(eq_table.CUSTOMER_CODE, 'Third Party'), YEAR(truckwash.Date), MONTH(truckwash.Date)) AS CustomerMonthly
                    FROM 
                        truckwash
                    LEFT JOIN 
                        eq_table ON truckwash.FleetNumber = eq_table.CODE
                    LEFT JOIN 
                        rates ON truckwash.Type = rates.Type
                    GROUP BY 
                        YEAR(truckwash.Date), 
                        MONTH(truckwash.Date),
                        Customer
                    ORDER BY 
                        Year DESC, 
                        Month DESC,
                        Customer"""
                cursor.execute(sql)
                results = cursor.fetchall()
                returnArray = [self.convertToDictionaryWashMonth(result) for result in results]
                return returnArray
            finally:
                cursor.close()
                connection.close()

# -------------- convert SQL output to dictionary ----------------------------------

    def convertToDictionary(self, resultLine): #getAllLim()
        attkeys = ['id', 'Date', 'FleetNumber', 'Reg', 'Type']
        return {key: value for key, value in zip(attkeys, resultLine)}
    
    def convertToDictionaryHist(self, resultLine): #getALL()
        attkeys = ['id', 'Date', 'FleetNumber', 'Reg', 'Type', 'Rate']
        return {key: value for key, value in zip(attkeys, resultLine)}

    def convertToDictionaryEQ(self, resultLine):#geAlleq()
        attkeys = ['id', 'FleetNumber', 'Reg', 'Type', 'Customer']
        return {key: value for key, value in zip(attkeys, resultLine)}
    
    def convertToDictionaryWash(self, resultLine): #getWashSum()
        attkeys = ['Year', 'Month', 'Customer', 'Type', 'TotalRate', 'CustomerMonthly']
        return {key: value for key, value in zip(attkeys, resultLine)}
    
    def convertToDictionaryWashMonth(self, resultLine): #getWashSumMonth()
        attkeys = ['Year', 'Month', 'Customer', 'TotalRate']
        return {key: value for key, value in zip(attkeys, resultLine)}
    

        # Import config file
#from config import TWlocal
from config import TWhosted

# Create TruckwashDAO instance with configuration from config.py
#truckwashDAO = TruckwashDAO(TWlocal)
truckwashDAO = TruckwashDAO(TWhosted)

# issue with "weakly-referenced object no longer exists" resolved by closing each cursor and connection and moving cnfig to the end (?)