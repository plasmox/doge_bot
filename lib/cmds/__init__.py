from time import time

from . import misc, economy, games, mod

PREFIX = "!"


class Cmd(object):

    def __init__(self, callables, func=None, cooldown=0):
        self.callables = callables
        self.func = func
        self.cooldown = cooldown
        self.next_use = time()


cmds = [
    # misc
    Cmd(["hello", "hi", "hey"], misc.hello, cooldown=15),
    Cmd(["userinfo", "ui"], misc.userinfo),
    Cmd(["translate"], misc.translate, cooldown=2),
    Cmd(["yeet"], misc.yeet, cooldown=5),
    Cmd(["botTime"], misc.bot_uptime, cooldown=5),
    Cmd(["shutdown"], misc.shutdown),
    # economy
    Cmd(["coins", "money"], economy.coins, cooldown=5),
    Cmd(["give"], economy.give, cooldown=1),
    Cmd(["scoreboard"], economy.scoreboard, cooldown=60),
    # games
    Cmd(["coinflip", "flip"], games.coinflip, cooldown=30),
    Cmd(["heist"], games.start_heist, cooldown=5),
    # mod
    Cmd(["warn"], mod.warn),
    Cmd(["timeout"], mod.buy_timeout, cooldown=60),
    Cmd(["unwarn", "rmwarn"], mod.remove_warn),
]

nightbot_cmds = ['8ball', 'bestmod', 'broken', 'bru', 'clang', 'dannytime', 'discord',
                 'eerie', 'factorio', 'falic', 'followage', 'gitgud', 'hug', 'ihatemylife',
                 'kiss', 'lurk', 'mistake', 'mjr', 'mods', 'moshimoshi', 'null', 'oc', 'oof',
                 'party', 'party2', 'pawel', 'pawelgoat', 'pizzaparty', 'plastechnique',
                 'quote1', 'quote2', 'quote3', 'quote4', 'quote5', 'quote6', 'quote69', 'quote7',
                 'quote8', 'read', 'reading', 'se', 'server', 'setdeths', 'so', 'terraria',
                 'time', 'tuck', 'twitchprime', 'unlurk', 'uptime', 'walter-old', 'wife']


def process(bot, user, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):]
        args = message.split(" ")[1:]
        perform(bot, user, cmd, *args)


def perform(bot, user, call, *args):
    if call in ("help", "commands", "cmds"):
        misc.help(bot, PREFIX, cmds)
    elif call in nightbot_cmds:
        pass
    else:
        for cmd in cmds:
            if call.lower() in cmd.callables:
                if time() > cmd.next_use:
                    cmd.func(bot, user, *args)
                    cmd.next_use = time() + cmd.cooldown
                else:
                    bot.send_message(f"Cooldown still in effect. Try again in {cmd.next_use-time():,.0f} seconds.")
                return
        bot.send_message(f"{user['name']}, \"{call}\" isn't a registered command.")
