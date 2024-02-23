import random
import nextcord
from nextcord.ext import commands
from yoda import Askyoda
from decouple import config

def member_has_role(member, role_name):
    """Checks if a member has the specified role.

    Args:
        member: The Discord member object to check.
        role_name: The name of the role to check.

    Returns:
        True if the member has the role, False otherwise.
    """
    print(member.roles)
    for role in member.roles:
        if role.name == role_name:
            return True
    return False
async def get_text(thread: nextcord.Thread):
        try:
            history = await thread.history().flatten()
            for message in history:

                if member_has_role(message.author, 'Developer'):
                    return True
             
            return False

            # for message in thread.history().flatten():
            #     if message.content["0"] == "!":
            #         print(message)
        except Exception as e:
            print(e)

async def check_messages(thread:nextcord.Thread,author):
    try:
        history = await thread.history().flatten()
        for message in history:
            print(message.author)
            if message.author==author.user:
                return True
             
        return False
    except Exception as e:
            print(e)

class User(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.yoda = Askyoda(config("PROJECT_ID"))

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author == self.client.user:
            return
        if message.content[0] == "!":
            return
        

        if message.channel.parent_id:
            if message.channel.parent_id == int(config("CHANNEL_ID")):
                if "Eden AI Team" in [role.name for role in message.author.roles]:
                    return

                else:
                    self.developer = nextcord.utils.get(
                        message.guild.roles, name="Developer"
                    )
                    members=self.developer.members # type: ignore
              
                    chosen_dev = random.choice(members)
                    try:
                        print(check_messages(message.channel,self.client))
                        if await check_messages(message.channel,self.client):

                            return
                        else:
                            async with message.channel.typing():
                                result = self.yoda.ask_llm(message.content)
                                if result == True:

                                    await message.reply(
                                        f"{chosen_dev.mention} I need some help"
                                    )
                                else:

                                    await message.reply(f" 🤖 _So that we can answer you quickly, we suggest an AI-generated answer using [AskYoda](https://app.edenai.run/bricks/edenai-products/askyoda/default) :_ \n\n{result}\n\n _If this doesn't answer your question, you can tag an @Developer.👍 We'll try to answer as quickly as possible with a real human 😉. Note that the bot answers only once (no point in replying to it)._")
                    except Exception as e:
                        print(e)
                        await message.reply(
                            f"{chosen_dev.mention} I need some help"
                        )

        # if user_message[0] == "!":
        #     user_message = user_message[1:]
        #     result = yoda.add_urls([user_message])
        #     await send_message(message, result)
        # elif user_message[0] == "?":
        #     result = yoda.get_collection_info()
        #     await send_message(message, result)
        # else:
        #     result = yoda.ask_llm(user_message)
        #     await send_message(message, result)


def setup(client):
    client.add_cog(User(client))
