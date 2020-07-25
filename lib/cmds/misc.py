from googletrans import Translator
from datetime import timedelta
from sys import exit
from time import time

from .. import db

BOOT_TIME = time()
OWNER = "plasmodium_"


def help(bot, prefix, cmds):
    '''sends the current list of commands'''
    # base commands
    bot.send_message(f"Registered commands: "
                     + ", ".join([f"{prefix}{cmd.callables[0]}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))
    # alias
    bot.send_message(f"Registered commands (incl. aliases): "
                     + ", ".join([f"{prefix}{'/'.join(cmd.callables)}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))


def hello(bot, user, *args):
    """test command to greet user"""
    bot.send_message(f"Hello, {user['name']}!")


def translate(bot, str, *args):
    """takes a string and translates it"""
    try:
        # stores args in a list
        input_string = [arg for arg in args]
        language = input_string[0]
        original = ' '.join(input_string[1:])
        # defaults the input of chinese to simp chinese
        if language.lower() == "chinese":
            language = "zh-cn"
        translator = Translator()
        # translates input text
        translated_string = translator.translate(f"{original}", dest=f"{language}")
        bot.send_message(f"{translated_string.text}")
    except ValueError:
        bot.send_message("Please input a valid language")


def _string_conversion(tup):
    """helper function for translate, converts tuple to string"""
    str = ' '.join(tup)
    return str


def yeet(bot, user, *args):
    """bans users if they say 'yeet'"""
    bot.send_message(f"{user['name']} has been yeet'ed for 10 seconds.")
    bot.send_message(f"/timeout {user['name']} 10")


def bot_uptime(bot, user, *args):
    """current bot uptime"""
    bot.send_message(f"The bot has been online for {timedelta(seconds=time()-BOOT_TIME)}.")


def userinfo(bot, user, *args):
    bot.send_message(f"Name: {user['name']}. ID: {user['id']}.")


def shutdown(bot, user, *args):
    if user["name"].lower() == OWNER:
        bot.send_message("Shutting down.")
        print('bot shutdown')
        db.commit()
        db.close()
        bot.disconnect()
        exit(0)

    else:
        bot.send_message("You can't do that.")
