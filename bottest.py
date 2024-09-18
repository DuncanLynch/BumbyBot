import asyncio
import discord
from discord.ext import commands
import time
import bot_commands


f = open("token.txt", "r")
DISCORD_API_KEY = f.read()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("bot ready")
    await bot.add_cog(bot_commands.RustCommands(bot))



bot.run(DISCORD_API_KEY)
