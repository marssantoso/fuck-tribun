# A reddit bot to fuck with tribunnews

## How to run

* Install the dependencies with `pip install -r requirements.txt`
* Add `praw.ini` file based on [this guide](https://praw.readthedocs.io/en/v4.0.0/getting_started/configuration/prawini.html)
* Add a `.env` file to referring to the `.env.example` file
* Run the `bot.py` file

## How the bot works

### Posts

* It finds submissions that links from the listed sites
* If the link posted isn't the full-page version (from the params), it replies with the correct link

### Comments

* It finds comments with the available commands and mentions of the bot
* It will reply said comment with appropriate command

## Listed Sites

* tribunnews.com
* kompas.com
* detik.com

## Available Commands

* `!fulltext` – reply the full text of an article within a post

## Change logs

### 2020-07-09

* Add support for other sites and params
* Fix url with multiple query params
* A bunch of refactoring
* Can now listen to command to post the full text of an article
  * Simply mention the bot with the `!fulltext` command
  * Links doesn’t have to be from the listed sites (but notes: doesn’t seem to work on some sites)

### 2020-02-06

* Initial release
* Replies submission links from tribunnews.com that isn't the full-page version with the correct link

