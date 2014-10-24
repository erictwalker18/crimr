#!/usr/bin/python
'''
	CRIMR

	webapp.py (phase_3)

	Charlie Imhoff,
	Graham Earley,
	Eric Walker
'''

'''
	The Homepage for CRIMR.

	The bread and butter of our app, search is home here, as well as
	the primary links to all other CRIMR pages.
'''

import cgi
# import cgitb
# cgitb.enable()

from CrimeDataFetcher import CrimeDataFetcher
from CrimrHTMLBuilder import CrimrHTMLBuilder

#UTILITY METHODS
def cleanInput(str):
	''' Removes any control characters that our HTML might be screwed up by
	'''
	charsToRemove = ';\\:\'"<>@'
	for ch in charsToRemove:
		str = str.replace(ch, '')
	return str

def getParametersFromFormOrDefaults():
	''' This function will always return a py dictionary of the params we care about.

		If no CGI params are passed in, it still creates this dictionary, ensuring
		nothing is calling a None variable
    '''
	parameters = {'search':''}
	try:
		form = cgi.FieldStorage()
		if 'search' in form:
			parameters['search'] = cleanInput(form['search'].value)
		if 'district' in form:
			parameters['district'] = cleanInput(form['district'].value)
		if 'category' in form:
			parameters['category'] = cleanInput(form['category'].value)
		if 'day' in form:
			parameters['day'] = cleanInput(form['day'].value)
		if 'resolution' in form:
			parameters['resolution'] = cleanInput(form['resolution'].value)
	except Exception, e:
		parameters = {'search':'nothing'}
	return parameters



#PAGE CONSTRUCTION
def main():
	''' Gets the parameters from defaults or a cgi form, and prints the HTML page
	'''
	parameters = getParametersFromFormOrDefaults()
	print CrimrHTMLBuilder.getStartingSequence(),
	print(getPageAsHTML(parameters)),

def getPageAsHTML(parameters):
	''' Constructs and returns an HTML formatted string that can be printed, and thus
		fill the webpage with a form and, possibly, results
	'''

	page = CrimrHTMLBuilder.getTopOfHTML('CRIMR')
	page += CrimrHTMLBuilder.getTopOfBody('Homepage')
	page += '''
			<h4>Search</h4>

			<!-- form -->
			%s

			<!-- results get popped in here -->
			%s

		''' % (getFormAsHTML(parameters), getSearchResultsAsHTML(parameters))
	page += CrimrHTMLBuilder.getNavigationLinks()
	page += CrimrHTMLBuilder.getClosingHTML()

	return page

def getFormAsHTML(parameters):
	'''
	Returns valid HTML as a string which represents the search form
	Will be placed directly into the output String of 'getPageAsHTML(parameters)'
	'''
	#most of the form select options are hardcoded in
	#districts will never change in the city, hardcoded
	html = '''<form action="webapp.py" method="get">
				<!-- Text Search Box -->
				<p>Search Crimr:<input type="text" name="search" value="[SEARCH]" /></p>
				<!-- Narrowing Dropdowns -->
				<p>
				by District:
				<select name="district" id="district">
					<option value="-">--</option>
					<option value="tenderloin">Tenderloin</option>
					<option value="central">Central</option>
					<option value="bayview">Bayview</option>
					<option value="ingleside">Ingleside</option>
					<option value="mission">Mission</option>
					<option value="northern">Northern</option>
					<option value="park">Park</option>
					<option value="southern">Southern</option>
					<option value="taraval">Taraval</option>
					<option value="richmond">Richmond</option>
				</select>
			'''
	#categories aren't hardcoded in, due to size and scope
	fetcher = CrimeDataFetcher()
	cats = fetcher.getListOfCategories()
	html += '''By Category:<select name="category" id="category">'''
	html += '''<option value="-">--</option>'''
	for cat in cats:
		html += '''<option value="%s" id="%s">%s</option>''' % (cat.lower(),cat.lower(),cat.title())
	html += '''</select>'''
	#days and resolution types are also static, so they're hardcoded
	html += '''
				by Day of Week:
				<select name="day" id="day">
					<option value="-">--</option>
					<option value="sunday">Sunday</option>
					<option value="monday">Monday</option>
					<option value="tuesday">Tuesday</option>
					<option value="wednsday">Wednesday</option>
					<option value="thursday">Thursday</option>
					<option value="friday">Friday</option>
					<option value="saturday">Saturday</option>
				</select>
			'''
	#resolution types flagged with * represent special searches to CrimeDataFetcher
	html += '''
				by Resolution:
				<select name="resolution" id="resolution">
					<option value="-">--</option>
					<option value="*resolved*">Resolved</option> #special case
					<option value="*unresolved*">Unresolved</option>
					<option value="arrest">Arrest</option>
					<option value="book">Booking</option>
					<option value="cite">Citing</option>
					<option value="psychopathic">Psychopathic Case</option>
					<option value="not prosecute">Not Prosecuted</option>
				</select>
				</p>
				<p><input type="submit" value="Find Crime" /></p>
			</form>'''
	filledHtml = html.replace('[SEARCH]',parameters['search'])
	return filledHtml

def getSearchResultsAsHTML(parameters):
	''' Returns the search results form the PSQL database, formatted into an HTML String
		Will be placed directly into the output String of 'getPageAsHTML(parameters)'
	'''
	outputString = ''
	try:
		dataFetcher = CrimeDataFetcher()
		try:
			outputTable = dataFetcher.getCrimesForSearch(parameters)
			headers = ['Crime ID','Category','Description','Day of Week','Date','District','Resolution','X','Y']
			outputString += CrimrHTMLBuilder.getHTMLTable(headers,outputTable)
		except Exception, e:
			outputString +=  'Cursor error: %s' % e
	except Exception, e:
		outputString += 'Connection error: %s' % e

	return outputString

if __name__ == '__main__':
	main()
