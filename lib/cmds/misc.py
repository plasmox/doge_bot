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
        # takes tuple and stores information as string
        chat_tuple = _string_conversion(args)

        # store languages into variables
        input_language = chat_tuple.split(" ", 1)[0]
        string_list = chat_tuple.split(" ", 1)[1:]
        # exception for chinese, if chinese is typed in, default chinese (simplified)
        if input_language.lower() == "chinese":
            input_language = 'zh-cn'
        # convert the original string from a list to a string
        original_string = _string_conversion(string_list)
        translator = Translator()
        translated_str = translator.translate(f'{original_string}', dest=f'{input_language}')
        bot.send_message(f"{translated_str.text}")
    except ValueError:
        # if the user tries to translate to a language that doesn't exist
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
