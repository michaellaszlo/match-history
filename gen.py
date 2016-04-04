import random
import string

num_players = 5
num_matches = 30


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

  def __init__(self, name, match_participation, skill_level):
    self.name = name
    self.match_participation = match_participation
    self.skill_level = skill_level
    self.matches = []
    self.defeated = {}
    self.defeated_by = {}

  def __str__(self):
    return '[%s %d]' % (self.name, self.match_participation)


class Match:

  def __init__(self, winner, loser):
    self.winner = winner
    self.loser = loser


def decide_outcome(a, b):
  if random.randrange(a.skill_level + b.skill_level) < a.skill_level:
    return a, b
  return b, a

match_participation_distribution = IntegerUniformDistribution(2, 30)
skill_level_distribution = IntegerUniformDistribution(5, 10)
name_generator = NameGenerator()

players = num_players * [ None ]
match_participation_total = 0
for i in range(num_players):
  player = Player(name_generator.value(),
      match_participation_distribution.value(),
      skill_level_distribution.value())
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

for i in range(num_matches):
  a = choose_match_player()
  while True:
    b = choose_match_player()
    if b != a:
      break
  a, b = sorted([a, b], key=lambda player: player.name)
  winner, loser = decide_outcome(a, b)
  print('%s defeats %s' % (winner.name, loser.name))
  match = Match(winner, loser)
  for player in [winner, loser]:
    player.matches.append(match)
  winner.defeated.setdefault(loser, []).append(match)
  loser.defeated_by.setdefault(winner, []).append(match)
