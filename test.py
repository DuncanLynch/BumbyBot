import asyncio
import time
from rustplus import RustSocket, ServerDetails, CommandOptions, ChatCommand, Command
import sqlite3
IP = "45.88.230.93"
PORT = "28093"
STEAMID = 76561198167575143
TOKEN = 817066201


async def main():
    #test
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM UserData WHERE username = ?", ("hypadeficit",))
    print(cursor.fetchall())

asyncio.run(main())