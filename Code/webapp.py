#!/usr/bin/python

'''
	CRIMR

	webapp.py (phase_3)

	Charlie Imhoff,
	Graham Earley,
	Eric Walker
'''

'''
	This file was made with the intention of searching the dataset, but upon further work
	we realized that it was impractical to implement a total search right now.

	Because of this, the user experience currently only searches by District.
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
		fill the webpage with content!

		I thought about linking this to a 'template.html' flat file, but it made more
		sense to me (at this instant) that that technique would be pretty poorly coupled
		as it would require a format string against a file that we would read without
		clear expectations about it's contents. It feels more safe to do it this way,
		even though design and code files aren't supposed to be together.
	'''

	page = CrimrHTMLBuilder.getTopOfHTML('CRIMR')
	page += CrimrHTMLBuilder.getTopOfBody('Homepage')
	page += '''
			<h4>Search</h4>

			<!-- form -->
			%s

			<!-- results get popped in here -->
			%s

			<!-- links -->
			<h4>Source Code</h4>
			<p> <a href="showsource.py?source=webapp.py">webapp.py</a> </p>
			<p> <a href="showsource.py?source=CrimeDataFetcher.py">CrimeDataFetcher.py</a> </p>
			<p> <a href="showsource.py?source=CrimrHTMLBuilder.py">CrimrHTMLBuilder.py</a> </p>
			<p> <a href="showsource.py?source=showsource.py">showsource.py</a> </p>
			
		''' % (getFormAsHTML(parameters), getSearchResultsAsHTML(parameters))
	page += CrimrHTMLBuilder.getClosingHTML()

	return page

def getFormAsHTML(parameters):
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
				by Category:
				<select name="category" id="category">
					<option value="-">--</option>
					<option value="murder">Murder</option>
					<option value="theft">Theft</option>
					<option value="assault">Assault</option>
					<option value="vandalism">Vandalism</option>
					<option value="drug">Drug</option>
					<option value="robbery">Robbery</option>
					<option value="missing">Missing Person</option>
					<option value="non-criminal">Non-Criminal</option>
				</select>
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
				by Resolution:
				<select name="resolution" id="resolution">
					<option value="-">--</option>
					<option value="*resolved*">Resolved</option> #special case
					<option value="none">Unresolved</option>
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
		Will be placed directly into the output String of 'getPageAsHTML(searchString)'
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
