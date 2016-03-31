import random

num_players = 500


class IntegerUniformDistribution:

  def __init__(self, low, high):
    self.low = low
    self.high = high

  def value(self):
    return random.randrange(low, high + 1)

class Player:

  def __init__(self, match_participation):
    self.match_participation = match_participation

match_participation_distribution = IntegerUniformDistribution(2, 30)
players = [ Player() for i in range(num_players) ]

