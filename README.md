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

1. After clone the CTFd repository, don't change directory. Clone this repository to the same CTFd directory. Run the **run_first.py**
2. It first creates a ``.ctfd_secret_key file`` which is required by the next step.
3. It then check the total number of CPU cores, and calculate the total number of workers. Then, it changes the setting. 
````
number_of_workers = 2*number_of_CPUs+1
````
4. The program will add to the following to base template (`themes/core/templates/base.html` if you are using the default theme):
```
<meta name="start_in" content="{{ ctf_starts_in() }}">
<meta name="ends_in" content="{{ ctf_ends_in() }}">
```
5. It then adds the following code right before the line with `id=challenge-window` in `themes/core/templates/challenges.html`. Feel free to manually add on any other pages.
````
<span class="ctfd-auto-scoreboard" style="position: relative; float: right; top: 0px; right: 0px; min-width: 20%;">&nbsp;</span>
````
6. At last, it copies the **auto-scoreboard** plugin to the plugins folder
7. Set an event start or end time in Admin -> Config.
