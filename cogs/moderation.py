import discord
import json
from discord.ext import commands

with open("configs.json", "r") as f:
    case = json.load(f)

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, user: discord.Member = None, *, reason = None):
        server = ctx.guild
        author = ctx.author
        channel = ctx.channel
        perms = channel.permissions_for(author).kick_members
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Kick Members** permissions, **{author.name}**")
            return
        if not user:
            await ctx.send(f":bangbang: **|** You need to state a user for me to kick, **{author.name}**")
            return
        if user == author:
            await ctx.send(f":bangbang: **|** You can't kick your self silly, **{author.name}**")
            return
        if user.top_role.position >= author.top_role.position and ctx.author != ctx.guild.owner:
            if author == server.owner:
                pass
            else:
                await ctx.send(f":bangbang: **|** You can't kick someone that has a higher role position than you, **{author.name}**")
                return
        if not str(server.id) in case:
            case[str(server.id)] = {}
        if not "case" in case[str(server.id)]:
            case[str(server.id)]["case"] = 0
        await user.kick()
        case[str(server.id)]["case"] += 1
        cases = case[str(server.id)]["case"]
        await ctx.send(f"<:tool:521458807558373420> **|** **``Case #{cases}``** {user.mention}/**{user.id}** has been kicked.")
        await ctx.send(f"Reason for kick: {reason}")
        with open("configs.json", "w") as f:
            json.dump(case,f,indent=4)

    @commands.command()
    async def ban(self, ctx, user: discord.Member = None, *, reason = None):
        server = ctx.guild
        author = ctx.author
        channel = ctx.channel
        perms = channel.permissions_for(author).ban_members
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Ban Members** permissions, **{author.name}**")
            return
        if not user:
            await ctx.send(f":bangbang: **|** You need to state a user for me to ban, **{author.name}**")
            return
        if user == author:
            await ctx.send(f":bangbang: **|** You can't ban your self silly, **{author.name}**")
            return
        if user.top_role.position >= author.top_role.position and ctx.author != ctx.guild.owner:
            if author == server.owner:
                pass
            else:
                await ctx.send(f":bangbang: **|** You can't ban someone that has a higher role position than you, **{author.name}**")
                return
        if not str(server.id) in case:
            case[str(server.id)] = {}
        if not "case" in case[str(server.id)]:
            case[str(server.id)]["case"] = 0
        await user.ban()
        case[str(server.id)]["case"] += 1
        cases = case[str(server.id)]["case"]
        await ctx.send(f"<:tool:521458807558373420> **|** **``Case #{cases}``** {user.mention}/**{user.id}** has been banned.")
        await ctx.send(f"Reason for ban: {reason}")
        with open("configs.json", "w") as f:
            json.dump(case,f,indent=4)

    @commands.command()
    async def softban(self, ctx, user: discord.Member = None, *, reason = None):
        server = ctx.guild
        author = ctx.author
        channel = ctx.channel
        perms = channel.permissions_for(author).ban_members
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Ban Members** permissions, **{author.name}**")
            return
        if not user:
            await ctx.send(f":bangbang: **|** You need to state a user for me to softban, **{author.name}**")
            return
        if user == author:
            await ctx.send(f":bangbang: **|** You can't softban your self silly, **{author.name}**")
            return
        if user.top_role.position >= author.top_role.position and ctx.author != ctx.guild.owner:
            if author == server.owner:
                pass
            else:
                await ctx.send(f":bangbang: **|** You can't softban someone that has a higher role position than you, **{author.name}**")
                return
        if not str(server.id) in case:
            case[str(server.id)] = {}
        if not "case" in case[str(server.id)]:
            case[str(server.id)]["case"] = 0
        await user.ban()
        await user.unban()
        case[str(server.id)]["case"] += 1
        cases = case[str(server.id)]["case"]
        await ctx.send(f"<:tool:521458807558373420> **|** **``Case #{cases}``** {user.mention}/**{user.id}** has been softbanned.")
        await ctx.send(f"Reason for ban: {reason}")
        with open("configs.json", "w") as f:
            json.dump(case,f,indent=4)

    @commands.command(aliases=["clear"])
    async def purge(self, ctx, limit: int=None):
        channel = ctx.channel
        server = ctx.guild
        author = ctx.author
        perms = channel.permissions_for(author).manage_messages
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Messages** permissions, **{author.name}**")
            return
        if not limit:
            await ctx.send(f":bangbang: **|** You need to state a amount for me to clear, **{author.name}**")
            return
        if limit is None:
            limit = 10
        elif limit > 100:
            limit = 100
        try:
            deleted = await channel.purge(limit=limit, before=ctx.message)
            await ctx.message.delete()
            await ctx.send(f"Purged **{limit}** messages.", delete_after=5)
        except discord.HTTPException:
            await ctx.send(":bangbang: **|** I can't delete a message 14 days or older, **{author.name}**")
            return
        except:
            pass

    @commands.command()
    async def text(self, ctx, *, text = None):
        channel = ctx.channel
        server = ctx.guild
        author = ctx.author
        perms = channel.permissions_for(author).manage_messages
        if not perms:
            await ctx.send(f":bangbang: **|** You need **Manage Messages** permissions, **{author.name}**")
            return
        if not text:
            await ctx.send(f":bangbang: **|** You need to state a text for me to say.., **{author.name}**")
            return
        embed = discord.Embed(color=0xb55aec)
        embed.description = text
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
