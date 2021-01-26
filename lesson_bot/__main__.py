import discord
from .client import Client
from .config import bot_id


def main():
    intents = discord.Intents.all()

    client = Client(intents=intents)
    client.run(bot_id)


if __name__ == "__main__":
    main()
