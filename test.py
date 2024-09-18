import asyncio
import time
from rustplus import RustSocket, CommandOptions, Command, ServerDetails
IP = "185.248.134.151"
PORT = "28035"
STEAMID = "76561198167575143"
TOKEN = "1572579393"
details = ServerDetails(IP, PORT, STEAMID, TOKEN)
options = CommandOptions(prefix="")
socket = RustSocket(IP, PORT, STEAMID, TOKEN)

@Command(details)
async def hi(command: Command):
    await socket.send_team_message("Hi")

async def main():
    


    
    await socket.connect()
    
    messages = await socket.get_team_chat()

    await socket.disconnect()

asyncio.run(main())
