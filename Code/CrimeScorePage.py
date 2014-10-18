#!/usr/bin/python

'''
  CRIMR

  NOT FINALIZED

  DO NOT RELEASE!!

'''

import cgi
import cgitb
cgitb.enable()

from CrimeDataFetcher import CrimeDataFetcher
from CrimeScore import CrimeScore

#UTILITY METHODS
def getCategoryList():
  '''Make this query the database!'''

  return ["ARSON", "ASSAULT", "BAD CHECKS", "BRIBERY", "BURGLARY", "DISORDERLY CONDUCT", "DRIVING UNDER THE INFLUENCE", "DRUG/NARCOTIC", "DRUNKENNESS", "EMBEZZLEMENT", "EXTORTION", "FAMILY OFFENSES", "FORGERY/COUNTERFEITING", "FRAUD", "GAMBLING", "KIDNAPPING", "LARCENY/THEFT", "LIQUOR LAWS", "LOITERING", \
  "MISSING PERSON", "NON-CRIMINAL", "OTHER OFFENSES", "PORNOGRAPHY/OBSCENE MATERIAL", "PROSTITUTION", "ROBBERY", "RUNAWAY", "SEX OFFENSES, FORCIBLE", "SEX OFFENSES, NON-FORCIBLE", "STOLEN PROPERTY", "SUICIDE", "SUSPICIOUS OCC", "TRESPASS", "VANDALISM", "VEHICLE THEFT", "WARRANTS", "WEAPON LAWS"]

def getRatingsHashFromForm():
  ''' COMMENT
  '''
  categories = getCategoryList()
  parameters = {}
  try:
    form = cgi.FieldStorage()
    for category in categories:
      if category in form:
        try:
          parameters[category] = int(form[category].value)
          # ^ By design of the form, these results will be strings
          # of numbers. So take int() of these strings.
          # Just in case int() raises an error, though:
        except Exception, e:
          parameters[category] = 0

  except Exception, e:
    parameters = {'ERROR':e}

  return parameters

#PAGE CONSTRUCTION
def main():
  ''' Gets the category ratings, and prints the HTML page
  '''
  print '''Content-type: text/html\r\n\r\n''',
  print(getPageAsHTML()),

def getPageAsHTML():
  ''' Constructs and returns an HTML formatted string that can be printed, and thus
    fill the webpage with content!

    I thought about linking this to a 'template.html' flat file, but it made more
    sense to me (at this instant) that that technique would be pretty poorly coupled
    as it would require a format string against a file that we would read without
    clear expectations about it's contents. It feels more safe to do it this way,
    even though design and code files aren't supposed to be together.
  '''

  page = '''<!DOCTYPE HTML>'''
  page += '''<html>
    <head>
      <title>CrimeScore</title>
      <script src="http://code.jquery.com/jquery-git2.js"></script>
    </head>

    <body>
      <h1>Crime Score</h1>
      <h2>%s</h2>

      <h3> Rate the crimes that scare you!</h3>
      <p>For each category below, consider how scary those types of crimes are to you.</p>
      <i>(0 = not scary, 10 = horrifying)</i>
      </br>

      <!-- form gets popped in here-->
      %s

      <!-- links -->
      <hr>
      <h4>Source Code</h4>
      <p> <a href="showsource.py?source=CrimeScore.py">CrimeScore.py Source Code</a> </p>
      <p> <a href="showsource.py?source=CrimeScorePage.py">CrimeScorePage.py Source Code</a> </p>
      <p> <a href="showsource.py?source=CrimeDataFetcher.py">CrimeDataFetcher.py Source Code</a> </p>
      <p> <a href="showsource.py?source=showsource.py">showsource.py Source Code</a> </p>


    </body>
    </html>
    ''' % (getCrimeScoreHTMLString(), getFormHTML())

  return page

def getFormHTML():
  categories = getCategoryList()
  outputString = '<form action="CrimeScorePage.py" method="get">'

  tableEntryIndex = 0
    # tableEntryIndex is used for splitting the table up.
  outputString+= "<table style='width:100%'><tr align='center'>"
  for category in categories:
    if tableEntryIndex % 3 == 0:
      # After each third entry, end the row and start a new one:
      outputString += "</tr><tr align='center'>"

    # Add a 'select' form element for each category, with options
    # 0 through 10 for ratings. Put them in a center-aligned table
    # so it isn't overwhelming / ugly:
    outputString += "<td>"
    outputString += "<p>%s: </p>" % category
    outputString += '<select name="%s" id=%s>' % (category, category)
    for num in range(0,11):
      outputString+= '<option value="%s">%i</option>' % (str(num), num)
    outputString += '</select>'
    outputString += "</td>"

    tableEntryIndex += 1

  outputString += "</tr>" # Close off the last table row.
  outputString += "</table>"

  outputString+= '<p><input type="submit" value="Calculate CrimeScore" /></p>'
  outputString += '</form>'

  return outputString

def getCrimeScoreHTMLString():
  ratingsHash = getRatingsHashFromForm()
  cs = CrimeScore(ratingsHash)
  score = cs.calculateCrimeScore()

  if ratingsHash.keys == ['ERROR'] or len(ratingsHash) == 0:
    return ""
  else: #so, if the hash table is populated
    return "<i>Your CrimeScore:</i> <b>%i</b>" % score

  return HTMLstring


if __name__ == '__main__':
  main()
