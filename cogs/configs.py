import discord
import json
import random
import asyncio
from discord.ext import commands

class Configs:
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.group()
    async def set(self, ctx):
        if not ctx.invoked_subcommand:
            embed = discord.Embed(color=0xb55aec)
            msg = """
            **!set welcome-message <message>** - If you do not wish to set one you can do: ``!set welcome-message default``
            **!set welcome-channel <#Channel>** - Set the welcome channel...
            **!set auto-role** - This will go through the list of server roles and you can pick one...
            **!set mute-role** - Same thing as the auto-role
            **!set farewell-message <message>** - If you do not wish to set one you can do: ``!set farewell-message default``
            **!set farewell-channel <#Channel>** - Set the farewell channel...

            **__VARIABLES__**

            **{member}** - Mention the user on join and say the tag and name when left
            **{server}** - Servers name
            **{member_count}** - Servers member count
            """
            embed.add_field(name="<:tool:521458807558373420> Settings", value="To set a setting up do: ``!set <setting>``")
            embed.add_field(name="<a:yus:521452481612480512> Options", value=msg)
            await ctx.send(embed=embed)

    @set.command(name="welcome-message")
    async def welcomemsg(self, ctx, *, message: str = None):
        with open("configs.json", "r") as f:
            welcome = json.load(f)
        server = ctx.guild
        author = ctx.author
        channel = ctx.channel
        perms = channel.permissions_for(author).manage_guild
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Server** permissions, **{author.name}**")
            return
        if not message:
            await ctx.send(f":bangbang: You need to state a welcome message")
            return
        if not str(server.id) in welcome:
            welcome[str(server.id)] = {}
        if str(server.id) in welcome:
            welcome[str(server.id)]["welcome message"] = message
            await ctx.send(f"Set welcome message to:")
            embed = discord.Embed(color=0xb55aec)
            embed.description = message
            await ctx.send(embed=embed)
        with open("configs.json", "w") as f:
            json.dump(welcome, f, indent=4)

    @set.command(name="welcome-channel")
    async def welcomechan(self, ctx, channel: discord.TextChannel = None):
        with open("configs.json", "r") as f:
            welcome = json.load(f)
        server = ctx.guild
        author = ctx.author
        channel1 = ctx.channel
        perms = channel1.permissions_for(author).manage_guild
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Server** permissions, **{author.name}**")
            return
        if not channel:
            await ctx.send(f":bangbang: **|** You need to state a welcome channel, **{author.name}**")
            return
        chan = self.bot.get_channel(channel.id)
        if not str(server.id) in welcome:
            welcome[str(server.id)] = {}
        if str(server.id) in welcome:
            welcome[str(server.id)]["welcome channel"] = channel.id
            await ctx.send("Set welcome channel to:")
            embed = discord.Embed(color=0xb55aec)
            embed.description = channel.mention
            await ctx.send(embed=embed)
        with open("configs.json", "w") as f:
            json.dump(welcome, f, indent=4)
    @welcomechan.error
    async def welcomechan_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            author = ctx.author
            await ctx.send(f":bangbang: **|** Invalid channel, **{author.name}**")

    @set.command(name="farewell-message")
    async def farewellmsg(self, ctx, *, message: str = None):
        with open("configs.json", "r") as f:
            farewell = json.load(f)
        server = ctx.guild
        author = ctx.author
        channel = ctx.channel
        perms = channel.permissions_for(author).manage_guild
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Server** permissions, **{author.name}**")
            return
        if not message:
            await ctx.send(f":bangbang: You need to state a farewell message")
            return
        if not str(server.id) in farewell:
            farewell[str(server.id)] = {}
        if str(server.id) in farewell:
            farewell[str(server.id)]["farewell message"] = message
            await ctx.send(f"Set farewell message to:")
            embed = discord.Embed(color=0xb55aec)
            embed.description = message
            await ctx.send(embed=embed)
        with open("configs.json", "w") as f:
            json.dump(farewell, f, indent=4)

    @set.command(name="farewell-channel")
    async def farewellchan(self, ctx, channel: discord.TextChannel = None):
        with open("configs.json", "r") as f:
            farewell = json.load(f)
        server = ctx.guild
        author = ctx.author
        channel1 = ctx.channel
        perms = channel1.permissions_for(author).manage_guild
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Server** permissions, **{author.name}**")
            return
        if not channel:
            await ctx.send(f":bangbang: **|** You need to state a farewell channel, **{author.name}**")
            return
        chan = self.bot.get_channel(channel.id)
        if not str(server.id) in farewell:
            farewell[str(server.id)] = {}
        if str(server.id) in farewell:
            farewell[str(server.id)]["farewell channel"] = channel.id
            await ctx.send("Set farewell channel to:")
            embed = discord.Embed(color=0xb55aec)
            embed.description = channel.mention
            await ctx.send(embed=embed)
        with open("configs.json", "w") as f:
            json.dump(farewell, f, indent=4)
    @farewellchan.error
    async def farewellchan_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            author = ctx.author
            await ctx.send(f":bangbang: **|** Invalid channel, **{author.name}**")

    @set.command(name="auto-role")
    async def auto_role(self, ctx, *, role = None):
        with open("configs.json", "r") as f:
            auto_role = json.load(f)
        server = ctx.guild
        author = ctx.author
        channel1 = ctx.channel
        perms = channel1.permissions_for(author).manage_guild
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Server** permissions, **{author.name}**")
            return
        if not role:
            await ctx.send(f":bangbang: **|** You need to state a role, **{author.name}**")
            return
        role1 = discord.utils.get(server.roles, name=role)
        if not role1:
            await ctx.send(f":bangbang: **|** Invalid role, **{author.name}**")
            return
        if not str(server.id) in auto_role:
            auto_role[str(server.id)] = {}
        if str(server.id) in auto_role:
            auto_role[str(server.id)]["auto-role"] = role
            await ctx.send(f"Set auto-role to:")
            embed = discord.Embed(color=0xb55aec)
            embed.description = role
            await ctx.send(embed=embed)
        with open("configs.json", "w") as f:
            json.dump(auto_role, f, indent=4)

    @set.command(name="mute-role")
    async def mute_role(self, ctx, *, role = None):
        with open("configs.json", "r") as f:
            mute_role = json.load(f)
        server = ctx.guild
        author = ctx.author
        channel1 = ctx.channel
        perms = channel1.permissions_for(author).manage_guild
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Server** permissions, **{author.name}**")
            return
        if not role:
            await ctx.send(f":bangbang: **|** You need to state a role, **{author.name}**")
            return
        role1 = discord.utils.get(server.roles, name=role)
        if not role1:
            await ctx.send(f":bangbang: **|** Invalid role, **{author.name}**")
            return
        if not str(server.id) in mute_role:
            mute_role[str(server.id)] = {}
        if str(server.id) in mute_role:
            mute_role[str(server.id)]["mute-role"] = role
            await ctx.send(f"Set mute-role to:")
            embed = discord.Embed(color=0xb55aec)
            embed.description = role
            await ctx.send(embed=embed)
        with open("configs.json", "w") as f:
            json.dump(mute_role, f, indent=4)

    async def on_member_join(self, member):
        with open("configs.json", "r") as f:
            welcome = json.load(f)
        server = member.guild
        if not str(server.id) in welcome:
            welcome[str(server.id)] = {}
        msg = welcome[str(server.id)]["welcome message"].format(**{'member': member.mention, 'server': server.name, 'member_count': server.member_count})
        chan = welcome[str(server.id)]["welcome channel"]
        auto_role = welcome[str(server.id)]["auto-role"]
        role = discord.utils.get(server.roles, name=auto_role)
        channel = self.bot.get_channel(chan)
        await channel.send(msg)
        await member.add_roles(role)

    async def on_member_remove(self, member):
        with open("configs.json", "r") as f:
            farewell = json.load(f)
        server = member.guild
        if not str(server.id) in farewell:
            farewell[str(server.id)] = {}
        msg = farewell[str(server.id)]["farewell message"].format(**{'member': member, 'server': server.name, 'member_count': server.member_count})
        chan = farewell[str(server.id)]["farewell channel"]
        channel = self.bot.get_channel(chan)
        await channel.send(msg)

    @commands.command()
    async def help(self, ctx):
        msg = """
        **Moderation**:

        **!kick @User reason** - Kick a user
        **!ban @User reason** - Ban a user
        **!softban @User reason** - Softban a user (ban then unban him/her)
        **!purge <1 - 100>** - Purge an amount of text
        **!text <text>** - Say something

        **Settings**:

        **!set <auto-role> <role>** - Set the auto-role
        **!set farewell-message <message>** - Set the goodbye message
        **!set farewell-channel #Channel** - Set the goodbye channel
        **!set welcome-message <message>** - Set the welcome message
        **!set welcome-channel #Channel** - Set the welcome channel

        **Economy**:

        **!daily** - Get a daily allowance
        **!work** - Get a work allowance
        **!give @User <amount>** - Give your friend some money
        **!leaderboard** - Just say that and it will go through some leaderboards
        **!stats** - See your stats
        **!gamble <amount>** - Just a fun gambling command

        **Misc**:

        **!server** - Get server invite
        **!invite** - Get the bot invite
        """
        embed = discord.Embed(color=0xb55aec)
        embed.description = msg
        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        embed = discord.Embed(color=0xb55aec)
        embed.description = "Here is the server invite: [Server invite](https://discord.gg/VcaKJG)"
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(color=0xb55aec)
        embed.description = "Here is the bot invite: [Bot invite](https://discordapp.com/api/oauth2/authorize?client_id=520794124732071937&permissions=8&scope=bot)"
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Configs(bot))
