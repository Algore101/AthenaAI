# AthenaAI
A Discord bot that does a bunch of Overwatch 2 related things.
## Contents
- [Features](#features)
  - [Random selection](#random-selection)
  - [Games](#games)
  - [Global personal profiles](#global-personal-profiles)
- [Commands](#commands)
  - [Core commands](#core-commands)
  - [Game commands](#game-commands)
  - [User-specific commands](#user-specific-commands)
  - [Other commands](#other-commands)

## Features
### Random selection
Get a random hero, role, or hero duo, including optimal hero duos
### Games
A variety of games including _Guess The Hero_, trivia, and _Overwatch GeoGuessr_
### Global personal profiles
Avoid getting heroes you don't like and keep track of your trivia scores from any server

Keep on reading to discover everything AthenaAI can do

## Commands
Commands marked with an \*asterisk are optional
### Core commands:
- **/hero \[\*role] \[\*duo]** - Respond with a random hero/duo in the selected role
  - \*role (`all`,`tank`,`damage`,`support`) - The role of the hero/duo you want to get a hero from, `all` by default
  - \*duo (`optimal`,`random`) - The type of duo, leave empty for a single hero
- **/role** - Respond with a role
### Game commands:
- **/trivia \[questions] \[difficulty]** - Play an Overwatch 2 hero trivia game
  - questions (1-10) - The number of questions to play
  - difficulty (`easy`,`hard`) - The difficulty level of the questions
- **/guess \[questions] \[difficulty]** - Play a game of "Guess The Hero"
  - questions (1-10) - The number of questions to play
  - difficulty (`easy`,`hard`) - The difficulty level of the questions
- **/geoguess \[questions] \[difficulty]** - Play a game of "Guess The Map"
  - questions] (1-10) - The number of questions to play
  - difficulty (`easy`,`hard`) - The difficulty level of the questions
- **/scoreboard** - Show the top trivia players
### User-specific commands:
- **/profile \[function]** - View your profile
  - function (`delete`) - The function to initiate with your profile
- **/avoid \[hero]** - Add a hero to your avoid list
  -  hero - The name of the hero to avoid
- **/unavoid \[hero]** - Remove a hero from your avoid list
  - hero - The name of the hero to remove from avoid list
### Other commands:
- **/help** - Respond with a list of commands
- **/list \[\*role]** - Respond with a list of all the heroes in the selected role
  - \*role (`all`,`tank`,`damage`,`support`) - The role get the hero list from
- **/dm** - Respond in the user's dms

## User profiles
In order to allow users to avoid heroes and compete in games, AthenaAI creates a profile with the following data:
- Your username
- Heroes you have chosen to avoid
- Your game scores

Your username (excluding the \#0001 identifier at the end of your name) is only shared with users in the same servers as you and cannot be accessed by anyone outside
### Creating a profile
There are some commands that invoke the creation of your profile. These commands are:
- `/profile`
- `/avoid`
- `/unavoid`
### Deleting your profile
Using `/profile function:delete` removes your profile from the AthenaAI records.

Deleting your profile removes everything across all servers: your username, avoided heroes, and trivia score. It will be as if you never used AthenaAI.

The use of any of the [creation commands](#creating-a-profile) will create a profile for you again.

