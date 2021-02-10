import discord
from discord.ext import commands
import json

class levels(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_message(self, message):
    #await self.client.process_commands(message)
    return

def setup(client):
  client.add_cog(levels(client))