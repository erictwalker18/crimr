#!/usr/bin/python
'''
    CRIMR

    CrimrHTMLBuilder.py (phase_3)

    Charlie Imhoff,
    Graham Earley,
    Eric Walker
'''
# import cgitb
# cgitb.enable()
import re   #regex checking module
from CrimeDataFetcher import CrimeDataFetcher

'''
    CrimrHTMLBuilder allows a quick, easy way to get reusable, flexible
    blocks of HTML via a cleaner interface than directly printing in Phython
    main methods.

    Allows us to have the wonders of both a code interface and a template file,
    without the downsides of managing a bunch of flat .HTML files
'''

class CrimrHTMLBuilder:

    @staticmethod
    def getStartingSequence():
        '''
            Returns the sequence that Python must first print before
            the print stream is read as HTML
        '''
        return '''Content-type: text/html\r\n\r\n'''

    @staticmethod
    def getTopOfHTML(title):
        '''
            Returns an HTML string which starts the HTML tag
            and fills in all the header info,
            setting param title as the title
        '''

        template = '''<!DOCTYPE HTML>
        <html>
        <head>
        <link rel="stylesheet" type="text/css" href="style.css" />
        <title>[[TITLE]]</title>
        </head>'''
        html = template.replace('[[TITLE]]',title)
        return html

    @staticmethod
    def getHTMLTable(headings, data):
        '''
            Returns an HTML string which creates, fills and closes a Table tag.
            Automagically detects crime_ids and converts them to CrimeDetail page links

            This parameter setup is designed to interface
            simply with CrimeDataFetcher.py

            params:
                - headings : String[]? : Gets formatted into the list as a header row
                - data : String[][] : Gets formatted into the html as a table
                if data is at all empty, an HTML error message is returned
        '''
        if len(data) == 0:
            return '<p>No Results</p>'
        html = '<table border="1">'
        if headings is not None:
            #fill in a header row
            html += '<tr>'
            for header in headings:
                html += '<th>%s</th>' % header
            html += '</tr>'
        if data is not None:
            for row in data:
                html += '<tr>'
                for cell in row:
                    cellInnerHtml = cell
                    #matches crime ids but not x/y coordinants
                    crimeIdRegexPattern = re.compile("^\d+$")
                    matchObject = crimeIdRegexPattern.match(str(cell))

                    if matchObject is not None: #if the regex matched
                        #replace crime_id with a link for more details
                        cellInnerHtml = '<a href="CrimeDetails.py?search=%s">%s</a>' % (cell,cell)
                    html += '<td>%s</td>' % cellInnerHtml
                html += '</tr>'
        html += '</table>'
        return html

    @staticmethod
    def getHTMLVertTable(headings, data):
        '''
                Returns an HTML string that creates, fills, and closes
                a vertical Table tag.

                This parameter setup is designed to interface
                with CrimeDataFetcher.py

                params:
                        -headings: String[] : Gets formatted into the list as the header column
                        -data: String[]? : Gets formatted into the html as a table
        '''
        html = '<table border="1">'
        if headings is not None and data is not None:
            i=0
            for header in headings:
                html += '<tr>'
                html += '<th>%s</th>' % header
                html+= '<td>%s</td>' % data[0][i]
                html += '</tr>'
                i += 1
        elif headings is not None:
            for header in headings:
                html += '<th>%s</th>' % header
            html += '</tr>'

        html += '</table>'
        return html

    @staticmethod
    def getTopOfBody(subpageHeader):
        '''
            Returns an HTML string which starts the Body tag
            and fills in the first two headers (first one is CRIMR,
            second one is from parameter)
        '''

        template = '''<body>
        <a href="webapp.py">
        <img src="Logo.png" alt="CRIMR" width="164" height="59">
        </a>
        <h2>[[SUBPAGE_HEADER]]</h2>
        '''
        html = template.replace('[[SUBPAGE_HEADER]]',subpageHeader)
        return html

    @staticmethod
    def getNavigationLinks():
        '''
            Returns an HTML string which links the user to the secondary
            features of CRIMR
        '''
        dataFetcher = CrimeDataFetcher()
        return '''<hr>
        <h2>Other Features</h2>
        <h3><a href="CrimeScorePage.py">CrimeScore:</a> get a personalized crime score</h3>
        <h3><a href="CrimeDetails.py?search=%s">Vigilante Button:</a> get a random, unsolved crime</h3>
        ''' % dataFetcher.getRandomUnsolvedCrimeID()

    @staticmethod
    def getClosingHTML():
        '''
            Returns an HTML string which closes the Body & HTML tags
            as well as inserts the link to the readme.html page
        '''
        return '''<hr>
        <p><i>CRIMR : imhoffc, earleyg, walkere</i></p>
        <p><a href="readme.html">Project ReadMe</a></p>
        </body></html>'''
