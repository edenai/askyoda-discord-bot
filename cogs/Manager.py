import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from yoda import Askyoda
from nextcord.ext.commands.core import has_role
from decouple import config


class Manager(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.yoda = Askyoda(config("PROJECT_ID"))

    async def get_text(self, thread: nextcord.Thread):
        try:
            string = []
            history = await thread.history().flatten()
            for message in history:

                if message.author == self.client.user:
                    pass
                if message.content[0] == "!":
                    string.append(message.content[1:])

            fstr = " ".join(string)
            return f"Question : {history[-1].content}\n Answer:{fstr}"

            # for message in thread.history().flatten():
            #     if message.content["0"] == "!":
            #         print(message)
        except Exception as e:
            print(e)

    @nextcord.slash_command(
        name="add_url",
        description="This command is to add data to your project",
    )
    async def add_url(self, ctx: Interaction, url: str):
        if "Eden AI Team" in [role.name for role in ctx.user.roles]:
            await ctx.response.send_message("Trying to add : " + url)
            result = self.yoda.add_urls([url])
            await ctx.send(result)
        else:
            await ctx.response.send_message("Access unauthorize")

    @nextcord.slash_command(
        name="get_collection_info",
        description="This command is to get info about the collection",
    )
    async def get_collection_info(self, ctx: Interaction):
        if "Eden AI Team" in [role.name for role in ctx.user.roles]:
            await ctx.response.send_message("Wait pls")
            result = self.yoda.get_collection_info()
            await ctx.send(result)
        else:
            await ctx.response.send_message("Access unauthorize")

    @nextcord.slash_command(
        name="save",
        description="This command is to save a thread",
    )
    async def save_thread(self, ctx: Interaction):
        if "Eden AI Team" in [role.name for role in ctx.user.roles]:
            # result = self.yoda.add_texts()
            text = await self.get_text(ctx.channel)
            await ctx.send("trying to save", ephemeral=True)
            result = self.yoda.add_texts(text)
            await ctx.send("saved", ephemeral=True)
        else:
            await ctx.response.send_message("Access unauthorize")


def setup(client):
    client.add_cog(Manager(client))
