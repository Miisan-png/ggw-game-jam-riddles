(function () {
  "use strict";

  var RIDDLES = [
    {
      id: 1,
      hint: "Found the spot? Take a good look around — the booth crew will ask you one small detail about it before the stamp is yours!",
      day: 1,
      unlock: new Date(2026, 6, 7, 0, 0, 0),
      badge: "☕",
      title: "The Island Fuel-Up",
      lines: [
        "When your stamina meter hits absolute zero,",
        "Skip Brewster's piping hot coffee blend.",
        "Where do villagers gather to sit, chat, and chew,",
        "To get a quick fuel-up and start days anew?"
      ]
    },
    {
      id: 2,
      hint: "Found the spot? Take a good look around — the booth crew will ask you one small detail about it before the stamp is yours!",
      day: 2,
      unlock: new Date(2026, 6, 8, 0, 0, 0),
      badge: "🎶",
      title: "The Saturday Night Special",
      lines: [
        "Go to the plaza where the paths all compete,",
        "Where the biggest display screen stands grand and elite.",
        "If K.K. Slider were hosting a concert tonight,",
        "He'd project his slick tunes under this massive light."
      ]
    },
    {
      id: 3,
      hint: "Found the spot? Snap a photo of yourself there (Dodo wave encouraged!), post it to your story and tag the GGW page — show us the post at the booth for your stamp!",
      day: 3,
      unlock: new Date(2026, 6, 9, 0, 0, 0),
      badge: "✈️",
      title: "Wilbur & Orville's Welcome",
      lines: [
        "Whether flying by Dodo or checking your map,",
        "This gateway is where your long journeys overlap.",
        "It's the very first acre your passport will show,",
        "Where the newcomers arrive and the travelers go."
      ]
    },
    {
      id: 4,
      hint: "No detail quiz for this one — squeezing into the giant Switch and snapping a photo IS your proof. Show it at the booth!",
      day: 3,
      unlock: new Date(2026, 6, 9, 0, 0, 0),
      badge: "📸",
      title: "Step Into the Switch",
      lines: [
        "The magic machine where our island resides,",
        "Has one blue, one red Joy-Con clipped to its sides.",
        "We built it SO big that a villager fits —",
        "Stand in the screen, say \"CHEESE!\", and that's it!"
      ]
    }
  ];

  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  function pad(n) {
    return n < 10 ? "0" + n : "" + n;
  }

  function formatDate(d) {
    return MONTHS[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear();
  }

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function buildUnlocked(riddle) {
    var card = el("article", "card unlocked");

    var day = el("span", "card-day", "Day " + riddle.day);
    card.appendChild(day);

    var head = el("div", "card-head");
    head.appendChild(el("span", "card-badge", riddle.badge));
    var headText = el("div");
    headText.appendChild(el("div", "card-sub", "Riddle " + riddle.id));
    headText.appendChild(el("div", "card-title", riddle.title));
    head.appendChild(headText);
    card.appendChild(head);

    var list = el("ul", "riddle-lines");
    riddle.lines.forEach(function (line) {
      list.appendChild(el("li", null, line));
    });
    card.appendChild(list);

    card.appendChild(el("div", "hint", riddle.hint));

    return card;
  }

  function buildLocked(riddle) {
    var card = el("article", "card locked");

    var day = el("span", "card-day", "Day " + riddle.day);
    card.appendChild(day);

    var body = el("div", "locked-body");
    body.appendChild(el("div", "lock-icon", "🔒"));
    body.appendChild(el("div", "locked-title", "Riddle " + riddle.id + " is sealed"));
    body.appendChild(el("div", "locked-date", "Unlocks " + formatDate(riddle.unlock)));

    var cd = el("div", "countdown");
    ["days", "hours", "mins", "secs"].forEach(function (key) {
      var unit = el("div", "cd-unit");
      var num = el("div", "cd-num", "--");
      num.setAttribute("data-cd", key);
      unit.appendChild(num);
      unit.appendChild(el("span", "cd-lab", key));
      cd.appendChild(unit);
    });
    body.appendChild(cd);
    card.appendChild(body);

    card._countdown = cd;
    card._target = riddle.unlock.getTime();
    return card;
  }

  var board = document.getElementById("board");
  var lockedCards = [];

  var forceUnlock = false;

  RIDDLES.forEach(function (riddle) {
    var unlocked = forceUnlock || Date.now() >= riddle.unlock.getTime();
    var card = unlocked ? buildUnlocked(riddle) : buildLocked(riddle);
    board.appendChild(card);
    if (!unlocked) lockedCards.push(card);
  });

  function tick() {
    var now = Date.now();
    var stillLocked = [];

    lockedCards.forEach(function (card) {
      var remaining = card._target - now;
      if (remaining <= 0) {
        location.reload();
        return;
      }
      var secs = Math.floor(remaining / 1000);
      var values = {
        days: Math.floor(secs / 86400),
        hours: Math.floor((secs % 86400) / 3600),
        mins: Math.floor((secs % 3600) / 60),
        secs: secs % 60
      };
      var nums = card._countdown.querySelectorAll("[data-cd]");
      for (var i = 0; i < nums.length; i++) {
        var key = nums[i].getAttribute("data-cd");
        nums[i].textContent = key === "days" ? values.days : pad(values[key]);
      }
      stillLocked.push(card);
    });

    lockedCards = stillLocked;
  }

  if (lockedCards.length) {
    tick();
    setInterval(tick, 1000);
  }
})();
