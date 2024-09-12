import discord
from discord.ext import commands
import asyncio
import UserSocket

class RustCommands(commands.Cog): 

    UserData = {}

    def __init__(self, bot):
        #do mysql stuff later i dont feel like doing it now LMAOOOOOOOOOOOOOOOO
        self.bot = bot
    
    @commands.command()
    async def Pair(self, ctx, *arg):
        if self.UserData.get(ctx.author.name):
            await ctx.send("You already have a Socket connected, remove it first before pairing again.")
            return
        if len(arg) == 0:
            embeded_msg = discord.Embed(title="Link to your pairing details", description="\n",color=discord.Color.brand_red(),url="https://companion-rust.facepunch.com/login")
            embeded_msg.add_field(name="Pairing", value="In order to pair yourself with rustplus, go to the link at the top and link your steam account.", inline=True)
            embeded_msg.add_field(name = "Sending a proper request", value="Then, copy your: IP, playerID, playerToken, and port. Send another pairing request in the form !pair IP, playerID, playerToken, port ", inline=False)
            embeded_msg.set_footer(text="Responding to " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embeded_msg)
            return
        if len(arg) != 4:
            await ctx.send("Error: invalid parameters.")
            return
        print(arg)
        currSocket = UserSocket.UserSocket(arg[0], arg[1], arg[2], arg[3])
        self.UserData[ctx.author.name] = currSocket
        await ctx.send("Socket created. If further commands don't work, unpair and pair again in the proper form. If a server wipes or you change server you will have to pair again.")
        