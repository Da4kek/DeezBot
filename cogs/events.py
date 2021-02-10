import discord
from discord.ext import commands
import json
import random

class events(commands.Cog):
  def __init__(self, client):
    self.client = client

def setup(client):
  client.add_cog(events(client))