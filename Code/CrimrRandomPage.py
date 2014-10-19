#!/usr/bin/python

'''
    CRIMR

    CrimrRandomCrime.py (phase_3)

    Eric Walker,
    Charlie Imhoff,
    Graham Earley
'''

'''
    This file returns the html code for a page that shows the details of a random crime.
'''

import cgi
#import cgitb
#cgitb.enable()

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

def getIDNumber():
    ''' This function will always return a py dictionary of the params we care about.

        It works by either filling in and cleaning these params from a CGI form,
        or if none exists it just goes ahead and defines them as a blank string,
        instead of nil (or whatever null value Python uses...)
    '''
    return getRandomCrimeID()


#PAGE CONSTRUCTION
def main():
    ''' Gets the parameters from a random algorithm in PSQL, and prints the HTML page
    '''
    parameter = getIDNumber()
    print CrimrHTMLBuilder.getStartingSequence(),
    print(getPageAsHTML(parameter)),

def getPageAsHTML(searchString):
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
            <h4>Random Crime</h4>
            <p> Click the button to get a random Crime!</p>

            <!-- form -->
            <form action="CrimrRandomPage.py" method="get">
                <p><input type="submit" value="Get Random Crime!" /></p>
            </form>

            <!-- results get popped in here -->
            %s

            <!-- links -->
            <h4>Source Code</h4>
            <p> <a href="showsource.py?source=CrimrRandomPage.py">CrimrRandomPage.py</a> </p>
            <p> <a href="showsource.py?source=CrimeDataFetcher.py">CrimeDataFetcher.py</a> </p>
            <p> <a href="showsource.py?source=CrimrHTMLBuilder.py">CrimrHTMLBuilder.py</a> </p>
            <p> <a href="showsource.py?source=showsource.py">showsource.py</a> </p>
            
        ''' % (getSearchResultsAsHTML(searchString))
    page += CrimrHTMLBuilder.getClosingHTML()

    return page

def getSearchResultsAsHTML():
    ''' Returns the search results form the PSQL database, formatted into an HTML String
        Will be placed directly into the output String of 'getPageAsHTML()'
    '''

    outputString = ''
    try:
        dataFetcher = CrimeDataFetcher()
        try:
            outputTable = dataFetcher.getAllCrimesFromDistrict(searchString)
            headers = ['Crime ID','Category','Description','Day of Week','Date','District','Resolution','X','Y']
            outputString += CrimrHTMLBuilder.getHTMLTable(headers,outputTable)
        except Exception, e:
            outputString +=  'Cursor error: %s' % e
    except Exception, e:
        outputString += 'Connection error: %s' % e

    return outputString

if __name__ == '__main__':
    main()
