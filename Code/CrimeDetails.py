#!/usr/bin/python

'''
    CRIMR

    CrimeDetails.py (phase_3)

    Eric Walker,
    Charlie Imhoff,
    Graham Earley
'''

'''
    This file returns the html code for a page that shows the details of a random crime.
'''

import cgi
import cgitb
cgitb.enable()

from CrimeDataFetcher import CrimeDataFetcher
from CrimrHTMLBuilder import CrimrHTMLBuilder

class CrimeDetails:
    #UTILITY METHODS
    @staticmethod
    def cleanInput(str):
        ''' Removes any control characters that our HTML might be screwed up by
        '''
        charsToRemove = ';,\\/:\'"<>@'
        for ch in charsToRemove:
            str = str.replace(ch, '')
        return str

    @staticmethod
    def getPageAsHTML(crimeID, otherText):
        ''' Constructs and returns an HTML formatted string that can be printed, and thus
            fill the webpage with content!

            I thought about linking this to a 'template.html' flat file, but it made more
            sense to me (at this instant) that that technique would be pretty poorly coupled
            as it would require a format string against a file that we would read without
            clear expectations about it's contents. It feels more safe to do it this way,
            even though design and code files aren't supposed to be together.
        '''

        page = CrimrHTMLBuilder.getTopOfHTML('CRIMR')
        page += CrimrHTMLBuilder.getTopOfBody('Crime Details')
        page += '''

                <!-- other stuff pops in here -->
                %s

                <!-- results get popped in here -->
                <div id="info">
                %s
                </div>

                <div id="features">
                
                </div>

                <!-- links -->
                <h4>Source Code</h4>
                <p> <a href="showsource.py?source=RandomCrimePage.py">RandomCrimePage.py</a> </p>
                <p> <a href="showsource.py?source=CrimeDetails.py">CrimeDetails.py</a> </p>
                <p> <a href="showsource.py?source=CrimeDataFetcher.py">CrimeDataFetcher.py</a> </p>
                <p> <a href="showsource.py?source=CrimrHTMLBuilder.py">CrimrHTMLBuilder.py</a> </p>
                <p> <a href="showsource.py?source=showsource.py">showsource.py</a> </p>
                
            ''' % (otherText, CrimeDetails.getDataAsHTML(crimeID))
        page += CrimrHTMLBuilder.getClosingHTML()

        return page

    @staticmethod
    def getDataAsHTML(crimeID):
        ''' Returns the search results form the PSQL database, formatted into an HTML String
            Will be placed directly into the output String of 'getPageAsHTML()'
        '''

        outputString = ''
        try:
            dataFetcher = CrimeDataFetcher()
            try:
                outputTable = dataFetcher.getCrimeFromID(crimeID)
                headers = ['Crime ID','Category','Description','Day of Week','Date','District','Resolution','X','Y']
                outputString += CrimrHTMLBuilder.getHTMLVertTable(headers,outputTable)
                outputString+='''
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

