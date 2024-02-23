import nextcord
from nextcord.ext import commands
import os
from decouple import config

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("The bot is up")
    print(nextcord.__version__)
    print("-----------------------------")


initial_extensions = []
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == "__main__":
    for extension in initial_extensions:
        client.load_extension(extension)


client.run(config("TOKEN"))
