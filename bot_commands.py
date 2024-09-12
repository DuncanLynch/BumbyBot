from discord.ext import commands
import asyncio
from rustplus import RustSocket

class bot_commands(commands.Cog): 

    def __init__(self, bot):
        self.bot = bot
    
