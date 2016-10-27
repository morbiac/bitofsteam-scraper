from bs4 import BeautifulSoup
import requests
import re
import time
import sqlite3


def bitofsteam():
    """Scrape Bitofsteam and use the SteamSpy API to create a database that stores useful information about the
    games available for sale.
    """
    # Get the information for the games on the bitofsteam website.
    url = "http://www.bitofsteam.com/Store"
    r = requests.get(url, "lxml")
    soup = BeautifulSoup(r.content, "lxml")
    allgames = soup.find_all('div', class_="col-md-4")

    # Create a database to store the information
    conn = sqlite3.connect('bitofsteam.sqlite')
    cur = conn.cursor()
    cur.executescript('''
        DROP TABLE IF EXISTS SteamGames;

        CREATE TABLE SteamGames (
            title     TEXT NOT NULL,
            link TEXT NOT NULL,
            creditcost INTEGER NOT NULL,
            posreviews INTEGER NOT NULL,
            owners INTEGER NOT NULL,
            price FLOAT NOT NULL
        );
        ''')
    for game in allgames:
        # Get url of game
        gameurl = game.find('a')['href']
        # Unimportant, but shows the progress
        print(gameurl)
        # Get the appid of the game
        app = re.search('/(\d+)', gameurl)
        appid = app.group(1)
        # Handle game packages, which return useless api data
        if "/sub/" in gameurl:
            pos_reviews, title, owners, price = 0, 'Game Package', 0, 0
        else:
            pos_reviews, title, owners, price = steamspy(appid)

        # Get credit cost of game
        costpat = re.compile(r'.* Credits')
        for elem in game(text=costpat):
            # Get rid of commas, convert to integer
            gamecost = int(elem[:-8].replace(',', ''))

        # Add game and its info to the database
        cur.execute('''INSERT INTO SteamGames
        (title, link, creditcost, posreviews, owners, price) VALUES ( ?, ?, ?, ?, ?, ?)''',
                    (title, gameurl, gamecost, pos_reviews, owners, price))
        conn.commit()
    conn.commit()


def steamspy(appid):
    """Use the SteamSpy API to get Steam data for a game."""
    # SteamSpy's API only allows 4 requests per second, so sleep for a suitable time between requests.
    time.sleep(.33)
    url = "http://steamspy.com/api.php?request=appdetails&appid={}".format(appid)
    r = requests.get(url)
    data = r.json()
    # Get the positive review percentage. Return 0 if no review data.
    try:
        pos_reviews = int(data['score_rank'])
    except ValueError:
        pos_reviews = 0
    # Game name
    title = data['name']
    # Estimated number of owners. This is useful for weeding out "highly reviewed" games that may have few reviews.
    owners = int(data['owners'])
    # Price, converted to dollars. Return 0 if no price data.
    try:
        price = float(int(data['price'])/100)
    except TypeError:
        price = 0
    return pos_reviews, title, owners, price

bitofsteam()
