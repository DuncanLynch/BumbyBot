import asyncio
import time
from rustplus import RustSocket


async def main():
    IP = "185.248.134.151"
    PORT = "28035"
    STEAMID = "76561198167575143"
    TOKEN = "1572579393"


    socket = RustSocket(IP, PORT, STEAMID, TOKEN)
    await socket.connect()
    
    await socket.send_team_message("Hello")

    await socket.disconnect()

asyncio.run(main())
