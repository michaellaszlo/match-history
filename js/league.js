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
      player.matches = [];
      player.defeated = {};
      player.defeatedBy = {};
    });
  }

  function setMatches(theseMatches) {
    matches = theseMatches;
    matches.forEach(function (match) {
      var winner = playerLookup[match.winner_id],
          loser = playerLookup[match.loser_id];
      matchLookup[match.id] = match;
      winner.matches.push(match);
      loser.matches.push(match);
    });
  }

  function load() {
    containers.wrapper = document.createElement('div');
    containers.wrapper.id = 'wrapper';
    document.body.appendChild(containers.wrapper);
    containers.players = document.createElement('div');
    containers.players.id = 'players';
    containers.wrapper.appendChild(containers.players);
    players.forEach(function (player) {
      var element = document.createElement('div');
      element.className = 'player';
      element.innerHTML = player.name;
      containers.players.appendChild(element);
    });
  }

  return {
    setPlayers: setPlayers,
    setMatches: setMatches,
    load: load
  };
})();

onload = League.load;
