import discord
from discord.ext import commands
import asyncio
import UserSocket

class bot_commands(commands.Cog): 

    UserData = {}

    def __init__(self, bot):
        #do mysql stuff later i dont feel like doing it now LMAOOOOOOOOOOOOOOOO
        self.bot = bot
    
    @commands.command()
    async def Pair(self, ctx, arg):
        if arg is None:
            embeded_msg = discord.Embed(title="Link to your pairing details", description="\n",color=discord.Color.brand_red(),url="https://companion-rust.facepunch.com/login")
            embeded_msg.add_field(name="Pairing", value="In order to pair yourself with rustplus, go to the link at the top and link your steam account.", inline=True)
            embeded_msg.add_field(name = "Sending a proper request", value="Then, copy your: IP, playerID, playerToken, and port. Send another pairing request in the form !pair IP, playerID, playerToken, port ", inline=False)
            embeded_msg.set_footer(text="Responding to " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embeded_msg)
        args = arg.split(", ")
        if len(args) != 4:
            await ctx.send("Error: invalid parameters.")
        currSocket = UserSocket(args[0], args[1], args[2], args[3])
        self.UserData[ctx.user.name] = currSocket
        