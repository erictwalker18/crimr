#!/usr/bin/python

'''
    CRIMR

    RandomCrimePage.py (phase_3)

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
from CrimeDetails import CrimeDetails

#UTILITY METHODS
def cleanInput(str):
    ''' Removes any control characters that our HTML might be screwed up by
    '''
    charsToRemove = ';,\\/:\'"<>@'
    for ch in charsToRemove:
        str = str.replace(ch, '')
    return str

#PAGE CONSTRUCTION
def main():
    ''' Gets the parameters from a random algorithm in PSQL, and prints the HTML page
    '''
    dataFetcher=CrimeDataFetcher()
    parameter = dataFetcher.getRandomCrimeID()
    print CrimrHTMLBuilder.getStartingSequence(),
    RandomButton = ''' <p> Click the button to get a random Crime!</p>

            <!-- form -->
            <form action="RandomCrimePage.py" method="get">
                <p><input type="submit" value="Get Random Crime!" /></p>
            </form> '''
    print(CrimeDetails.getPageAsHTML(parameter, RandomButton)),

if __name__ == '__main__':
    main()
