import discord
import os 
from pathlib import Path
from discord.ext import commands
from discord.utils import get
import asyncio
from dpymenus import Page,PaginatedMenu
import time

class Joinleave(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self,ctx):
        try:
            channel = get(ctx.guild.channels,name = "💢log-in")
            member_count = len(ctx.guild.members)
            embed = discord.Embed(color = discord.Color.green())
            embed.add_field(name = "💢Log in Message!",value = f"{ctx.mention} has joined the server!! \nTotal member count: {member_count}")
            embed.set_footer(text = f"Timestamp: {time.ctime()}")
            await channel.send(embed = embed)
        except:
            return None
        
    @commands.Cog.listener()
    async def on_member_remove(self,ctx):
        try:
            channel = get(ctx.guild.channels,name ='🧨log-out')
            member_count = len(ctx.guild.members)
            embed = discord.Embed(color=discord.Color.red())
            embed.add_field(name ="🧨Log out Message!",value = f"{ctx.mention} has left the server!! \nTotal member count: {member_count}")
            embed.set_footer(text=f"Timestamp: {time.ctime()}")
            await channel.send(embed = embed)
        except:
            return None
def setup(client):
    client.add_cog(Joinleave(client))