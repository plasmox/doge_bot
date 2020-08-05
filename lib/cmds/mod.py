from .. import db

OWNER = "plasmodium_"

# warnings
warning_timers = (1, 5, 60)


def warn(bot, user, target=None, *reason):
    if target is None:
        bot.send_message("You must specify a target.")
    elif user["name"] == OWNER or user["name"] in TEMP_MOD:
        reason = " ".join(reason)
        warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?",
                            target.lower())
        if warnings is None:
            bot.send_message("That user hasn't visited this channel yet.")
        elif warnings < len(warning_timers):
            mins = warning_timers[warnings]
            bot.send_message(f"/timeout {user['name']} {mins}m")
            bot.send_message(f"{target}, you have been muted for the following reason: {reason}. You will be unmuted for {mins} minute(s).")

            db.execute("UPDATE Users SET Warnings = Warnings + 1 WHERE UserName = ?",
                       target)
        else:
            bot.send_message(f"/ban {target} Repeated infractions.")
            bot.send_message(f"{target}, you have been banned for repeated infractions.")


def remove_warn(bot, user, target=None, *args):
    if target is None:
        bot.send_message("You must specify a target.")
    else:
        warnings = db.field("SELECT Warnings FROM users WHERE UserName = ?",
                            target.lower())

        if warnings == 0:
            bot.send_message(f"{target} has not recieved any warnings.")
        else:
            db.execute("UPDATE users SET Warnings = Warnings - 1 WHERE UserName = ?",
                       target)
            bot.send_message(f"Warning for {target} revoke.")


def buy_timeout(bot, user, target=None, *time):
    """user bought timeout, removes coins, and times out for specific time"""
    try:
        status = db.field("SELECT Type FROM users WHERE UserID = ?", user["id"])
        if status == 1 or target == OWNER:
            bot.send_message("This target cannot be timed out.")
        else:
            # converts *time to int
            time = ' '.join(*time)
            # stores current user's coin to check if they have enough
            coins = db.field("SELECT Coins FROM users WHERE UserID = ?", user["id"])
            cost = 150

            #checks if the user has enough coins
            if coins < cost:
                bot.send_message(f"This command costs {cost} coins. {user['name']}, has only {coins:,} coins.")
            else:
                if target is None:
                    bot.send_message("You must specify a target.")
                else:
                    db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?",
                        cost, user['id'])
                    bot.send_message(f"/timeout {target} {time}s")
                    bot.send_message(f"{target}, has been muted for {time}s by {user['name']}.")
    except TypeError:
        bot.send_message("Please input a user and a time, i.e. !timeout [user] [time]s")


