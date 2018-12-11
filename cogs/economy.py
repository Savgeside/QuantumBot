import discord
import json
import random
from discord.ext import commands

class Economy:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_account(self, ctx):
        with open("money.json", "r") as f:
            economy = json.load(f)
        server = ctx.guild
        author = ctx.author
        if not str(server.id) in economy:
            economy[str(server.id)] = {}
        if str(author.id) in economy[str(server.id)]:
            await ctx.send(f":bangbang: **|** You already have an account, **{author.name}**")
            return
        if not str(author.id) in economy[str(server.id)]:
            economy[str(server.id)][str(author.id)] = {"balance": 0, "networth": 0, "daily-streak": 0}
            await ctx.send(f":tada: You have created an account, **{author.name}**")
        with open("money.json", "w") as f:
            json.dump(economy,f,indent=4)

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        with open("money.json", "r") as f:
            economy = json.load(f)
        server = ctx.guild
        author = ctx.author
        randmoney = random.randint(100, 700)
        if not str(server.id) in economy:
            economy[str(server.id)] = {}
        if not str(author.id) in economy[str(server.id)]:
            await ctx.send(f":bangbang: **|** You need to create a account, you can do this by doing: **!create_account**")
            return
        economy[str(server.id)][str(author.id)]["balance"] += randmoney
        economy[str(server.id)][str(author.id)]["networth"] += randmoney
        await ctx.send(f":moneybag: **|** You gained **${randmoney}** for work today!")
        with open("money.json", "w") as f:
            json.dump(economy,f,indent=4)
    @work.error
    async def cooldown_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if h == 0:
                time = "**%d** minute(s) **%d** second(s)" % (m, s)
            elif h == 0 and m == 0:
                time = "**%d** second(s)" % (s)
            else:
                time = "**%d** hour(s) **%d** minute(s) **%d** second(s)" % (h, m, s)
            return await ctx.send(":stopwatch: **|** You are on cooldown, time remaining: {}".format(time))

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        with open("money.json", "r") as f:
            economy = json.load(f)
        server = ctx.guild
        author = ctx.author
        randmoney = random.randint(100, 700)
        if not str(server.id) in economy:
            economy[str(server.id)] = {}
        if not str(author.id) in economy[str(server.id)]:
            await ctx.send(f":bangbang: **|** You need to create a account, you can do this by doing: **!create_account**")
            return
        economy[str(server.id)][str(author.id)]["balance"] += randmoney
        economy[str(server.id)][str(author.id)]["networth"] += randmoney
        economy[str(server.id)][str(author.id)]["daily-streak"] += 1
        daily_streak = economy[str(server.id)][str(author.id)]["daily-streak"]
        await ctx.send(f":moneybag:  **|** You gained **${randmoney}** today!")
        await ctx.send(f":signal_strength:  **|** Congrats! Your new daily-streak is now **{daily_streak}**!")
        with open("money.json", "w") as f:
            json.dump(economy,f,indent=4)
    @daily.error
    async def cooldown_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if h == 0:
                time = "%d minute(s) %d second(s)" % (m, s)
            elif h == 0 and m == 0:
                time = "%d second(s)" % (s)
            else:
                time = "**%d** hour(s) **%d** minute(s) **%d** second(s)" % (h, m, s)
            return await ctx.send(":stopwatch: **|** You are on cooldown, time remaining: {}".format(time))

    @commands.command()
    async def give(self, ctx, user: discord.Member = None, amount: int = None):
        with open("money.json", "r") as f:
            economy = json.load(f)
        server = ctx.guild
        author = ctx.author
        if not str(server.id) in economy:
            economy[str(server.id)] = {}
        if not str(author.id) in economy[str(server.id)]:
            await ctx.send(f":bangbang: **|** You need to create a account, you can do this by doing: **!create_account**")
            return
        if user == author:
            await ctx.send(f":bangbang: **|** You can't give money to your self silly..")
            return
        if not str(user.id) in economy[str(server.id)]:
            await ctx.send(f":bangbang: **|** **{user.name}** needs to create an account, please notify him to do: **!create_account**")
            return
        balance = economy[str(server.id)][str(author.id)]["balance"]
        if amount > balance:
            await ctx.send(f":bangbang: **|** The amount you wanted to give to **{user.name}** is more than what you have in your account, pleas look below for stats.")
            await ctx.send(f":moneybag: **|** Amount in your account - **${balance}**/**{amount}**")
            return
        economy[str(server.id)][str(author.id)]["balance"] -= amount
        economy[str(server.id)][str(user.id)]["balance"] += amount
        economy[str(server.id)][str(user.id)]["networth"] += amount
        await ctx.send(f"You have given **{user.name}** **${amount}**! How nice of you...")
        with open("money.json", "w") as f:
            json.dump(economy,f,indent=4)

    @commands.command()
    async def stats(self, ctx, user: discord.Member = None):
        with open("money.json", "r") as f:
            economy = json.load(f)
        server = ctx.guild
        author = ctx.author
        if not str(author.id) in economy[str(server.id)]:
            await ctx.send(f":bangbang: **|** You need to create a account, you can do this by doing: **!create_account**")
            return
        if not user:
            server_users = economy[str(server.id)]
            balance = economy[str(server.id)][str(author.id)]["balance"]
            daily_streaks = economy[str(server.id)][str(author.id)]["daily-streak"]
            a = sorted(enumerate(economy[str(server.id)].items()), key=lambda x: x[1][1]["balance"],reverse=True)
            rank = [x[0]+1 for x in a if x[1][0] == str(author.id)][0]
            networth = economy[str(server.id)][str(author.id)]["networth"]
            msg = f"""
            Balance - **${balance}**
            Daily Streaks - **{daily_streaks} streaks**
            Networth - **${networth}**
            Rank for money - **#{rank}**
            """
            embed = discord.Embed(color=0xb55aec)
            embed.add_field(name=":signal_strength: Stats for you", value=msg, inline=False)
            await ctx.send(embed=embed)


    @commands.group()
    async def leaderboard(self, ctx):
        if not ctx.invoked_subcommand:
            msg = """
            See the leaders in this server!

``Economy|economy|money`` - See the **Top 10** leaders for money: **!leaderboard money**

``Networth|networth`` - See the **Top 10** leaders for the most money out of all: **!leaderboard networth**

``Daily_Streaks|daily_streaks|deaily-streaks`` - See the **Top 10** for the most daily streaks: **!leaderboard daily-streaks**
            """
            await ctx.send(f"Following leaderboard options:")
            await ctx.send(msg)

    @leaderboard.command(aliases=["Economy", "economy", "money"])
    async def moneys(self, ctx):
        with open("money.json", "r") as f:
            bank = json.load(f)
        server = ctx.guild
        if str(server.id) in bank:
            server_users = bank[str(server.id)]
            top = sorted([ (user,server_users[user]['balance']) for user in server_users], key=lambda x: x[1], reverse=True)
            mds = ["\U0001F947", "\U0001F948", "\U0001F949", "▫ ", "▫ "]
            top10 = top[:10]
            top = []
            for i,j in top10:
                x = await self.bot.get_user_info(i)
                top.append((str(x),f"${j}"))
            top = top + [("No User Found","0")]*10
            formatt = [f"``{rank} | `` {user_score[0]} -  **{user_score[1]}**" for rank, user_score in zip(range(1,11), top[:10])]
            for medal, rank, user_score in zip(mds, range(1,11), top[:10]):
                msg = "\n".join(formatt)
            await ctx.send(f"Top 10 for **Economy|economy|money**")
            await ctx.send(msg)

    @leaderboard.command(aliases=["networth", "Networth"])
    async def networths(self, ctx):
        with open("money.json", "r") as f:
            bank = json.load(f)
        server = ctx.guild
        if str(server.id) in bank:
            server_users = bank[str(server.id)]
            top = sorted([ (user,server_users[user]['networth']) for user in server_users], key=lambda x: x[1], reverse=True)
            mds = ["\U0001F947", "\U0001F948", "\U0001F949", "▫ ", "▫ "]
            top10 = top[:10]
            top = []
            for i,j in top10:
                x = await self.bot.get_user_info(i)
                top.append((str(x),f"${j}"))
            top = top + [("No User Found","0")]*10
            formatt = [f"``{rank} | `` {user_score[0]} -  **{user_score[1]}**" for rank, user_score in zip(range(1,11), top[:10])]
            for medal, rank, user_score in zip(mds, range(1,11), top[:10]):
                msg = "\n".join(formatt)
            await ctx.send(f"Top 10 for **Networth|networth**")
            await ctx.send(msg)

    @leaderboard.command(aliases=["Daily_Streaks", "daily_streaks", "daily-streaks"])
    async def daily_streak(self, ctx):
        with open("money.json", "r") as f:
            bank = json.load(f)
        server = ctx.guild
        if str(server.id) in bank:
            server_users = bank[str(server.id)]
            top = sorted([ (user,server_users[user]['daily-streak']) for user in server_users], key=lambda x: x[1], reverse=True)
            mds = ["\U0001F947", "\U0001F948", "\U0001F949", "▫ ", "▫ "]
            top10 = top[:10]
            top = []
            for i,j in top10:
                x = await self.bot.get_user_info(i)
                top.append((str(x),f"{j}"))
            top = top + [("No User Found","0")]*10
            formatt = [f"``{rank} | `` {user_score[0]} -  **{user_score[1]} streaks**" for rank, user_score in zip(range(1,11), top[:10])]
            for medal, rank, user_score in zip(mds, range(1,11), top[:10]):
                msg = "\n".join(formatt)
            await ctx.send(f"Top 10 for **Daily_Streaks|daily_streaks|daily-streaks**")
            await ctx.send(msg)

    @commands.command()
    async def gamble(self, ctx, amount: int = None):
        with open("money.json", "r") as f:
            economy = json.load(f)
        server = ctx.guild
        author = ctx.author
        choices = random.randint(0, 1)
        if not str(server.id) in economy:
            economy[str(server.id)] = {}
        if not str(author.id) in economy[str(server.id)]:
            await ctx.send(f":bangbang: **|** You need to create a account, you can do this by doing: **!create_account**")
            return
        balance = economy[str(server.id)][str(author.id)]["balance"]
        if amount > balance:
            await ctx.send(f":bangbang: **|** The amount you wanted to gamble is more than what you have in your account, pleas look below for stats.")
            await ctx.send(f":moneybag: **|** Amount in your account - **${balance}**/**{amount}**")
            return
        if choices == 0:
            economy[str(server.id)][str(author.id)]["balance"] += amount * 2
            economy[str(server.id)][str(author.id)]["networth"] += amount * 2
            await ctx.send(f"Yay! You gambled **${amount * 2}**!! :wink: You lucky duck :duck:")
        else:
            economy[str(server.id)][str(author.id)]["balance"] -= amount
            await ctx.send(f"Oof you lost.. loser lmao")
        with open("money.json", "w") as f:
            json.dump(economy,f,indent=4)

def setup(bot):
    bot.add_cog(Economy(bot))
