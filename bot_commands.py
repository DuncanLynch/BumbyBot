import discord
from discord.ext import commands, tasks
import asyncio
import UserSocket
import time
import io

class RustCommands(commands.Cog): 

    Socket = UserSocket
    GuildData = {}
    UserData = {
        "testSuperExamplethatwillneverbecaughtbyadiscordservername": {
            "ActiveTeamChat": False,
            "RemoveTeamChat":  False,
        }
    }


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
        await currSocket.SendMessage("I just connected a websocket using Bumbybot!", ctx.author.name)
        self.UserData[ctx.author.name] = currSocket

        embed = discord.Embed(title="Socket Connected", description="",color=discord.Color.brand_green())
        embed.add_field(name="",value="Your socket has been created. If no messages appear then you created the socket incorrectly and must unpair before pairing correctly again.")
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def message(self, ctx, *arg):
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
                l+= tlist[i][0] + " /Online/ :white_check_mark:\n"
            else:
                l+= tlist[i][0] + " /Offline/ :x:\n"
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
        await socket.disconnect()

        while not(self.GuildData[ctx.guild.name]["RemoveTeamChat"]):
            await socket.connect()
            try:
                
                messagelist = await socket.GetNewMessages()
            except:
                print("Error occured: Breaking from the messages list.")
                break
            for i in range(len(messagelist)):
                m = "[" + str(messagelist[i].time) + "]" + " " + messagelist[i].name + ": " + messagelist[i].message
                await ctx.send(m)
            await socket.disconnect()
            time.sleep(5)
        await socket.connect()
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
        6

        with io.BytesIO() as image_binary:
            GameMap.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
        return

            

            