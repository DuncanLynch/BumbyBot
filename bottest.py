import asyncio
import discord
from discord.ext import commands
import time


DISCORD_API_KEY = None

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(),)

@bot.command(name="yo")
async def send_embed(ctx):
    embeded_msg = discord.Embed(title="Link to your pairing details", description="\n",color=discord.Color.brand_red(),url="https://companion-rust.facepunch.com/login")
    embeded_msg.add_field(name="Pairing", value="In order to pair yourself with rustplus, go to the link at the top and link your steam account.", inline=True)
    embeded_msg.add_field(name = "Sending a proper request", value="Then, copy your: IP, playerID, playerToken, and port. Send another pairing request in the form !pair (IP, playerID, playerToken, port) ", inline=False)
    embeded_msg.set_footer(text="Responding to " + ctx.author.name, icon_url=ctx.author.avatar)
    await ctx.send(embed=embeded_msg)

@bot.event
async def on_ready():
    print("bot ready")



bot.run(DISCORD_API_KEY)
