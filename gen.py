import sys
import random
import string
import json

num_players = 50
num_matches = 3000


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

  def random_letter(self):
    if random.randrange(3) == 0:
      return random.choice('aeiou')
    else:
      return random.choice('bcdfghjklmnpqrstvwxyz')

  def value(self):
    parts = []
    for i in range(2):
      n = random.randrange(4, 9)
      part = ''.join(self.random_letter() for i in range(n))
      part = part[0].upper() + part[1:]
      parts.append(part)
    return ' '.join(parts)

player_lookup = {}

class Player:

  def __init__(self, id, name, eagerness, skill):
    self.id = id
    player_lookup[id] = self
    self.name = name
    self.eagerness = eagerness
    self.skill = skill
    self.matches = []
    self.defeated = {}
    self.defeated_by = {}

  def __str__(self):
    return '%s, eagerness %d, skill %d' % (self.name, self.eagerness,
        self.skill)

  def to_dict(self):
    return {
        'id': self.id,
        'name': self.name
    }


class Match:

  def __init__(self, id, winner_id, loser_id):
    self.id = id
    self.winner_id = winner_id
    self.loser_id = loser_id

  def __str__(self):
    winner = player_lookup[self.winner_id]
    loser = player_lookup[self.loser_id]
    return '%d, %d, %s defeats %s' % (id, winner.name, loser.name)
 
  def to_dict(self):
    return {
        'id': self.id,
        'winner_id': self.winner_id,
        'loser_id': self.loser_id
    }


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
  player = Player(i + 1,
      name_generator.value(),
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

matches = num_matches * [ None ]
for i in range(num_matches):
  a = choose_match_player()
  while True:
    b = choose_match_player()
    if b != a:
      break
  a, b = sorted([a, b], key=lambda player: player.name)
  winner, loser = decide_outcome(a, b)
  match_id = i + 1 
  match = Match(match_id, winner.id, loser.id)
  matches[i] = match
  for player in [winner, loser]:
    player.matches.append(match)
  winner.defeated.setdefault(loser, []).append(match)
  loser.defeated_by.setdefault(winner, []).append(match)

if False:
  for player in players:
    print(str(player))
    print('  defeated:')
    for opponent, matches in player.defeated.items():
      print('    %d times: %s' % (len(matches), opponent.name))
    print('  defeated by:')
    for opponent, matches in player.defeated_by.items():
      print('    %d times: %s' % (len(matches), opponent.name))
    print('')
else:
  #with sys.stdout as out_file:
  with open('js/data.js', 'w') as out_file:
    out_file.write('League.setPlayers(%s);\n' % json.dumps(
        [ player.to_dict() for player in players ],
        sort_keys=False, indent=2))
    out_file.write('League.setMatches(%s);\n' % json.dumps(
        [ match.to_dict() for match in matches ],
        sort_keys=False, indent=2))

