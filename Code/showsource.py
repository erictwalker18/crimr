#!/usr/bin/python
'''
	used by CRIMR

	showsource.py (phase_4)

	Eric Walker,
	Charlie Imhoff,
	Graham Earley
'''
''' showsource.py
    Jeff Ondich, 16 October 2013

    For all my web application samples, I want you to be able to execute
    the server-side code and to view its source. I was using an awkward
    system for providing access to the source code, so I'm going to try
    this simpler idea. We'll see if it's any easier to use.
'''

import cgi

def printFileAsPlainText(fileName):
    ''' Prints to standard output the contents of the specified file, preceded
        by a "Content-type: text/plain" HTTP header.
    '''
    text = ''
    try:
        f = open(fileName)
        text = f.read()
        f.close()
    except Exception, e:
        pass

    print 'Content-type: text/plain\r\n\r\n',
    print text

if __name__ == '__main__':
    # Not going to allow people to view just anything.
    allowedFiles = (
        'showsource.py',
        'webapp.py',
	    'CrimeDataFetcher.py',
        'CrimeScorePage.py',
        'CrimeScore.py',
        'CrimeDetails.py',
        'CrimrHTMLBuilder.py',
        'style.css',
        'index.py',
        'Dataset_Cleaning/CSVcleaner.py'
    )

    # Really. Don't trust the user.
    form = cgi.FieldStorage()
    sourceFileName = 'showsource.py'
    if 'source' in form:
        sourceFileName = form['source'].value
    if sourceFileName not in allowedFiles:
        sourceFileName = 'showsource.py'

    # Print the file in question.
    printFileAsPlainText(sourceFileName)
