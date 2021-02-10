import discord
from discord.ext import commands
import json
import asyncio
from discord.utils import get
from discord.ext.commands import has_permissions

class AntiSpam(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.command(name = "antispam",usage = "<true/false>",description="Enable or disable antispam")
    @has_permissions(administrator=True)
    @commands.guild_only()
    async def antispam(self,ctx,antispam):
        antispam = antispam.lower()
        if antispam == "true":
            with open("./data/configuration.json",'r') as config:
                data = json.load(config)
                data['antispam'] = True
                newdata = json.dump(data,indent=4,ensure_ascii=False)
            embed = discord.Embed(title = f"**ANTI SPAM ENABLED**",description = f"Anti spam was enabled.",color = discord.Colour.red())
        else:
            with open("./data/configuration.json","r") as config:
                data = json.load(config)
                data['antispam'] = True
                newdata = json.dump(data,indent = 4,ensure_ascii=False)
            embed = discord.Embed(title = f"**ANIT SPAM DISABLED**",description = f"Anto spam was disabled.",color = discord.Colour.greyple())
        await ctx.channel.send(embed= embed)
        with open("./data/configuration.json","w") as config:
            config.write(newdata)
        
def setup(client):
    client.add_cog(AntiSpam(client))
