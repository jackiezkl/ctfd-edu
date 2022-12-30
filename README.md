##CTFd for Edu

codes for checking new user and add new challenges using API

before running, login in to CTFd as admin user, go to the settings page. Then, select a future time and generate a authentication token to use the API.


# auto-scoreboard plugin
Inspired by ctfd-event-countdown from https://github.com/alokmenghrajani/ctfd-event-countdown
Altered for special needs.

The plugin shows a scoreboard, and a countdown until the start of the event and then until the end of the event. The scoreboard will also show all users' solve counts.

## Screenshot

![sample](screenshot.png)


## To use

1. Clone this repository to the same CTFd parent folder. Run the **run_first.py**
2. The program will add to the following to base template (`themes/core/templates/base.html` if you are using the default theme):
```
    <meta name="start_in" content="{{ ctf_starts_in() }}">
    <meta name="ends_in" content="{{ ctf_ends_in() }}">
```
3. It then adds `<span class="ctfd-auto-scoreboard" style="position: relative; float: right; top: 0px; right: 0px; min-width: 20%;">&nbsp;</span>` right before the line with `id=challenge-window` in `themes/core/templates/challenges.html`. Feel free to manually add on any other pages.
4. At last, it copies the **auto-scoreboard** plugin to the plugins folder
5. Set an event start or end time in Admin -> Config.
