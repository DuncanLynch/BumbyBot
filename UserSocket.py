from rustplus import RustSocket, ServerDetails, CommandOptions, ChatCommand, Command
import asyncio
import time

class UserSocket:
    options = CommandOptions(prefix="!")
    Sdetails = ServerDetails
    Socket = RustSocket
    PlayerToken = "" 
    IP = ""
    Port = ""
    playerID = ""
    Messages = []

    #Initializes the UserSocket with the RustSocket object.
    def __init__(self, ip, playerid, pt, port):
        self.Sdetails = ServerDetails(ip = ip, player_token=pt, player_id=playerid, port=port)
        self.Socket = RustSocket(server_details=self.Sdetails)
        self.IP = ip
        self.PlayerToken = pt
        self.playerID = playerid
        self.Port = port    
        return

    #Connects the current Socket
    async def connect(self):
        await self.Socket.connect()
        return
    
    #Disconnects the current Socket
    async def disconnect(self):
        await self.Socket.disconnect()
        return
    

    #Sends a message in the Rust Teamchat, returning the status of the message relating to sent/unsent.
    async def SendMessage(self, message, name):
        if self.Socket == False or self.PlayerToken == "" or self.IP == "" or self.Port == "" or self.playerID == "":
            return "Error: Socket Info not initalized."
 
        print("User socket attempting to message")
        await self.Socket.send_team_message(name + " Sent an API message: " + message)

        return "Message sent."

    #Returns a list of tuples of the current members on the Socket player's team'sname, status, and steamid.
    async def GetTeamMembers(self):
        info = await self.Socket.get_team_info()
        tlist = info.members
        resultantList = list()
        for i in range(len(tlist)):
            resultantList.append((tlist[i].name, tlist[i].is_online, tlist[i].steam_id))
        return resultantList
    
    #Returns a list of message objects that do not current exist in self.Messages, aka. The new messages.
    async def GetNewMessages(self):
        messages = await self.Socket.get_team_chat()
        if len(self.Messages) == len(messages):
            return False
        newmessages = messages[len(self.Messages):]
        self.Messages = messages
        return newmessages
    
    #Returns an image of the ingame map with the grid, icons, events, and vending machines added on.
    async def GetMap(self):
        map = await self.Socket.get_map(add_grid=True, add_icons=True,add_events=True,add_vending_machines=True)
        return map
    
    #Takes a steamID as a parameter, and given that the one calling it is the current TeamLeader, 
    #it will promote the player with the associated SteamId to leader
    async def PromoteToLeader(self, STEAMID):
        await self.Socket.promote_to_team_leader(steamid=STEAMID)

        