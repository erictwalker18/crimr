#!/usr/bin/python

import cgi

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
			<title>webapptest</title>
		</head>

		<body>
			<h2>webapptest.py</h2>
			
			<!-- form -->
			<form action="webapptest.py" method="get">
				<p>Search Crimr:<input type="text" name="search" value="%s" /></p>
				<p><input type="submit" value="Go" /></p>
			</form>

			<!-- results get popped in here -->
			%s
			
			<!-- links -->

		</body>
		</html>
		''' % (searchString, getSearchResultsAsHTML(searchString))
		
	return page
		
def getSearchResultsAsHTML(searchString):
	''' Returns the search results form the PSQL database, formatted into an HTML String
		Will be placed directly into the output String of 'getPageAsHTML(searchString)'
	'''
	#TODO : Implement
	if searchString == '':
		return '''<p>Search using the field above to get started!</p>'''
	else:
		return '''<p>Search Results for : %s</p>''' % searchString


if __name__ == '__main__':
	main()