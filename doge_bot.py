import json

from irc.bot import SingleServerIRCBot
from requests import get

from lib import db, cmds, react, automod


NAME = "dogebot"
OWNER = "plasmodium_"
filename = "tokens.json"
tokens = []

try:
    with open(filename) as f:
        tokens = json.load(f)
except FileNotFoundError:
    pass

class Bot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = NAME.lower()
        self.CLIENT_ID = tokens[0]
        self.TOKEN = tokens[1]
        self.CHANNEL = f"#{OWNER}"

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        """sends message to chat to confirm bot activation"""
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        db.build()
        self.send_message("Now Online.")

    @db.with_commit
    def on_pubmsg(self, cxn, event):
        """
        keeps the bot from reacting to itself
        parses chat input and reads for commands
        """
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]

        react.add_user(bot, user)

        if user["name"] != NAME and automod.clear(bot, user, message):
            react.process(bot, user, message)
            cmds.process(bot, user, message)

    def send_message(self, message):
        """allows bot to post messages to chat"""
        self.connection.privmsg(self.CHANNEL, message)


if __name__ == "__main__":
    bot = Bot()
    bot.start()
