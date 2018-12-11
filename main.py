import discord
import json
from discord.ext import commands


bot = commands.Bot(command_prefix="!")

owners = [
    499864547839049728, #aQ
    481270883701358602 #Savage
]

extensions = [
    "cogs.configs",
    "cogs.economy",
    "cogs.moderation"
]

@bot.event
async def on_ready():
    print("QuantumBot is ready to serve some good people!")
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as error:
            print(f"Error: {error}")

#Leveling up event (Gonna add some cool stuff ;) )

@bot.command()
async def reload(ctx, *, ext = None):
    if not ctx.author.id in owners:
        await ctx.send(f":bangbang: You need the ``developer`` permission. (Not a permission so don't try..)")
        return
    try:
        bot.unload_extension(ext)
        bot.load_extension(ext)
        await ctx.send(f"<a:yus:521452481612480512> Reloaded ``{ext}``")
    except Exception as error:
        await ctx.send(f":open_mouth: Error: ``{error}``")


bot.run(os.environ['TOKEN'])
