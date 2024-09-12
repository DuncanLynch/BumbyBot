from rustplus import RustSocket
import asyncio
import time

class UserSocket:
    Socket = RustSocket()
    PlayerToken = "" 
    IP = ""
    Port = ""
    playerID = ""
    Messages = []

    def __init__(self, ip, playerid, pt, port):
        self.Socket = RustSocket(ip = ip, player_token=pt, steam_id=playerid, port=port)
        self.IP = ip, self.PlayerToken = pt, self.playerID = playerid, self.Port = port
        return
        

    async def SendMessage(self, message, name):
        if self.Socket == False or self.PlayerToken == "" or self.IP == "" or self.Port == "" or self.SteamID == "":
            return "Error: Socket Info not initalized."
        await self.Socket.send_team_message(name + " Sent an API message: " + message)
        return "Message sent."

    async def GetTeamMembers(self):
        info = await self.Socket.get_team_info()
        tlist = info.members
        resultantList = list()
        for i in range(len(tlist)):
            resultantList.append((tlist[i].name, tlist[i].is_online))
        return resultantList
    
    async def GetNewMessages(self):
        messages = await self.Socket.get_team_chat()
        if len(self.Messages) == len(messages):
            return False
        newmessages = messages[len(self.Messages):]
        self.Messages = messages
        return newmessages
    
    async def GetMap(self):
        map = await self.Socket.get_map(add_grid=True)
        return map
    
    #to add: listener for rustplus notifications, and security camera movement detection

        