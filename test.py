import asyncio
import time
from rustplus import RustSocket, ServerDetails, CommandOptions, ChatCommand, Command
IP = "45.88.230.93"
PORT = "28093"
STEAMID = 76561198167575143
TOKEN = 817066201


async def main():
    server_details = ServerDetails(IP, PORT, STEAMID, TOKEN)
    socket = RustSocket(server_details)

    options = CommandOptions(prefix="!")


    
    await socket.connect()

    m = await socket.get_team_chat()
    time.sleep(.5)
    await socket.send_team_message("this should be the extraneous chat message!")

    n = await socket.get_team_chat()

    print(len(m))
    print(len(n))
    
    x = n[len(m):]
    print(x[0].message)

    await socket.disconnect()

asyncio.run(main())