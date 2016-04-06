import random
import string
import json

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

  def __init__(self, name, eagerness, skill):
    self.name = name
    self.eagerness = eagerness
    self.skill = skill
    self.matches = []
    self.defeated = {}
    self.defeated_by = {}

  def __str__(self):
    return '%s, eagerness %d, skill %d' % (self.name, self.eagerness,
        self.skill)

  def dictionary(self):
    d = {}
    d['name'] = self.name
    d['defeated'] = {}
    for opponent, matches in self.defeated.items():
      d['defeated'][opponent.name] = [ str(match) for match in matches ]
    d['defeated_by'] = {}
    for opponent, matches in self.defeated_by.items():
      d['defeated'][opponent.name] = [ str(match) for match in matches ]
    return d


class Match:

  def __init__(self, winner, loser):
    self.winner = winner
    self.loser = loser

  def __str__(self):
    return '%s defeats %s' % (self.winner.name, self.loser.name)


def decide_outcome(a, b):
  if random.randrange(a.skill + b.skill) < a.skill:
    return a, b
  return b, a

eagerness_distribution = IntegerUniformDistribution(2, 30)
skill_distribution = IntegerUniformDistribution(5, 25)
name_generator = NameGenerator()

players = num_players * [ None ]
eagerness_total = 0
for i in range(num_players):
  player = Player(name_generator.value(),
      eagerness_distribution.value(),
      skill_distribution.value())
  players[i] = player
  eagerness_total += player.eagerness

weighted_players = eagerness_total * [ None ]
pos = 0
for player in players:
  for i in range(player.eagerness):
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
  match = Match(winner, loser)
  for player in [winner, loser]:
    player.matches.append(match)
  winner.defeated.setdefault(loser, []).append(match)
  loser.defeated_by.setdefault(winner, []).append(match)

for player in sorted(players, key=lambda player: -player.skill):
  print(str(player))
  print('  defeated:')
  for opponent, matches in player.defeated.items():
    print('    %d times: %s' % (len(matches), opponent.name))
  print('  defeated by:')
  for opponent, matches in player.defeated_by.items():
    print('    %d times: %s' % (len(matches), opponent.name))
  print(json.dumps(player.dictionary()))
  print('')
