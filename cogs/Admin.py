import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext.commands.core import has_permissions
from nextcord.ext.commands import MissingPermissions


class Admin(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @nextcord.slash_command(
        name="add_members",
        description="Give the role Manager to the member",
    )
    async def add_members(
        self,
        ctx,
        member: nextcord.Member,
    ) -> None:
        if "admin" in [role.name.lower() for role in ctx.user.roles]:
            manager_role = nextcord.utils.get(ctx.guild.roles, name="Manager")
            if manager_role in member.roles:
                await ctx.send("Member already has the Manage role.", ephemeral=True)
            else:
                await member.add_roles(manager_role)
                await ctx.send(f"{member.mention} got the role Manager")
        else:
            await ctx.response.send_message("Access unauthorize")

    @nextcord.slash_command(
        name="remove_member",
        description="Remove the role Manager to the member",
    )
    async def remove_member(
        self,
        ctx: Interaction,
        member: nextcord.Member,
    ) -> None:
        if "admin" in [role.name.lower() for role in ctx.user.roles]:
            manager_role = nextcord.utils.get(ctx.guild.roles, name="Manager")

            if manager_role in member.roles:
                await member.remove_roles(manager_role)
                await ctx.send(f"Removed the Manager role from {member.mention}")
            else:
                await ctx.send(
                    f"{member.mention} do not have the role Manager", ephemeral=True
                )
        else:
            await ctx.response.send_message("Access unauthorize")

    @remove_member.error
    async def remove_member_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions for this command.")
        else:
            await ctx.send(error)


def setup(client):
    client.add_cog(Admin(client))
