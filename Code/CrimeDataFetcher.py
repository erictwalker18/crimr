import psycopg2

'''
    CRIMR
    
    webapp.py (phase_2)
    
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
    			- 'search'		: String (will be bluntly searched against the table)
    			- 'district'	: String
    			- 'crime_id'	: String
    			- 'category'	: String
    			- 'day'			: String
    			- 'resolution'	: String 
    	'''
        connection = self._getConnection()
        if connection is not None:
        	cursor = connection.cursor()
        	
        	#craft the perfect query
        	query = 'SELECT * FROM crimes'
        	queryHasWhere = False
        	
        	#for each possible parameter, check where it's present, 
        	#and if it is, append an extra condition to the query 
        	if searchParams['search'] is not None:
        		search = self.cleanInput(searchParams['search'])
        		if queryHasWhere:
        			query += ' AND'
        		else:
        			query += ' WHERE'
        			queryHasWhere = True
        		#narrow with search
        		longOr = ' (district LIKE [search] OR description LIKE [search] OR category LIKE [search] OR resolution LIKE [search])'
        		query += longOr.replace('[search]',search)
        		
        	if searchParams['district'] is not None:
        		district = self.cleanInput(searchParams['district'])
        		if queryHasWhere:
        			query += ' AND'
        		else:
        			query += ' WHERE'
        			queryHasWhere = True
        		query += ' district LIKE %s' % district
        		
        	if searchParams['crime_id'] is not None:
        		crime_id = self.cleanInput(searchParams['crime_id'])
        		if queryHasWhere:
        			query += ' AND'
        		else:
        			query += ' WHERE'
        			queryHasWhere = True
        		query += ' crime_id=%s' % crime_id
        	
        	if searchParams['category'] is not None:
        		category = self.cleanInput(searchParams['category'])
        		if queryHasWhere:
        			query += ' AND'
        		else:
        			query += ' WHERE'
        			queryHasWhere = True
        		query += ' category LIKE %s' % category
        		
        	if searchParams['resolution'] is not None:
        		resolution = self.cleanInput(searchParams['resolution'])
        		if queryHasWhere:
        			query += ' AND'
        		else:
        			query += ' WHERE'
        			queryHasWhere = True
        		query += ' resolution LIKE %s' % resolution
        		
        	if searchParams['day'] is not None:
        		day = self.cleanInput(searchParams['day'])
        		if queryHasWhere:
        			query += ' AND'
        		else:
        			query += ' WHERE'
        			queryHasWhere = True
        		query += ' day LIKE %s' % day
        	
        	query += ' ORDER BY crime_id DESC'
        	cursor.execute(query)
        	
        	#construct 2d array
        	table = self.createTableFromCursor(cursor)
        	connection.close()
        	return table
        
        #else
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
            
        #else
        return [[]]
        
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