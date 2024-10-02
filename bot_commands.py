import discord
from discord.ext import commands, tasks
import asyncio
import UserSocket
import time
import io
import sqlite3

class RustCommands(commands.Cog): 

    Messages = []
    Socket = UserSocket
    GuildData = {
        "testSuperExamplethatwillneverbecaughtbyadiscordservername": {
            "ActiveTeamChat": False,
            "RemoveTeamChat":  False,
        }
    }
    UserData = {}
        


    def __init__(self, bot):
        #do mysql stuff later i dont feel like doing it now LMAOOOOOOOOOOOOOOO
        self.bot = bot
    
    @commands.command()
    async def pair(self, ctx, *arg):
        if self.UserData.get(ctx.author.name):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You already have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        if len(arg) == 0:
            embeded_msg = discord.Embed(title="Link to your pairing details", description="\n",color=discord.Color.blue(),url="https://companion-rust.facepunch.com/login")
            embeded_msg.add_field(name="Pairing", value="In order to pair yourself with rustplus, go to the link at the top and link your steam account.", inline=True)
            embeded_msg.add_field(name = "Sending a proper request", value="Then, copy your: IP, playerID, playerToken, and port. Send another pairing request in the form !pair IP, playerID, playerToken, port ", inline=False)
            embeded_msg.set_footer(text="Responding to " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embeded_msg)
            return
        if len(arg) != 4:
            await ctx.send("Error: invalid parameters.")
            return
        currSocket = UserSocket.UserSocket(ip=str(arg[0]), playerid=str(arg[1]), pt=str(arg[2]), port=str(arg[3]))
        await currSocket.connect()
        self.UserData[ctx.author.name] = currSocket

        embed = discord.Embed(title="Socket Connected", description="",color=discord.Color.brand_green())
        embed.add_field(name="",value="Your socket has been created. If no messages appear then you created the socket incorrectly and must unpair before pairing correctly again.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def unpair(self, ctx):
        if not(self.UserData.get(ctx.author.name)):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        self.UserData[ctx.author.name].disconnect()
        await self.EndTeamMessages(ctx)
        self.UserData[ctx.author.name] = False
        embed = discord.Embed(title="Socket Cleared", description="",color=discord.Color.brand_red())
        embed.add_field(name="",value="You no longer have an active Socket paired.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
        

    @commands.command()
    async def msg(self, ctx, *arg):
        message = ""
        if not(self.UserData.get(ctx.author.name)):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        for i in range(len(arg)):
            message += arg[i] + " "
        socket = self.UserData.get(ctx.author.name)
        try:
            await socket.SendMessage(message, ctx.author.name)
            print("attempted to message")
        except:
            embed = discord.Embed(title="Message Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="Message failed to send, websocket seems to be disconnected.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Message Sent", description="",color=discord.Color.brand_green())
        embed.add_field(name="",value="Message sent. If it doesn't appear in game, then your socket is expired.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
        return
     
    @commands.command()
    async def teamlist(self, ctx):
        if not(self.UserData.get(ctx.author.name)):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        socket = self.UserData.get(ctx.author.name)
        try:
            tlist = await socket.GetTeamMembers()
        except:
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="Websocket seems to be disconnected.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        l = ""
        for i in range(len(tlist)):
            if tlist[i][1]:
                l+= "|" + str(tlist[i][2]) + "| " + tlist[i][0] + " /Online/ :white_check_mark:\n"
            else:
                l+= "|" + str(tlist[i][2]) + "| " + tlist[i][0] + " /Offline/ :x:\n"
        embed = discord.Embed(title="Current List of Team Members", description="",color=discord.Color.brand_green())
        embed.add_field(name="",value=l)
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    #make this work across multiple servers
    @commands.command()
    async def GrabTeamMessages(self, ctx):
        if not(self.UserData.get(ctx.author.name)):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        
        if not(self.GuildData.get(ctx.guild.name)):
            self.GuildData[ctx.guild.name] = {
            "ActiveTeamChat": False,
            "RemoveTeamChat": False,
            "TeamChatChannel": "",
        }

        if self.GuildData.get(ctx.guild.name).get("ActiveTeamChat"):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You already have an active teamchat in a channel.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return 
        
        embed = discord.Embed(title="Messages Set Up", description="",color=discord.Color.brand_green())
        embed.add_field(name="",value="Team Messages will be posted in this channel. If it doesn't appear, then your socket is invalid.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

        self.GuildData[ctx.guild.name]["ActiveTeamChat"] = True
        self.GuildData[ctx.guild.name]["RemoveTeamChat"] = False
        self.GuildData[ctx.guild.name]["TeamChatChannel"] = ctx.channel

        socket = self.UserData.get(ctx.author.name)
        
        

        while not(self.GuildData[ctx.guild.name]["RemoveTeamChat"]):
            messagelist = await socket.GetNewMessages()
            if messagelist:
                for i in range(len(messagelist)):
                    m = "[" + str(messagelist[i].time) + "]" + " " + messagelist[i].name + ": " + messagelist[i].message
                    await ctx.send(m)
            await asyncio.sleep(1)

        return


    @commands.command()
    async def EndTeamMessages(self, ctx):
        if not(self.UserData.get(ctx.author.name)):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return

        if not(self.GuildData.get(ctx.guild.name)) or not(self.GuildData.get(ctx.guild.name).get("ActiveTeamChat")):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active teamchat in a channel.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return 


        if not(ctx.channel == self.GuildData.get(ctx.guild.name).get("TeamChatChannel")):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You must enter this command in the channel with the team chat active.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return 

        embed = discord.Embed(title="Messages deactivated", description="",color=discord.Color.brand_green())
        embed.add_field(name="",value="Team Messages will no longer be posted in this channel.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

        self.GuildData[ctx.guild.name]["ActiveTeamChat"] = False
        self.GuildData[ctx.guild.name]["RemoveTeamChat"] = True

    @commands.command()
    async def map(self, ctx):
        if not(self.UserData.get(ctx.author.name)):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return

        sock = self.UserData.get(ctx.author.name)

        try:
            GameMap = await sock.GetMap()
        except:
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="Map failed to generate.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return

        with io.BytesIO() as image_binary:
            GameMap.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
        return

    @commands.command()
    async def promote(self, ctx, *arg):
        if not(self.UserData.get(ctx.author.name)):
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="You do not have an active Socket paired.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        
        if len(arg) != 1:
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="Invalid parameters.\nUsage: !promote <steamID>")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        try:
            self.Socket.PromoteToLeader(arg[0])
        except:
            embed = discord.Embed(title="Command Failed", description="",color=discord.Color.brand_red())
            embed.add_field(name="",value="Promotion failed.")
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
            return
        
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="All Commands", description="",color=discord.Color.brand_green())
        embed.add_field(name="!pair",value="Usage: !pair IP PlayerId PlayerToken Port\nPairs the rust socket and saves it for access while your credentials are valid. If the other functions don't work after the socket successfully pairs, then check your credentials, unpair, and try again.")
        embed.add_field(name="!unpair",value="Removes the current paired websocket and resets all connected channels.")
        embed.add_field(name="!msg",value="Usage: !msg [message]\nSends a message in game through teamchat. It takes the form {[name] sent an API Message: [message]}.")
        embed.add_field(name="!promote",value="Usage: !promote [SteamID]\nGiven that the one who calls the command is the team leader, promotes the given player to team leader.")
        embed.add_field(name="!teamlist",value="Grabs the current list of team members and their status as online or offline.")
        embed.add_field(name="!GrabTeamMessages",value="Binds a updating list of team messages to the channel it is sent into.")
        embed.add_field(name="!EndTeamMessages",value="Unbinds the channel with the team messages. Must be called in the same channel.")
        embed.add_field(name="!map",value="Grabs the current server map with the grids, icons, events, and vending machines.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        ctx.send(embed)
        return

            