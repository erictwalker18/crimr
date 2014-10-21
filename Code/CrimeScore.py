from CrimeDataFetcher import CrimeDataFetcher

class CrimeScore:
  ''' The class that calculates CrimeScore values
      and other appropriate information about the
      user's rating of categories of crime.
  '''
  def __init__(self, ratingsHash):
    self.ratingsHash = ratingsHash
      # ratingsHash will be a hash table with
      # categories for keys and ratings (0-10) for
      # values.

  def getScoreForCategory(self, category):
    ''' Returns a float of the percent weight
        for the category (calculated by taking
        the 'rating points' given to the category
        divided by the total points given).
    '''
    if category not in self.ratingsHash:
      return 0
    else:
      return int(self.ratingsHash[category])

  def getTotalCrimesInDatabase(self):
    '''Returns the total number of crimes (for all categories)'''
    total = 0
    fetcher = CrimeDataFetcher()
    for category in self.ratingsHash.keys():
      total += fetcher.getNumberOfCrimesInCategory(category)

    return total

  def calculateCrimeScore(self):
    ''' Calculates the crime score by multiplying
        the category ratings by their user-given scores to obtain
        a 'weighted' numerator. This number is normalized
        by dividing by the total number of crimes in the
        dataset multiplied by the highest possible amount of points (10)
        to make the CrimeScore between 1 and 100.
    '''
    numerator = 0
    categories = self.ratingsHash.keys()
    totalCrimes = self.getTotalCrimesInDatabase()

    for category in categories:
      # weightedCategoryScore = 0
      if category in self.ratingsHash:
        categoryScore = self.getScoreForCategory(category)

        fetcher = CrimeDataFetcher()
        numberOfCrimesInCategory = fetcher.getNumberOfCrimesInCategory(category)

        weightedCategoryScore = categoryScore * numberOfCrimesInCategory

      numerator += weightedCategoryScore

    quotient = float(numerator)/(totalCrimes * 10)

    # Multiply by 100 and round to remove the decimal:
    return round(quotient*100)

  def getScoreCommentary(self, score = None):
    '''Return a string comment characterizing the CrimeScore.
    The score parameter is optional; use it to get a message for
    a certain score, or leave it out and get the message for the
    CrimeScore class's current score calculation.'''

    if score == None:
      score = self.calculateCrimeScore()
    else: score = int(score)

    if score < 10:
      return "Either nothing scares you, or there's not much crime out there. Either way, you should feel pretty comfortable."
    elif score < 20:
      return "Things are pretty tame. Go ahead and walk the dog, but look behind you every now and then."
    elif score < 40:
      return "Be a bit cautious, but don't worry too much."
    elif score < 60:
      return "Be careful out there. Crime may be afoot."
    elif score < 80:
      return "Might want to take a raincheck. Let things die down a bit, you know?"
    elif score < 100:
      return "Things are not safe, by your standards. Stay inside, stay safe."
    elif score == 100:
      return "RED ALERT! Lock your doors and windows!!"

    return ""
