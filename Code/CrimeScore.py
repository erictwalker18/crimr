import random # FOR TESTING PURPOSES!! REMOVE!!

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

  def getTotalPoints(self):
    ''' Determines the total points that
        the user weighed stuff with.
    '''
    values = self.ratingsHash.values()
    sum = 0
    for value in values:
      sum += int(value)
      # The keys must be numbers!
    return sum

  def getWeightForCategory(self, category):
    ''' Returns a float of the percent weight
        for the category (calculated by taking
        the 'rating points' given to the category
        divided by the total points given).
    '''
    if category not in self.ratingsHash or int(self.ratingsHash[category]) == 0:
      # The category has no weight if it wasn't given any points, so return 0.
      return 0.0
    else:
      categoryPoints = int(self.ratingsHash[category])
      totalPoints = self.getTotalPoints()

      return categoryPoints/float(totalPoints)

  def calculateCrimeScore(self):
    ''' Calculates the crime score by multiplying
        the category ratings by their weights.
    '''
    score = 0
    categories = self.ratingsHash.keys()

    for category in categories:
      weightedCategoryScore = 0
      if category in self.ratingsHash:
        weight = self.getWeightForCategory(category)
        # numberOfCrimesInCategory = CrimeDataFetcher.numberOfCrimesInCategory(category)
            # IMPLEMENT THAT ^^^
        '''this is super temporary, FOR TESTING ONLY!!::'''
        numberOfCrimesInCategory = random.choice([20,30,40,50,70]) # for now.

        weightedCategoryScore = weight * numberOfCrimesInCategory

      score += weightedCategoryScore

    # CrimeScores have no time for decimals!:
    return int(round(score))
