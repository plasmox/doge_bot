from collections import defaultdict

from . import db

OWNER = "plasmodium_"
CURSES = ("boomer", "thot", "RDR2")
FOLLOW_BOTS = ("wanna become famous?", "followingbot.com", "bigfollows . com", "Buy followers, primes and views")
warning_timers = (1, 5, 15)


def clear(bot, user, message):
    """General user curses"""
    if any([curse in message.lower() for curse in CURSES]):
        warn(bot, user, reason="Cursing")
        return False
    elif any([string in message.lower() for string in FOLLOW_BOTS]):
        bot.send_message(f"/ban {user['name']}")
        bot.send_message(f"{user['name']} has been banned for being a follow bot.")
        return False

    return True


def warn(bot, user, reason=None):
    if user['type'] == 1 or user['name'] == OWNER:
        pass
    else:
        warnings = db.field("SELECT Warnings FROM users WHERE UserID = ?",
                            user["id"])
        if warnings < len(warning_timers):
            mins = warning_timers[warnings]
            bot.send_message(f"/timeout {user['name']} {mins}m")
            bot.send_message(f"{user['name']}, you have been muted for the following reason: {reason}. You will be unmuted in {mins} minute(s).")

            db.execute("UPDATE Users SET Warnings = Warnings + 1 WHERE UserID = ?",
                       user["id"])
        else:
            bot.send_message(f"/ban {user['name']} Repeated infractions.")
            bot.send_message(f"{user['name']}, you have been banned from chat for repeated infractions.")
