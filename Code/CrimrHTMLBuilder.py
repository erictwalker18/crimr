#!/usr/bin/python
'''
    CRIMR

    CrimrHTMLBuilder.py (phase_3)

    Charlie Imhoff,
    Graham Earley,
    Eric Walker
'''
import cgitb
cgitb.enable()
import re   #regex checking module
from CrimeDataFetcher import CrimeDataFetcher

'''
    CrimrHTMLBuilder allows a quick, easy way to get reusable, flexible
    blocks of HTML via a cleaner interface than directly printing in Python
    main methods.

    Most methods insert information into template HTML files, but there
    are a couple that are so dynamic that it is more efficient to simply
    generate the whole return string in this file.
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
            setting param title as the title.

            The HTML is loaded from a template file.
        '''
        templateFile = open('templates/topOfHTML.partial.html', 'r')
        html = templateFile.read()
        htmlWithTitle = html.replace('[[TITLE]]',title)
        return htmlWithTitle

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

            This method doesn't involve a template file because the table size isn't fixed;
            it involves a loop.
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

            Again, this method doesn't involve a template file because the table size isn't fixed;
            it involves a loop.
        '''
        html = '<table border="1">'
        if headings is not None and data is not None:
            i=0
            for header in headings:
                html += '<tr>'
                html += '<th>%s</th>' % header
                html+= '<td>%s</td>' % data[i]
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
            and adds the CRIMR logo and the header parameter.

            The HTML is loaded from a template file.
        '''
        templateFile = open('templates/topOfBody.partial.html', 'r')
        html = templateFile.read()

        htmlWithHeader = html.replace('[[SUBPAGE_HEADER]]', subpageHeader)
        return htmlWithHeader

    @staticmethod
    def getNavigationLinks():
        '''
            Returns an HTML string which links the user to the secondary
            features of CRIMR.

            The HTML is loaded from a template file.
        '''
        templateFile = open('templates/navigation.partial.html', 'r')
        html = templateFile.read()

        return html

    @staticmethod
    def getTemplate(fileName):
        '''
            Returns the content of any template file in the /templates
            directory.

            The 'fileName' parameter should only be the name of the file
            (no directories or filetypes included!)
        '''
        fileString = 'templates/'
        fileString += fileName
        fileString += '.partial.html'

        templateFile = open(fileString, 'r')
        return templateFile.read()

    @staticmethod
    def getClosingHTML():
        '''
            Returns an HTML string which closes the Body & HTML tags
            as well as inserts the link to the readme.html page

            The HTML is loaded from a template file.
        '''
        templateFile = open('templates/footer.partial.html', 'r')
        return templateFile.read()
