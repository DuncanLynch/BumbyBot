import asyncio
import time
from rustplus import RustSocket


async def main():
    IP = "168.100.162.252"
    PORT = "28082"
    STEAMID = "76561198167575143"
    TOKEN = "-58625704"

    socket = RustSocket(IP, PORT, STEAMID, TOKEN)
    await socket.connect()
    info = await socket.get_team_info()
    tlist = info.members    
    # this block of code prints the online players
    for i in range(len(tlist)):
        if tlist[i].is_online:
            await socket.send_team_message(tlist[i].name + ", SteamID: " + str(tlist[i].steam_id))
    # this block grabs all messages        
    messages = await socket.get_team_chat()
    for i in range(len(messages)):
        print(messages[i].name + ": " + messages[i].message)

    await socket.disconnect()

asyncio.run(main())
