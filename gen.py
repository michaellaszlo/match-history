import random
import string

num_players = 500


class IntegerUniformDistribution:

  def __init__(self, low, high):
    self.low = low
    self.high = high

  def value(self):
    return random.randrange(self.low, self.high + 1)


class NameGenerator:

  def __init__(self, seed=None):
    if seed != None:
      random.seed(seed)

  def value(self):
    parts = []
    for i in range(2):
      n = random.randrange(4, 9)
      part = ''.join(random.choice(string.ascii_lowercase) for i in range(n))
      part = part[0].upper() + part[1:]
      parts.append(part)
    return ' '.join(parts)

class Player:

  def __init__(self, name, match_participation):
    self.name = name
    self.match_participation = match_participation

  def __str__(self):
    return '[%s %d]' % (self.name, self.match_participation)


match_participation_distribution = IntegerUniformDistribution(2, 30)
name_generator = NameGenerator()

players = num_players * [ None ]
match_participation_total = 0
for i in range(num_players):
  player = Player(name_generator.value(),
      match_participation_distribution.value())
  players[i] = player
  match_participation_total += player.match_participation

weighted_players = match_participation_total * [ None ]
pos = 0
for player in players:
  for i in range(player.match_participation):
    weighted_players[pos] = player
    pos += 1

def choose_match_player():
  return random.choice(weighted_players)

a = choose_match_player()
while True:
  b = choose_match_player()
  if b != a:
    break
print(a)
print(b)
