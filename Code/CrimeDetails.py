#!/usr/bin/python
'''
    CRIMR

    CrimeDetails.py (phase_4)

    Eric Walker,
    Charlie Imhoff,
    Graham Earley

    The Google Map Initiation script is pulled from:
        Google
            (developers.google.com)
            (https://developers.google.com/maps/documentation/javascript/examples/marker-simple)
'''
'''
    Crimr | CrimeDetails

    This file prints out an HTML page of a crime with a given ID or a random
    unsolved crime.
'''

import cgi
# import cgitb
# cgitb.enable()

from CrimeDataFetcher import CrimeDataFetcher
from CrimrHTMLBuilder import CrimrHTMLBuilder


#UTILITY METHODS
def cleanInput(str):
    ''' Removes any control characters that our HTML might be screwed up by.
    '''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        str = str.replace(ch, '')
    return str


def getParametersFromFormOrDefaults():
    ''' This method will return an int parameter to identify a crime

        By default, this will return an ID of a random crime from the database, if
        a search cgi parameter is given and is valid, it will return the ID of that
        crime.
    '''
    dataFetcher = CrimeDataFetcher()
    #default is a random unsolved crime
    parameter = dataFetcher.getRandomUnsolvedCrimeID()
    try:
        form = cgi.FieldStorage()
        if 'search' in form:
            tempID = cleanInput(form['search'].value)
            #check if the ID is valid!
            if dataFetcher.getCrimeFromID(tempID):
                parameter = tempID
    except Exception, e:
        pass
    return parameter

#Printing methods
def getPageAsHTML(crimeID):
    ''' Constructs and returns an HTML formatted string that can be printed,
        and thus fill the webpage with content!

        Always shows the links at the bottom and uses getDataAsHTML method to
        get a table of the information and map for the crime.
    '''

    page = CrimrHTMLBuilder.getTopOfHTML('CRIMR')
    page += CrimrHTMLBuilder.getTopOfBody('Crime Details')
    page += getDataAsHTML(crimeID)

    # The random crime button!
    page += '''
            <form action="CrimeDetails.py" method="get">
                <p><input type="submit" value="Get Unsolved Crime!" /></p>
            </form>
            '''

    page += CrimrHTMLBuilder.getClosingHTML()

    return page

def getDataAsHTML(crimeID):
    ''' Returns the crime info from the PSQL database and a google maps map,
        formatted into an HTML String. Will be placed directly into the output
        String of 'getPageAsHTML()'

        The embedded map is retrieved from a template file.
    '''

    outputString = ''
    try:
        dataFetcher = CrimeDataFetcher()

        currentCrimeData = dataFetcher.getCrimeFromID(crimeID)
        headers = ['Crime ID','Category','Description','Day of Week','Date','District','Resolution','X','Y']
        outputString += CrimrHTMLBuilder.getHTMLVertTable(headers,currentCrimeData)

        xCoordinateFromTable = currentCrimeData[7]
        yCoordinateFromTable = currentCrimeData[8]

        # Google map embed:
        mapEmbed = CrimrHTMLBuilder.getTemplate('googleMapEmbed')
        # Fill in the coordinates:
        mapEmbed = mapEmbed.replace('[[X_COORDINATE]]', str(xCoordinateFromTable))
        mapEmbed = mapEmbed.replace('[[Y_COORDINATE]]', str(yCoordinateFromTable))

        outputString += mapEmbed

    except Exception, e:
        outputString += 'Connection error: %s' % e

    return outputString

#main
def main():
    ''' Gets the parameters from cgi input or a random PSQL algorithm and prints
        the page.
    '''
    parameter = getParametersFromFormOrDefaults()
    print CrimrHTMLBuilder.getStartingSequence(),
    print getPageAsHTML(parameter)

if __name__ == '__main__':
    main()
