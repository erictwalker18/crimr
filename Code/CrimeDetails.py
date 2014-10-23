#!/usr/bin/python

'''
    CRIMR

    CrimeDetails.py (phase_3)

    Eric Walker,
    Charlie Imhoff,
    Graham Earley
'''

'''
    This file prints out an HTML page of a crime with a given ID or a random
    unsolved crime.
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

#main
def main():
    ''' Gets the parameters from cgi input or a random PSQL algorithm and prints
        the page.
    '''
    parameter = getParametersFromFormOrDefaults()
    print CrimrHTMLBuilder.getStartingSequence(),
    print getPageAsHTML(parameter)

#Printing methods
def getPageAsHTML(crimeID):
    ''' Constructs and returns an HTML formatted string that can be printed,
        and thus fill the webpage with content!

        Always shows the links at the bottom and uses getDataAsHTML method to
        get a table of the information and map for the crime.
    '''

    page = CrimrHTMLBuilder.getTopOfHTML('CRIMR')
    page += CrimrHTMLBuilder.getTopOfBody('Crime Details')
    page += '''
            <!-- results get popped in here -->
            <div id="info">
            %s
            </div>

            <div id="features">
            
            </div>
            <!-- Get Random Unsolved Crime Button -->

            <!-- form -->
            <form action="CrimeDetails.py" method="get">
                <p><input type="submit" value="Get Unsolved Crime!" /></p>
            </form>
            <!-- links -->
            <h4>Source Code</h4>
            <p> <a href="showsource.py?source=CrimeDetails.py">CrimeDetails.py</a> </p>
            <p> <a href="showsource.py?source=CrimeDataFetcher.py">CrimeDataFetcher.py</a> </p>
            <p> <a href="showsource.py?source=CrimrHTMLBuilder.py">CrimrHTMLBuilder.py</a> </p>
            <p> <a href="showsource.py?source=showsource.py">showsource.py</a> </p>
            
        ''' % (getDataAsHTML(crimeID))
    page += CrimrHTMLBuilder.getClosingHTML()

    return page

def getDataAsHTML(crimeID):
    ''' Returns the search results form the PSQL database and a google maps map,
        formatted into an HTML String. Will be placed directly into the output
        String of 'getPageAsHTML()'
    '''

    outputString = ''
    try:
        dataFetcher = CrimeDataFetcher()
        try:
            outputTable = dataFetcher.getCrimeFromID(crimeID)
            headers = ['Crime ID','Category','Description','Day of Week','Date','District','Resolution','X','Y']
            outputString += CrimrHTMLBuilder.getHTMLVertTable(headers,outputTable)
            #Google map embed:
            outputString+='''
                <!-- Google map script and div that it pops into -->
                <script
                src="http://maps.googleapis.com/maps/api/js?key=AIzaSyDY0kkJiTPVd2U7aTOAwhc9ySH6oHxOIYM&sensor=false">
                </script>

                <script>
                function initialize() {
                var mapProp = {
                    center:new google.maps.LatLng(%s,%s),
                    zoom:19,
                    mapTypeId:google.maps.MapTypeId.ROADMAP };
                    var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
                }

                google.maps.event.addDomListener(window, 'load', initialize);
                </script>
                <div id="googleMap" style="width:500px;height:380px;"></div>

                
                ''' %(outputTable[0][8], outputTable[0][7])
        except Exception, e:
            outputString +=  'Cursor error: %s' % e
    except Exception, e:
        outputString += 'Connection error: %s' % e

    return outputString

if __name__ == '__main__':
    main()
