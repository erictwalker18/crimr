#!/usr/bin/python
'''
	CRIMR

	index.py (phase_3)

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
import cgitb
cgitb.enable()

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
	districts = ["Tenderloin", "Central", "Bayview", "Ingleside", "Mission", "Northern", "Park", "Southern", "Taraval", "Richmond"]
	html = '''<form action="index.py" method="get">
				<!-- Text Search Box -->
				<p>Search Crimr:<input type="text" name="search" value="[SEARCH]" /></p>
				<!-- Narrowing Dropdowns -->
				<p>
				by District:
				<select name="district" id="district">
				'''
	html += '''<option value="-">--</option>'''
	for district in districts:
		html+= '''<option value="%s">%s</option>''' % (district.lower(), district)
	html+= '''</select>'''

	#categories aren't hardcoded in, due to size and scope
	fetcher = CrimeDataFetcher()
	cats = fetcher.getListOfCategories()
	html += '''By Category:<select name="category" id="category">'''
	html += '''<option value="-">--</option>'''
	for cat in cats:
		html += '''<option value="%s" id="%s">%s</option>''' % (cat.lower(),cat.lower(),cat.title())
	html += '''</select>'''

	#days and resolution types are also static, so they're hardcoded
	daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	html += '''
				by Day of Week:
				<select name="day" id="day">
			'''
	html += '''<option value="-">--</option>'''
	for day in daysOfWeek:
		html+= '''<option value="%s">%s</option>''' % (day.lower(), day)
	html += '''</select>'''

	#resolution types flagged with * represent special searches to CrimeDataFetcher
	resolutions = ["*Resolved*", "*Unresolved*", "Arrest", "Booking", "Citing", "Psychopathic", "Not Prosecute"]
	html += '''
				by Resolution:
				<select name="resolution" id="resolution">
			'''
	html += '''<option value="-">--</option>'''
	for resolution in resolutions:
		html += '''<option value="%s">%s</option>''' % (resolution.lower(), resolution)
	html += '''
				</select>
				</p>
				<p><input type="submit" value="Find Crime" /></p>
			</form>'''

	#to keep the default values for the dropdown menus
	lowerDistricts = ["tenderloin", "central", "bayview", "ingleside", "mission", "northern", "park", "southern", "taraval", "richmond"]
	if 'district' in parameters and parameters['district'] in lowerDistricts:
		strToReplace = 'value="%s"' % parameters['district']
		replacementString = 'selected="selected" value="%s"' % parameters['district']
		html = html.replace(strToReplace, replacementString)

	lowerCats = []
	for s in cats:
		lowerCats.append(s.lower())
	if 'category' in parameters and parameters['category'] in lowerCats:
		strToReplace = 'value="%s"' % parameters['category']
		replacementString = 'selected="selected" value="%s"' % parameters['category']
		html = html.replace(strToReplace, replacementString)

	lowerDaysOfWeek = []
	for s in daysOfWeek:
		lowerDaysOfWeek.append(s.lower())
	if 'day' in parameters and parameters['day'] in lowerDaysOfWeek:
		strToReplace = 'value="%s"' % parameters['day']
		replacementString = 'selected="selected" value="%s"' % parameters['day']
		html = html.replace(strToReplace, replacementString)

	lowerResolutions = []
	for s in resolutions:
		lowerResolutions.append(s.lower())
	if 'resolution' in parameters and parameters['resolution'] in lowerResolutions:
		strToReplace = 'value="%s"' % parameters['resolution']
		replacementString = 'selected="selected" value="%s"' % parameters['resolution']
		html = html.replace(strToReplace, replacementString)

	filledHtml = html.replace('[SEARCH]',parameters['search'])


	return filledHtml

def getSearchResultsAsHTML(parameters):
	''' Returns the search results form the PSQL database, formatted into an HTML String
		Will be placed directly into the output String of 'getPageAsHTML(parameters)'
	'''
	outputString = ''
	dataFetcher = CrimeDataFetcher()
	try:
		outputTable = dataFetcher.getCrimesForSearch(parameters)
		if outputTable is not None:	#print nothing if there was no search
			headers = ['Crime ID','Category','Description','Day of Week','Date','District','Resolution','X','Y']
			outputString += CrimrHTMLBuilder.getHTMLTable(headers,outputTable)
		else:
			outputString += 'Use the controls above to get searching'
	except Exception, e:
		outputString +=  'Connection/Cursor Error: %s' % e

	return outputString

if __name__ == '__main__':
	main()
