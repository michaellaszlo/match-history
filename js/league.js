var League = (function () {
  var players,
      matches,
      containers = {};

  function setPlayers(thesePlayers) {
    players = thesePlayers;
  }

  function setMatches(theseMatches) {
    matches = theseMatches;
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
