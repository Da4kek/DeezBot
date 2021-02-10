import discord
from discord.ext import commands
import json
class antinuke(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def antinuke(self, ctx, *, yesno):
    return

def setup(client):
  client.add_cog(antinuke(client))
  