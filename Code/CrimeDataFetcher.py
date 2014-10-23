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

    #ACCESSING DATA by Many Parameters
    def getCrimesForSearch(self, searchParams):
        '''
            Returns a table of crimes for a given, complex search
            The search is constructed from a python dictionary of search keys
            and search values (for example 'resolution':'None'). Because of the way
            parameters are passed in as a dictionary, that makes every search narrower
            optional.

            Search Keys & Expected Types:
                - 'search'        : String (will be bluntly searched against the table)
                - 'district'    : String
                - 'category'    : String
                - 'day'            : String
                - 'resolution'    : String
        '''
        connection = self._getConnection()
        if connection is not None:
            cursor = connection.cursor()

            #craft the perfect query
            query = 'SELECT * FROM crimes'
            queryHasWhere = False

            #for each possible parameter, check where it's present,
            #and if it is, append an extra condition to the query
            if searchParams['search'] is not None and searchParams['search'] != '':
                search = self.cleanInput(searchParams['search'])
                if queryHasWhere:
                    query += ' AND'
                else:
                    query += ' WHERE'
                    queryHasWhere = True
                #narrow with search
                longOr = " (district ILIKE '%[search]%' OR description ILIKE '%[search]%' OR category ILIKE '%[search]%' OR resolution ILIKE '%[search]%' OR dayofweek ILIKE '[search]%')"
                query += longOr.replace("[search]",search)

            if 'district' in searchParams and searchParams['district'] != '-':
                district = self.cleanInput(searchParams['district'])
                if queryHasWhere:
                    query += ' AND'
                else:
                    query += ' WHERE'
                    queryHasWhere = True
                toQ = " district ILIKE '%[s]%'"
                query += toQ.replace('[s]',district)

            if 'category' in searchParams and searchParams['category'] != '-':
                category = self.cleanInput(searchParams['category'])
                if queryHasWhere:
                    query += ' AND'
                else:
                    query += ' WHERE'
                    queryHasWhere = True
                toQ = " category ILIKE '%[s]%'"
                query += toQ.replace('[s]',category)

            if 'resolution' in searchParams and searchParams['resolution'] != '-':
                resolution = self.cleanInput(searchParams['resolution'])
                if queryHasWhere:
                    query += ' AND'
                else:
                    query += ' WHERE'
                    queryHasWhere = True
                if resolution == '*resolved*':
                    query += " (resolution NOT ILIKE 'none' AND resolution NOT ILIKE 'unfound')"
                else:
                    toQ = " resolution ILIKE '%[s]%'"
                    query += toQ.replace('[s]',resolution)
            if 'day' in searchParams and searchParams['day'] != '-':
                day = self.cleanInput(searchParams['day'])
                if queryHasWhere:
                    query += ' AND'
                else:
                    query += ' WHERE'
                    queryHasWhere = True
                toQ = " dayofweek ILIKE '%[s]%'"
                query += toQ.replace('[s]',day)

            query += ' ORDER BY crime_id DESC'

            if queryHasWhere:       #requires an actual search to return data
                cursor.execute(query)
                #print "query : %s" % query || was used for debugging
                table = self.createTableFromCursor(cursor)
                connection.close()
                return table
            else:
                return [[]]

        else:
            return [[]]


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

        else:
            return [[]]

    def getNumberOfCrimesInCategory(self, category):
        ''' Returns the quantity of crimes under a category'''
        connection = self._getConnection()
        if connection is not None:
            cursor = connection.cursor()

            query = 'SELECT * FROM crimes WHERE category=%s'
            cursor.execute(query, (category.upper(),))
            crimesInCategory = cursor.fetchall()
            connection.close()
            return len(crimesInCategory)
        else:
            return 0

    def getListOfCategories(self):
        '''Returns list of unique categories in the dataset'''
        connection = self._getConnection()
        categoryList = []
        if connection is not None:
            cursor = connection.cursor()

            query = 'SELECT DISTINCT category FROM crimes ORDER BY category;'
            cursor.execute(query)
            categories = cursor.fetchall()
            connection.close()

            for categoryRow in categories:
                categoryList.append(categoryRow[0])
                # (Cleaning up the list)

            return categoryList

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

        else:
            return [[]]

    def getRandomCrimeID(self):
        ''' Returns the ID of a random unsolved Crime'''
        connection = self._getConnection()
        if connection is not None:
            cursor = connection.cursor()

            #Execute the query in a safe manner, taking advantage of .execute()'s format
            #str compatibility & helpful injection attack detection.
            query = "SELECT * FROM crimes WHERE (resolution ILIKE 'none' OR resolution ILIKE 'unfound') ORDER BY random() limit 1"
            cursor.execute(query)

            #Construct a 2D array of all the information from the query
            table = self.createTableFromCursor(cursor)
            connection.close() #we're done with the connection
            #Extract the one number we need from the table
            return table[0][0]

        else:
            return [[]]
