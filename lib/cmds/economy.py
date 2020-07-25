from .. import db

OWNER = "plasmodium_"


def coins(bot, user, *args):
    coins = db.field("SELECT Coins FROM users WHERE UserID = ?",
                     user["id"])
    bot.send_message(f"{user['name']}, you have {coins:,} coins.")


def give(bot, user, *args):
    """gives coins from user to another"""
    try:
        input_string = [arg for arg in args]
        target = input_string[0]
        amount = int(input_string[1])
        coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user["id"])

        if user['name'] == OWNER:
            db.execute("UPDATE users SET Coins = Coins + ? WHERE UserName = ?",
                amount, target)
            bot.send_message(f"{target} has been given {amount} coins.")
        else:
            # check if user has coins to give
            if coins < amount:
                bot.send_message(f"{user['name']}, you only have {coins:,} coins to give.")
            else:
                # removes coins from user to give
                db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?",
                           amount, user["id"])
                # gives to other user
                db.execute("UPDATE users SET Coins = Coins + ? WHERE UserName = ?",
                           amount, target)
                bot.send_message(f"{user['name']} has given {coins:,} coins to {target}.")
    except:
        bot.send_message("Please enter a user and amount, i.e. !give [user] [amount]")


def scoreboard(bot, *args):
    """Prints user coin leaderboard to chat"""
    user_list = db.get("SELECT Coins, UserName FROM users")
    dict_1 = {}
    scoreboard = Convert(user_list, dict_1)
    sorted_scoreboard = sorted(scoreboard.items())
    sorted_scoreboard.sort(reverse=True)
    count = 1

    bot.send_message(f"Top 5 coins scoreboard:")
    for coins, user in sorted_scoreboard[:5]:
        bot.send_message(f"{count} - {user}: {coins}")
        count += 1
