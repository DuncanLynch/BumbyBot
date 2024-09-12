from rustplus import RustSocket
import asyncio
import time

class UserSocket:
    Socket = RustSocket()
    PlayerToken = "" 
    IP = ""
    Port = ""
    SteamID = ""

    def __init__(self, pt, ip, port, steamid):
        self.Socket = RustSocket(ip = ip, player_token=pt, steam_id=steamid, port=port)
        self.IP = ip, self.PlayerToken = pt, self.SteamID = steamid, self.Port = port
        return
        

    async def SendMessage(self, message, name):
        if self.Socket == False or self.PlayerToken == "" or self.IP == "" or self.Port == "" or self.SteamID == "":
            return "Error: Socket Info not initalized."
        await self.Socket.send_team_message(name + " Sent an API message: " + message)
        return "Message sent."

    async def GetTeamMembers(self):
        info = await self.Socket.get_team_info
        tlist = info.members
        resultantList = list()
        for i in range(len(tlist)):
            resultantList.append((tlist[i].name, tlist[i].is_online))
        return resultantList
    
    #self.lists for current messages returning only the messages that didn't already exist.
    async def GetNewMessages(self):
        pass
        