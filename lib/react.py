import json

from collections import defaultdict
from datetime import datetime, timedelta
from random import randint
from re import search
from time import time

from . import db
from .cmds import games

welcomed = []
messages = defaultdict(int)

filename = 'welcomed.json'

try:
    with open(filename) as f:
        welcomed = json.load(f)
except FileNotFoundError:
    pass


def process(bot, user, message):
    h = games.heist
    update_records(bot, user)

    if user["id"] not in welcomed:
        welcome(bot, user)

    elif "bye" in message:
        say_goodbye(bot, user)

    # if user["id"] != "STREAMER ID NUMBER"
    check_activity(bot, user)

    match = search(r'cheer[0-9]+', message)
    if match is not None:
        thank_for_cheer(bot, user, match)

    if h is not None:
        if h.start_time <= time() and not h.running:
            games.run_heist(bot)
        elif h.end_time <= time() and h.running:
            games.end_heist(bot)


def add_user(bot, user):
    """Adds first time users to the DB"""
    db.execute("INSERT OR IGNORE INTO users (UserID, UserName, Type) VALUES (?, ?, ?)",
               user["id"], user["name"].lower(), user["type"])


def update_records(bot, user):
    db.execute("UPDATE users SET UserName = ?, MessagesSent = MessagesSent + 1, Type = ? WHERE UserID = ?",
               user["name"].lower(), user["type"], user["id"])

    stamp = db.field("SELECT CoinLock FROM users WHERE UserID = ?",
                     user["id"])

    if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.utcnow():
        coinlock = (datetime.utcnow() + timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")

        db.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?",
                   randint(1, 5), coinlock, user["id"])


def welcome(bot, user):
    """
    greets new users, and sets them up in the db
    users in db will not be greeted again
    """
    bot.send_message(f"Welcome to the stream {user['name']}!")
    welcomed.append(user["id"])
    with open(filename, 'w') as f:
        json.dump(welcomed, f)


def say_goodbye(bot, user):
    bot.send_message(f"See ya later {user['name']}!")
    welcomed.remove(user["id"])


def check_activity(bot, user):
    messages[user["id"]] += 1
    count = messages[user["id"]]

    if count % 100 == 0:
        bot.send_message(f"Thanks for being active in chat {user['name']} - you've sent {count:,} messages! Keep it up!")


def thank_for_cheer(bot, user, match):
    bot.send_message(f"Thanks for the {match.group[5:]:,} bits {user['name']}! That's really appreciated!")
