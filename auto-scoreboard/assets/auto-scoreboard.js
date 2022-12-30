Skip to content
Search or jump to…
Pull requests
Issues
Codespaces
Marketplace
Explore
 
@jackiezkl 
simewu
/
cwssp
Public
forked from CTFd/CTFd
Code
Pull requests
Actions
Projects
Security
Insights
cwssp/CTFd-3.4.0/CTFd/plugins/ctfd-auto-scoreboard/assets/auto-scoreboard.js /
@simewu
simewu Fix scoreboard undefined behavior
Latest commit 8dec770 on Dec 2, 2021
 History
 1 contributor
294 lines (265 sloc)  16 KB

(() => {
  var now = Date.now();

  var f = ((seconds, prefix) => {
    if (seconds <= 0) {
      return 'Event ended, thank you for playing!';
    }
    var days = (seconds / 86400)|0;
    var hours = ((seconds % 86400) / 3600)|0;
    var minutes = ((seconds % 3600) / 60)|0;
    var seconds = seconds % 60;

    if (days > 0) {
      return prefix + days + ' day' + (days > 1 ? 's' : '') +
          ', ' + hours + ' hour' + (hours > 1 ? 's' : '');
    } else if (hours > 0) {
      return prefix + hours + ' hour' + (hours > 1 ? 's' : '') +
          ', ' + minutes + ' minute' + (minutes > 1 ? 's' : '');
    } else if (minutes > 0) {
      return prefix + minutes + ' minute' + (minutes > 1 ? 's' : '') +
          ', ' + seconds + ' second' + (seconds > 1 ? 's' : '');
    } else {
      return prefix + seconds + ' second' + (seconds > 1 ? 's' : '');
    }
  });

  // Cybersecurity Lab
  let challengesList = { // ID: [Name, Value, Category]
    2: ['Incident Response Actions', '60', 'Design'],
    5: ['Our Program Name', '10', 'Investigation'],
    9: ['Program Review', '20', 'Testing and Evaluation'],
    12: ['Flag in a Flag System', '70', 'Analysis'],
    16: ['We are being attacked!', '42', 'Analysis'],
    18: ['Hope it\'s not a Backdoor', '25', 'Analysis'],
    19: ['Further Attack 1', '40', 'Analysis'],
    20: ['Further Attack 2', '40', 'Analysis'],
    21: ['A File Was Stolen', '45', 'Analysis'],
    23: ['Encoded Message', '25', 'Analysis'],
    24: ['Mystery JavaScript 2', '55', 'Testing and Evaluation'],
    26: ['Hardware Encryption', '60', 'Implementation'],
    29: ['Determining User Inputs', '60', 'Implementation'],
    30: ['Prisoner\'s Dilemma', '90', 'Design'],
    32: ['Cryptocurrency Audit', '70', 'Analysis'],
    33: ['Mystery JavaScript 1', '50', 'Testing and Evaluation'],
    34: ['Steganography 1', '40', 'Analysis'],
    35: ['Name the Attack 1', '23', 'Investigation'],
    36: ['Name the Attack 2', '24', 'Investigation'],
    37: ['Name the Attack 3', '24', 'Investigation'],
    38: ['Name the Attack 4', '26', 'Investigation'],
    39: ['Name the Attack 5', '26', 'Investigation'],
    40: ['Name the Attack 6', '26', 'Investigation'],
    41: ['Name the Attack 7', '26', 'Investigation'],
    42: ['Name this Software 1', '24', 'Investigation'],
    43: ['Name this Software 2', '24', 'Investigation'],
    44: ['Name this Software 3', '24', 'Investigation'],
    45: ['Name this Software 4', '24', 'Investigation'],
    46: ['Name this Software 5', '24', 'Investigation'],
    47: ['Name this Software 6', '26', 'Investigation'],
    48: ['Name this Software 7', '24', 'Investigation'],
    49: ['Incident Response Ordering', '50', 'Design'],
    50: ['Risk Management ROI', '10', 'Analysis'],
    51: ['If you know, you know', '28', 'Testing and Evaluation'],
    52: ['Lightning Show', '70', 'Analysis'],
    53: ['Read The Story Scenario', '5', 'Introduction'],
    54: ['Regular Expressions 1', '30', 'Testing and Evaluation'],
    55: ['Regular Expressions 2', '33', 'Testing and Evaluation'],
    56: ['Breakout Room 1', '60', 'Coordination'],
    57: ['Breakout Room 2', '60', 'Coordination'],
    58: ['Coordination XOR 1', '34', 'Coordination'],
    59: ['Coordination XOR 2', '34', 'Coordination'],
    60: ['Coordination XOR 3', '34', 'Coordination'],
    61: ['Coordination XOR 4', '34', 'Coordination'],
    62: ['Coordination XOR 5', '34', 'Coordination'],
    63: ['Reverse Image Search', '100', 'Investigation'],
    64: ['Coordination XOR 6', '34', 'Coordination'],
    65: ['Coordination XOR 7', '34', 'Coordination'],
    66: ['Coordination XOR 8', '34', 'Coordination'],
    67: ['Linux Basics 1', '20', 'Implementation'],
    68: ['Linux Basics 2', '20', 'Implementation'],
    69: ['Linux Basics 3', '20', 'Implementation'],
    70: ['Linux Basics 4', '20', 'Implementation'],
    71: ['Linux Basics 5', '20', 'Implementation'],
    73: ['Linux Basics 6', '35', 'Implementation'],
    74: ['Linux Basics 7', '21', 'Implementation'],
    75: ['Simple Testing Server', '26', 'Testing and Evaluation'],
    76: ['Linux Basics 8', '21', 'Implementation'],
    77: ['Windows Basics 1', '20', 'Implementation'],
    78: ['Windows Basics 2', '21', 'Implementation'],
    79: ['Windows Basics 3', '21', 'Implementation'],
    80: ['Windows Basics 4', '21', 'Implementation'],
    81: ['Windows Basics 5', '21', 'Implementation'],
    82: ['Firewall 1', '26', 'Design'],
    83: ['Firewall 2', '26', 'Design'],
    84: ['Windows Basics 6', '21', 'Implementation'],
    85: ['Windows Basics 7', '21', 'Implementation'],
    87: ['Windows Basics 8', '35', 'Implementation'],
    88: ['Draw Your Favorite Animal', '50', 'Design'],
    89: ['Firewall 3', '26', 'Design'],
    90: ['Remove the Hacker', '60', 'Design'],
    91: ['Firewall 4', '25', 'Design'],
    92: ['Firewall 5', '24', 'Testing and Evaluation'],
    93: ['Historical Event', '45', 'Investigation'],
    94: ['Networking 1', '24', 'Testing and Evaluation'],
    95: ['Linux Basics 9', '24', 'Testing and Evaluation'],
    96: ['Vulnerability Test 1', '22', 'Implementation'],
    97: ['Vulnerability Test 2', '24', 'Testing and Evaluation'],
    98: ['Vulnerability Test 3', '24', 'Testing and Evaluation'],
    99: ['Vulnerability Test 4', '24', 'Testing and Evaluation'],
    101: ['Networking 2', '24', 'Testing and Evaluation'],
    102: ['Vulnerability Test 5', '23', 'Analysis'],
    103: ['Draw a Lock', '40', 'Design'],
    104: ['Introduction', '5', 'Introduction'],
    105: ['System Development Life Cycle', '22', 'Design'],
    106: ['Steganography 2', '25', 'Design'],
    107: ['Regular Expressions 3', '40', 'Testing and Evaluation'],
    108: ['Regular Expressions 4', '50', 'Testing and Evaluation'],
    109: ['Preliminary Information 1', '5', 'Introduction'],
    110: ['Preliminary Information 2', '5', 'Introduction'],
    112: ['Coordination using Zoom Chat', '8', 'Coordination'],
    113: ['Birthday Month 1', '50', 'Coordination'],
    114: ['Birthday Month 2', '50', 'Coordination']
  }
  
  var getUserSolvesHistogram = function(user) {
    let numSolves = 0;
    let categoryHistogram = {'Investigation': 0, 'Design': 0, 'Analysis': 0, 'Implementation': 0, 'Testing and Evaluation': 0, 'Coordination': 0};
    for(let solve of user.solves) {
      let indexedItem = challengesList[solve.challenge_id];
      if(indexedItem === undefined) {
        //console.log('Cannot find challenge "' + solve.challenge_id + '", skipping.');
        continue;
      }
      if(categoryHistogram[indexedItem[2]] === undefined) {
        // Ignore all other categories that are not predefined (like Introduction)
        // categoryHistogram[indexedItem[2]] = 1;
      } else {
        categoryHistogram[indexedItem[2]] += 1;
        numSolves += 1;
      }
    }
    return {numSolves: numSolves, categoryHistogram: categoryHistogram};
  }

  var scoreboard = {
    //id: {name: '', rank: 0, numSolves: 0, score: 0, categoriesSolves: '0 / 0', bonuses: 0}
  };
  var scoreboard_toggle = false;

  var scoreboardPromiseResolver = function(element, countdown, show_scoreboard, scoreboardPromise) {
    if(scoreboardPromise.inspect().state == 'fulfilled') {
      var wrapper_start = '';
      var wrapper_scoreboard = '';
      var wrapper_end = '';

      if(show_scoreboard) {
        var response = scoreboardPromise.valueOf().data;
        var response_keys = Object.keys(response);

        wrapper_scoreboard += '<div class="toast-body">';
        wrapper_scoreboard += '<table class="table table-sm table-striped"><thead><tr>';
        wrapper_scoreboard += '<td scope="col"><b>User<br>Name</b></td>';
        wrapper_scoreboard += '<td scope="col"><b>Roles /<br>Categories</b></td>';
        wrapper_scoreboard += '<td scope="col"><b>Current<br>Score</b></td>';
        wrapper_scoreboard += '</tr></thead>';

        if(scoreboard_toggle) {
          // Only fill in the score
          for(var key of response_keys) {
            var id = response[key].account_id;
            var name = response[key].name;
            var score = response[key].score;

            if(score === undefined) continue;

            if(scoreboard[id] === undefined) {
              scoreboard[id] = {name: name, rank: 0, numSolves: 0, score: 0, bonus: 0, categoriesSolvedIn: '0 / 0'}
            }
            scoreboard[id].score = score;
          }

        } else {
          // SET IT TO THE ID

          // Fill in everything but the score
          for(var key of response_keys) {
            var user = response[key];
            var id = user.id;

            if(scoreboard[id] === undefined || scoreboard[id].name != user.name) {
              scoreboard[id] = {name: user.name, rank: 0, numSolves: 0, score: 0, bonus: 0, categoriesSolvedIn: '0 / 0'}
            }

            scoreboard[id].rank = key;
            var computedData = getUserSolvesHistogram(user);
            var categoriesSolvedIn = 0;
            for(var category in computedData.categoryHistogram) {
              if(computedData.categoryHistogram[category] > 0) categoriesSolvedIn += 1;
            }
            scoreboard[id].numSolves = computedData.numSolves;
            scoreboard[id].categoriesSolvedIn = categoriesSolvedIn + ' / 6';

            var bonus = 0;
            //if(CTFd.user.id == 1) {
            if(categoriesSolvedIn >= 6) {
              bonus += 200;
            } else if(categoriesSolvedIn >= 5) {
              bonus += 100;
            } else if(categoriesSolvedIn >= 4) {
              bonus += 50;
            }
            //}
            scoreboard[id].bonus = bonus;
          }
        }

        // Sort the users by rank, then list them
        var sorted = Object.values(scoreboard);
        sorted.sort((a, b) => {
          //return (b.score > a.score) - (b.score < a.score);
          return ((b.score + b.bonus) > (a.score + a.bonus)) - ((b.score + b.bonus) < (a.score + a.bonus));
        });

        for(var val of sorted) {
          if(val.score + val.bonus === undefined) continue;
          if(val.categoriesSolvedIn == '0 / 0') continue;
          wrapper_scoreboard += '<tr>';
          wrapper_scoreboard += '<td scope="col">' + val.name + '</td>';
          wrapper_scoreboard += '<td scope="col">' + val.categoriesSolvedIn + '</td>';
          if(val.bonus == 0) wrapper_scoreboard += '<td scope="col">' + val.score + '</td>';
          else {
            var color = val.bonus >= 200 ? 'primary' : (val.bonus >= 100 ? 'info' : 'dark');
            wrapper_scoreboard += '<td scope="col" title="Total score = ' + (val.score + val.bonus) + '">' + val.score + '<span class="badge badge-' + color + ' ml-2"> + ' + val.bonus + '</span></td>';
          }


          wrapper_scoreboard += '</tr>';
        }
        wrapper_scoreboard += '</div>';
      }

      wrapper_start += '<div id="scoreboard"><div class="toast m-3 fade show" role="alert"><div class="toast-header"><strong class="mr-auto lead">';
      wrapper_end += '</strong><p class="ctfd-event-countdown">&nbsp;</p></div>'
      wrapper_end += wrapper_scoreboard;
      wrapper_end += '</div></div>';
      
      element.innerHTML = wrapper_start + countdown + wrapper_end;
    } else {
      setTimeout(scoreboardPromiseResolver, 100, element, countdown, show_scoreboard, scoreboardPromise);
    }
  }

  var g = ((element, countdown, show_scoreboard) => {
    var scoreboardPromise;
    if(scoreboard_toggle) {
      scoreboardPromise = CTFd.api.get_scoreboard_detail({count: 1000000000});
      scoreboard_toggle = false;
    } else {
      scoreboardPromise = CTFd.api.get_scoreboard_list({count: 1000000000});
      scoreboard_toggle = true;
    }
    setTimeout(scoreboardPromiseResolver, 100, element, countdown, show_scoreboard, scoreboardPromise);
  });

  function update_auto_scoreboard() {
    var elapsed = ((Date.now() - now) / 1000)|0;
    var elements = document.getElementsByClassName('ctfd-auto-scoreboard');
    for (var i=0; i<elements.length; i++) {
      var element = elements[i];
      var seconds = document.getElementsByName("start_in")[0].content - elapsed;
      if (seconds > 0) {
        g(element, f(seconds, "Event starts in "), false);
      } else {
        seconds = document.getElementsByName("ends_in")[0].content - elapsed;
        g(element, f(seconds, "Time left: "), true);
      }
      if(seconds <= 0) {
        if(document.getElementById('firework-overlay') == null) {
          // Fireworks
          var SCREEN_WIDTH = window.innerWidth,
              SCREEN_HEIGHT = window.innerHeight,
              mousePos = {
                  x: 400,
                  y: 300
              },
              canvas = document.createElement("canvas"),
              context = canvas.getContext("2d"),
              particles = [],
              rockets = [],
              MAX_PARTICLES = 400,
              colorCode = 0;

          function begin_fireworks() {
              document.body.appendChild(canvas), canvas.id = "firework-overlay", canvas.width = SCREEN_WIDTH, canvas.height = SCREEN_HEIGHT, canvas.style.position = "fixed", canvas.style.top = "0", canvas.style.left = "0", canvas.style.pointerEvents = "none", setInterval(launch, 800), setInterval(loop, 20)
          }

          function launch() {
              launchFrom(mousePos.x)
          }

          function launchFrom(t) {
              if (rockets.length < 10) {
                  var e = new Rocket(t);
                  e.explosionColor = 10 * Math.floor(360 * Math.random() / 10), e.vel.y = -6 * Math.random() - 9, e.vel.x = 6 * Math.random() - 3, e.size = 15, e.shrink = .999, e.gravity = .1, rockets.push(e)
              }
          }

          function loop() {
              SCREEN_WIDTH != window.innerWidth && (canvas.width = SCREEN_WIDTH = window.innerWidth), SCREEN_HEIGHT != window.innerHeight && (canvas.height = SCREEN_HEIGHT = window.innerHeight), context.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
              for (var t = [], e = 0; e < rockets.length; e++) {
                  rockets[e].update(), rockets[e].render(context);
                  var o = Math.sqrt(Math.pow(mousePos.x - rockets[e].pos.x, 2) + Math.pow(mousePos.y - rockets[e].pos.y, 2)),
                      s = rockets[e].pos.y < 2 * SCREEN_HEIGHT / 3 && 100 * Math.random() <= 1;
                  rockets[e].pos.y < SCREEN_HEIGHT / 5 || rockets[e].vel.y >= 0 || o < 50 || s ? rockets[e].explode() : t.push(rockets[e])
              }
              rockets = t;
              var i = [];
              for (e = 0; e < particles.length; e++) particles[e].update(), particles[e].exists() && (particles[e].render(context), i.push(particles[e]));
              for (particles = i; particles.length > MAX_PARTICLES;) particles.shift()
          }

          function Particle(t) {
              this.pos = {
                  x: t ? t.x : 0,
                  y: t ? t.y : 0
              }, this.vel = {
                  x: 0,
                  y: 0
              }, this.shrink = .97, this.size = 2, this.resistance = 1, this.gravity = 0, this.flick = !1, this.alpha = 1, this.fade = 0, this.color = 0
          }

          function Rocket(t) {
              Particle.apply(this, [{
                  x: t,
                  y: SCREEN_HEIGHT
              }]), this.explosionColor = 0
          }
          $(document).mousemove(function(t) {
              t.preventDefault(), mousePos = {
                  x: t.clientX,
                  y: t.clientY
              }
          }), $(document).mousedown(function(t) {
              for (var e = 0; e < 5; e++) launchFrom(Math.random() * SCREEN_WIDTH * 2 / 3 + SCREEN_WIDTH / 6)
          }), Particle.prototype.update = function() {
              this.vel.x *= this.resistance, this.vel.y *= this.resistance, this.vel.y += this.gravity, this.pos.x += this.vel.x, this.pos.y += this.vel.y, this.size *= this.shrink, this.alpha -= this.fade
          }, Particle.prototype.render = function(t) {
              if (this.exists()) {
                  t.save(), t.globalCompositeOperation = "lighter";
                  var e = this.pos.x,
                      o = this.pos.y,
                      s = this.size / 2,
                      i = t.createRadialGradient(e, o, .1, e, o, s);
                  i.addColorStop(.1, "rgba(0,0,0," + this.alpha + ")"), i.addColorStop(.8, "hsla(" + this.color + ", 100%, 50%, " + this.alpha + ")"), i.addColorStop(1, "hsla(" + this.color + ", 100%, 50%, 0.1)"), t.fillStyle = i, t.beginPath(), t.arc(this.pos.x, this.pos.y, this.flick ? Math.random() * this.size : this.size, 0, 2 * Math.PI, !0), t.closePath(), t.fill(), t.restore()
              }
          }, Particle.prototype.exists = function() {
              return this.alpha >= .1 && this.size >= 1
          }, Rocket.prototype = new Particle, Rocket.prototype.constructor = Rocket, Rocket.prototype.explode = function() {
              for (var t = 10 * Math.random() + 80, e = 0; e < t; e++) {
                  var o = new Particle(this.pos),
                      s = Math.random() * Math.PI * 2,
                      i = 25 * Math.cos(Math.random() * Math.PI / 2);
                  o.vel.x = Math.cos(s) * i, o.vel.y = Math.sin(s) * i, o.size = 10, o.gravity = .2, o.resistance = .92, o.shrink = .05 * Math.random() + .93, o.flick = !0, o.color = this.explosionColor, particles.push(o)
              }
          }, Rocket.prototype.render = function(t) {
              if (this.exists()) {
                  t.save(), t.globalCompositeOperation = "lighter";
                  var e = this.pos.x,
                      o = this.pos.y,
                      s = this.size / 2,
                      i = t.createRadialGradient(e, o, .1, e, o, s);
                  i.addColorStop(.1, "rgba(0, 0, 0 ," + this.alpha + ")"), i.addColorStop(1, "rgba(0, 0, 0, 0)"), t.fillStyle = i, t.beginPath(), t.arc(this.pos.x, this.pos.y, this.flick ? Math.random() * this.size / 2 + this.size / 2 : this.size, 0, 2 * Math.PI, !0), t.closePath(), t.fill(), t.restore()
              }
          };
          begin_fireworks();
        }
      }
    }
  }

  setInterval(update_auto_scoreboard, 10000);
  
  setTimeout(update_auto_scoreboard(), 100);
  setTimeout(update_auto_scoreboard(), 500);
  setTimeout(update_auto_scoreboard(), 1000);


})()
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
cwssp/auto-scoreboard.js at master · simewu/cwssp
