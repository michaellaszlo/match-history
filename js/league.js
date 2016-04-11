var League = (function () {
  var players = [],
      playerLookup = {},
      matches = [],
      matchLookup = {},
      containers = {};

  function setPlayers(thesePlayers) {
    players = thesePlayers;
    players.forEach(function (player) {
      playerLookup[player.id] = player;
      player.history = [];
      player.wins = player.losses = 0;
    });
  }

  function setMatches(theseMatches) {
    matches = theseMatches;
    matches.forEach(function (match) {
      var winner = playerLookup[match.winner_id],
          loser = playerLookup[match.loser_id];
      matchLookup[match.id] = match;
      winner.history.push({
        result: 'W', opponent: loser, match: match
      });
      winner.wins += 1;
      loser.history.push({
        result: 'L', opponent: winner, match: match
      });
      loser.losses += 1;
    });
  }

  function make(tag, options) {
    var element = document.createElement(tag);
    [ 'id', 'className' ].forEach(function (property) {
      if (property in options) {
        element[property] = options[property];
      }
    });
    if ('parent' in options) {
      options.parent.appendChild(element);
    }
    return element;
  }

  function load() {
    containers.wrapper = make('div', { id: 'wrapper',
        parent: document.body });
    containers.players = make('div', { id: 'players',
        parent: containers.wrapper });
    containers.spotlight = make('div', { id: 'spotlight',
        parent: containers.wrapper });
    console.log(containers.spotlight);
    players.sort(function (a, b) {
      if (a.name < b.name) {
        return -1;
      } else if (a.name == b.name) {
        return 0;
      }
      return 1;
    });
    players.forEach(function (player) {
      var container = document.createElement('div');
      container.className = 'player';
      container.innerHTML = player.name + ' ' +
          player.wins + '-' + player.losses + '<br>';
      player.history.forEach(function (record) {
        container.innerHTML += record.result + ' ' + record.opponent.name +
            '<br>';
      });
      containers.players.appendChild(container);
    });
  }

  return {
    setPlayers: setPlayers,
    setMatches: setMatches,
    load: load
  };
})();

onload = League.load;
