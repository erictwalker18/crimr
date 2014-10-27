#!/usr/bin/python

'''
    CRIMR

    CrimeScorePage.py (phase_3)

    Charlie Imhoff,
    Graham Earley,
    Eric Walker
'''
'''
  CRIMR | CrimeScore

  This program generates the HTML output for the
  CrimeScore page. It calls on CrimeDataFetcher.py
  and CrimeScore.py in order to get the information
  required to tell the user their CrimeScore.

'''

import cgi
# import cgitb
# cgitb.enable()

from CrimeDataFetcher import CrimeDataFetcher
from CrimeScore import CrimeScore
from CrimrHTMLBuilder import CrimrHTMLBuilder

# UTILITY METHODS:
def getCategoryList():
  ''' Returns a list of the categories of crime
      (using CrimeDataFetcher to query the database)
  '''
  fetcher = CrimeDataFetcher()
  categories = fetcher.getListOfCategories()
  return categories

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

        # Just in case int() raises an error, though (like if the user
        # tries to sneak a string into the URL):
        except Exception, e:
          parameters[category] = 0

  except Exception, e:
    # If there's an error with the form, the dictionary will
    # return with a key and value of zero.
    parameters = {"ERROR":0}

  return parameters


# PAGE CONSTRUCTION
def main():
  ''' Prints the HTML page (using the CrimrHTMLBuilder where applicable)
  '''
  print CrimrHTMLBuilder.getStartingSequence()
  print(getPageAsHTML())

def getPageAsHTML():
  ''' Constructs and returns an HTML formatted string that can be printed, and thus
      fill the webpage with content! This method also calls helper methods for
      generating the HTML for the rating form and for the CrimeScore display.
  '''

  page = CrimrHTMLBuilder.getTopOfHTML("CrimeScore")
  page += CrimrHTMLBuilder.getTopOfBody("CrimeScore")
  page += '''
      <!-- CrimeScore presentation/readout:-->
      %s

      <h3> Rate the crimes that scare you!</h3>
      <p>For each crime-category below, consider how scary those types of crimes are to you.</p>
      <i>(0 = not scary, 10 = horrifying)</i></br>
      <a href="readme.html"><i>Read the methodology section of our README for more information about this calculation.</i></a>
      </br>
      </br>

      <!-- Crime rating form:-->
      %s
    ''' % (getCrimeScoreHTMLReadOut(), getFormHTML())
  page += CrimrHTMLBuilder.getClosingHTML()

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
  outputString+= '<table style="width:100%"><tr align="center">'
  for category in categories:
    if tableEntryIndex % 3 == 0:
      # After each third entry, end the row and start a new one:
      outputString += '</tr><tr align="center">'

    # Add the forms:
    outputString += '<td>'
    outputString += '<p>%s: </p>' % category
    outputString += '<select name="%s" id=%s>' % (category, category)
    for num in range(0,CrimeScore.MAX_SCORE + 1):
      outputString+= '<option value="%s">%i</option>' % (str(num), num)
    #Setting the default value to 2 for everything!!!
    outputString = outputString.replace('<option value="2"', '<option selected="selected" value="2"')
    outputString += '</select>'
    outputString += '</td>'

    tableEntryIndex += 1

  outputString += '</tr>' # Close off the last table row.
  outputString += '</table>'

  outputString += '<div style="text-align:center">'
  outputString += '<p><input type="submit" value="Calculate CrimeScore" /></p>'
  outputString += '</div>'
  outputString += '</form>'

  return outputString

def getCrimeScore():
  ''' Returns the calculated CrimeScore.'''

  ratingsHash = getRatingsHashFromForm()
  cs = CrimeScore(ratingsHash)
  score = cs.calculateCrimeScore()
  commentary = cs.getScoreCommentary()

  if ratingsHash.keys == ["ERROR"] or len(ratingsHash) == 0:
    # If there's an error or the user hasn't filled in ratings yet,
    # there's no CrimeScore to return!
    return ""

  else: #so, if the hash table is populated
    return score

def getCrimeScoreCommentary():
  '''Returns the CrimeScore's associated commentary.'''
  ratingsHash = getRatingsHashFromForm()
  cs = CrimeScore(ratingsHash)
  return cs.getScoreCommentary()

def getCrimeScoreHTMLReadOut():
  '''Returns the HTML that presents the calculated CrimeScore.'''
  ratingsHash = getRatingsHashFromForm()

  if ratingsHash.keys == ["ERROR"] or len(ratingsHash) == 0:
    # If there's an error or the user hasn't filled in ratings yet,
    # there's no CrimeScore info to return!
    return ""

  else: #so, the user has rated the crimes
    score = getCrimeScore()
    commentary = getCrimeScoreCommentary()

    outputString = "<div id='crimeScore'>"
    outputString += "<h2 id='crimescore-head'>Your Personalized CrimeScore:</h2>"
    outputString += "<h1 id='crimescore'>%i</h1>" % score
    outputString += "<h6>(scores range from 0 to 100)</h6>"
    outputString += "<p>%s</p>" % commentary
    outputString += "<hr>"
    outputString += "</div>"


    return outputString


if __name__ == '__main__':
  main()
