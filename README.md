Bitofsteam scraper (Python 3)
=============================

This is a simple script that scrapes the store at http://www.bitofsteam.com/Store for the list of games and their current prices. It then accesses the [SteamSpy API](http://steamspy.com/api.php) for each of those games and adds additional data to an sqlite database (price on Steam, percentage of positive reviews, estimated number of owners). It makes use of the [Requests](http://docs.python-requests.org/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) libraries.

It does not currently do anything with that database, but you can view it in something like [DB Browser for Sqlite](http://sqlitebrowser.org/) and filter the data to find games you might want to purchase without clicking through countless poorly-reviewed games.
 
Usage
-----

By default, it will create a database called bitofsteam.sqlite which will be re-written whenever the script is run. This may be changed in the future, to allow the script to notify you of new games that weren't scraped previously.

To run the script, simply enter this command: 

	python bitofsteam.py

It will provide visual output in the form of steam links for each game, just to show that it's working. It may take a couple minutes to complete, as SteamSpy asks that its API not be accessed more than 4 times a second. This script aims for 3 per second.
