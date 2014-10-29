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

	page += '<h4>Search</h4>'
	page += getFormAsHTML(parameters)
	page += getSearchResultsAsHTML(parameters)

	page += CrimrHTMLBuilder.getNavigationLinks()
	page += CrimrHTMLBuilder.getClosingHTML()

	return page

def getFormAsHTML(parameters):
	'''
	Returns valid HTML as a string which represents the search form
	Will be placed directly into the output String of 'getPageAsHTML(parameters)'

	Uses an HTML template for the most part (assembles one form due for scalability purposes)
	'''

	html = CrimrHTMLBuilder.getTemplate('mainSearchForm')
	# Most of the search form options are for static elements of the dataset that
	#  aren't likely to change (e.g. days of week, districts). Thus they are
	#  hardcoded into the template file.

	# However, due to potential for new categories in future updates to the dataset,
	#  the category select form options are assembled by grabbing all the categories
	#  from the database:
	fetcher = CrimeDataFetcher()
	categories = fetcher.getListOfCategories()
	categoryFormString = ''
	for category in categories:
		categoryFormString += '<option value="%s" id="%s">%s</option>' % (category.lower(),category.lower(),category.title())
	html = html.replace('[[CATEGORIES_SELECT_FORM_OPTIONS]]', categoryFormString)

	#Preserve Search Form on page refresh
	#Keep values for the dropdown menus
	lowerDistricts = ["tenderloin", "central", "bayview", "ingleside", "mission", "northern", "park", "southern", "taraval", "richmond"]
	if 'district' in parameters and parameters['district'] in lowerDistricts:
		strToReplace = 'value="%s"' % parameters['district']
		replacementString = 'selected="selected" value="%s"' % parameters['district']
		html = html.replace(strToReplace, replacementString)

	lowerCats = []
	for s in categories:
		lowerCats.append(s.lower())
	if 'category' in parameters and parameters['category'] in lowerCats:
		strToReplace = 'value="%s"' % parameters['category']
		replacementString = 'selected="selected" value="%s"' % parameters['category']
		html = html.replace(strToReplace, replacementString)

	lowerDaysOfWeek = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
	if 'day' in parameters and parameters['day'] in lowerDaysOfWeek:
		strToReplace = 'value="%s"' % parameters['day']
		replacementString = 'selected="selected" value="%s"' % parameters['day']
		html = html.replace(strToReplace, replacementString)

	lowerResolutions = ['*all*', '*resolved*', '*unresolved*', 'arrest', 'book', 'cite', 'psychopathic', 'not prosecute']
	if 'resolution' in parameters and parameters['resolution'] in lowerResolutions:
		strToReplace = 'value="%s"' % parameters['resolution']
		replacementString = 'selected="selected" value="%s"' % parameters['resolution']
		html = html.replace(strToReplace, replacementString)

	# Keep the search box filled in:
	html = html.replace('[[SEARCH]]',parameters['search'])

	return html

def getSearchResultsAsHTML(parameters):
	''' Returns the search results from the PSQL database, formatted into an HTML String
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
