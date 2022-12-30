# ctfd-auto-scoreboard
Inspired by ctfd-event-countdown from https://github.com/alokmenghrajani/ctfd-event-countdown

Plugin for CTFd which shows a scoreboard, and a countdown until the start of the event and then until the end of the event.

## Screenshot

![sample]()


## Install

1. Clone this repository to your CTFd installation under `CTFd/plugins/`.
2. Add to your base template (`themes/core/templates/base.html` if you are using the default theme):
```
    <meta name="start_in" content="{{ ctf_starts_in() }}">
    <meta name="ends_in" content="{{ ctf_ends_in() }}">
```
3. Add `<span class="ctfd-auto-scoreboard" style="position: relative; float: right; top: 0px; right: 0px; min-width: 20%;">&nbsp;</span>` right before the line with `id=challenge-window` in `themes/core/templates/challenges.html` and/or on any other pages.
4. Set an event start or end time in Admin -> Config.
