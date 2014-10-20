#!/usr/bin/python
import psycopg2
import cgitb
cgitb.enable()
'''
    CRIMR
    
    CrimeDataFetcher.py (phase_3)
    
    Charlie Imhoff,
    Graham Earley,
    Eric Walker
'''

class CrimeDataFetcher:
    '''
    Our DataSource.py equivalent. CrimeDataFetcher is a great little interface for
    automatically setting up an psql connection, grabbing a cursor, and filling a table
    with results from said cursor.
    '''

    #UTILITY METHODS
    def __init__(self):
        pass
    
    def _getConnection(self):
        return psycopg2.connect(database='earleyg', user='earleyg', password='field799java')

    #Deprecated. Execute cursor queries using cursor.execute(query, (formatStrParam, ))
    def cleanInput(self, str):
        ''' Removes any control characters that out HTML might be screwed up by
        '''
        charsToRemove = ';,\\/:\'"<>@'
        for ch in charsToRemove:
            str = str.replace(ch, '')
        return str
        
    def createTableFromCursor(self, cursor):
        table = []
        for row in cursor:
            rowData = []
            for cell in row:
                rowData.append(cell)
            table.append(rowData)
        return table

    #ACCESSING DATA
    def getAllCrimesFromDistrict(self, districtString):
        ''' Returns a table of the crimes of all the crimes in the district'''
        connection = self._getConnection()
        if connection is not None:
            cursor = connection.cursor()
        
            #Execute the query in a safe manner, taking advantage of .execute()'s format
            #str compatibility & helpful injection attack detection. 
            query = 'SELECT * FROM crimes WHERE district=%s ORDER BY crime_id DESC'
            cursor.execute(query, (districtString.upper(),))
            
            #Construct a 2D array of all the information from the query
            table = self.createTableFromCursor(cursor)
            connection.close() #we're done with the connection
            return table
            
        #else
        return [[]]

    def getCrimeFromID(self, idNum):
        ''' Returns a table containing the data from one crime, identified by the
            ID number. '''
        connection = self._getConnection()
        if connection is not None:
            cursor = connection.cursor()
        
            #Execute the query in a safe manner, taking advantage of .execute()'s format
            #str compatibility & helpful injection attack detection. 
            query = 'SELECT * FROM crimes WHERE crime_id=%s'
            cursor.execute(query, (idNum,))
            
            #Construct a 2D array of all the information from the query
            table = self.createTableFromCursor(cursor)
            connection.close() #we're done with the connection
            return table
            
        #else
        return [[]]

    def getRandomCrimeID(self):
        ''' Returns the ID of a random Crime'''
        connection = self._getConnection()
        if connection is not None:
            cursor = connection.cursor()
        
            #Execute the query in a safe manner, taking advantage of .execute()'s format
            #str compatibility & helpful injection attack detection. 
            query = 'SELECT * FROM crimes ORDER BY random() limit 1'
            cursor.execute(query)
            
            #Construct a 2D array of all the information from the query
            table = self.createTableFromCursor(cursor)
            connection.close() #we're done with the connection
            #Extract the one number we need from the table
            return table[0][0]
            
        #else
        return 0

    def getAllCrimesByCategory(self, catString):
        ''' Returns a table of the crimes of all the crimes in a category'''
        #Implement later
        return []
        
    def getAllCrimesByDate(self, date):
        ''' Returns a table of the crimes of all the crimes on a date'''
        #Implement later
        return []
        
    def getCrimesContainingDescriptionText(self, desc):
        ''' Returns a table of the crimes related to the inputed description'''
        #Implement later
        return []
        
    def getAllCrimesByDayOfWeek(self, day):
        ''' Returns a table of the crimes which occurred on the specified day of the week'''
        #Implement later
        return []
        
    def getRandomUnresolvedCrime(self):
        '''Returns a table row of a random crime where resolution="None" '''
        #Implement later
        return []
