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
  ''' Returns a list of the categories of crime
      (using CrimeDataFetcher to query the database)
  '''
              '''Make this query the database!'''###

  return ["ARSON", "ASSAULT", "BAD CHECKS", "BRIBERY", "BURGLARY", "DISORDERLY CONDUCT", "DRIVING UNDER THE INFLUENCE", "DRUG/NARCOTIC", "DRUNKENNESS", "EMBEZZLEMENT", "EXTORTION", "FAMILY OFFENSES", "FORGERY/COUNTERFEITING", "FRAUD", "GAMBLING", "KIDNAPPING", "LARCENY/THEFT", "LIQUOR LAWS", "LOITERING", \
  "MISSING PERSON", "NON-CRIMINAL", "OTHER OFFENSES", "PORNOGRAPHY/OBSCENE MATERIAL", "PROSTITUTION", "ROBBERY", "RUNAWAY", "SEX OFFENSES, FORCIBLE", "SEX OFFENSES, NON-FORCIBLE", "STOLEN PROPERTY", "SUICIDE", "SUSPICIOUS OCC", "TRESPASS", "VANDALISM", "VEHICLE THEFT", "WARRANTS", "WEAPON LAWS"]

def getRatingsHashFromForm():
  ''' Uses the CGI library to pull out the user's
      ratings of the crime categories. Then, it returns
      them in a Python dictionary.
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
    # If there's an error with the form, the dictionary will
    # return with a key and value of zero.
    parameters = {"ERROR":0}

  return parameters


#PAGE CONSTRUCTION
def main():
  ''' Prints the HTML page
  '''
  print '''Content-type: text/html\r\n\r\n''',
  print(getPageAsHTML()),

def getPageAsHTML():
  ''' Constructs and returns an HTML formatted string that can be printed, and thus
      fill the webpage with content! This method also calls helper methods for
      generating the HTML for the rating form and for the CrimeScore display.
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
  ''' Builds the rating form's HTML. It goes through each category
      and adds an HTML Select form with options 0-10 for each category.
      Forms are put into a table for organizational purposes.
  '''

  categories = getCategoryList()
  outputString = '<form action="CrimeScorePage.py" method="get">'

  tableEntryIndex = 0
    # tableEntryIndex is used for dividing the table up into columns.
  outputString+= "<table style='width:100%'><tr align='center'>"
  for category in categories:
    if tableEntryIndex % 3 == 0:
      # After each third entry, end the row and start a new one:
      outputString += "</tr><tr align='center'>"

    # Add the forms:
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
  ''' Returns an HTML-ified string that is either blank
      or tells the the calculated CrimeScore.
  '''

  ratingsHash = getRatingsHashFromForm()
  cs = CrimeScore(ratingsHash)
  score = cs.calculateCrimeScore()

  if ratingsHash.keys == ["ERROR"] or len(ratingsHash) == 0:
    # If there's an error or the user hasn't filled in ratings yet,
    # there's no CrimeScore to return!
    return ""

  else: #so, if the hash table is populated
    return "<i>Your CrimeScore:</i> <b>%i</b>" % score


if __name__ == '__main__':
  main()
