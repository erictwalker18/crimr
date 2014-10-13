#!/usr/bin/python

'''
	CRIMR
	
	webapp.py (phase_2)
	
	Charlie Imhoff,
	Graham Earley,
	Eric Walker
'''

'''
	This file was made with the intention of searching the dataset, but upon further work
	we realized that it was impractical to implement a total search right now.
	
	Because of this, the user experience now using a form to ask for an appeasement, before the
	data is loaded. This is filed around as a 'search', and comments in this document refer to it
	as such. But it is not a search, it's simply an activator for the form.
'''

import cgi
import cgitb
cgitb.enable()
import psycopg2

#UTILITY METHODS
def cleanInput(str):
	''' Removes any control characters that out HTML might be screwed up by
	'''
	charsToRemove = ';,\\/:\'"<>@'
	for ch in charsToRemove:
		str = str.replace(ch, '')
	return str

def getParametersFromFormOrDefaults():
	''' This function will always return a py dictionary of the params we care about.
		
		It works by either filling in and cleaning these params from a CGI form, 
		or if none exists it just goes ahead and defines them as a blank string, 
		instead of nil (or whatever null value Python uses...)
    '''
	parameters = {'search':''}
	try:
		form = cgi.FieldStorage()
		if 'search' in form:
			parameters['search'] = cleanInput(form['search'].value)
	except Exception, e:
		parameters = {'search':'nothing'}
	return parameters
	
	
	
#PAGE CONSTRUCTION	
def main():
	''' Gets the parameters from defaults or a cgi form, and prints the HTML page
	'''
	parameters = getParametersFromFormOrDefaults()
	print '''Content-type: text/html\r\n\r\n''',
	print(getPageAsHTML(parameters['search'])),

def getPageAsHTML(searchString):
	''' Constructs and returns an HTML formatted string that can be printed, and thus
		fill the webpage with content!
		
		I thought about linking this to a 'template.html' flat file, but it made more
		sense to me (at this instant) that that technique would be pretty poorly coupled
		as it would require a format string against a file that we would read without
		clear expectations about it's contents. It feels more safe to do it this way,
		even though design and code files aren't supposed to be together.
	'''
	
	page = '''<!DOCTYPE HTML>'''
	page += '''<html>
		<head>
			<title>webapp</title>
		</head>

		<body>
			<h2>webapp.py</h2>
			
			<!-- form -->
			<form action="webapp.py" method="get">
				<p>Appease Us:<input type="text" name="search" value="%s" /></p>
				<p><input type="submit" value="Find All Crime in Tenderloin District!" /></p>
			</form>

			<!-- results get popped in here -->
			%s
			
			<!-- links -->
			<p> <a href="showsource.py?source=webapp.py">Source Code</a> </p>

		</body>
		</html>
		''' % (searchString, getSearchResultsAsHTML(searchString))
		
	return page
		
def getSearchResultsAsHTML(searchString):
	''' Returns the search results form the PSQL database, formatted into an HTML String
		Will be placed directly into the output String of 'getPageAsHTML(searchString)'
	'''
	
	if searchString == '':
		return 'type something in to make us like you, then we\'ll print results'
	
	outputString = ''
	try:
		connection = psycopg2.connect(database='earleyg', user='earleyg', password='field799java')
		try:
			cursor = connection.cursor()
			query = 'SELECT * FROM crimes WHERE district=\'TENDERLOIN\' ORDER BY crime_id DESC'
			cursor.execute(query)
			outputString += '<table border="1">'
			outputString += '<tr> <th>Crime ID</th> <th>Category</th> <th>Description</th> <th>Day of Week</th> <th>Date</th> <th>District</th> <th>Resolution</th> </tr>'
			for row in cursor:
				outputString += '<tr> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> </tr>' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
			outputString += '</table>'
	
		except Exception, e:
			outputString +=  'Cursor error', e
	except Exception, e:
		outputString += 'Connection error: ', e
									
	return outputString

if __name__ == '__main__':
	main()
