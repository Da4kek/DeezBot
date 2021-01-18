import discord
from discord.ext import commands
import json
from typing import Optional
from discord import Embed,Member
import datetime
import random

date = datetime.datetime.now()

with open("./data/config.json", 'r+') as f:
  data = json.load(f)
  ownerids = data['ownerids']
  default_prefix = data['default_prefix']
  version = data['version']


class Info(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  async def botinfo(self, ctx):
    em = discord.Embed(title=f"**__Bot Info:__**", color=random.randint(0, 0xFFFFF))
    em.set_thumbnail(url=ctx.guild.me.avatar_url)
    em.add_field(name=f":small_blue_diamond: | **__Version:__**", value=f"[`{version}`]", inline=False)
    em.add_field(name=f":books: | **__Library:__**", value=f"[`discord.py`]", inline=False)
    em.add_field(name=f":keyboard: | **__Creators:__**", value=f"[`- RandomDudk81#8537`]\n[`- RealNoah#0011`]", inline=False)
    em.add_field(name=f":busts_in_silhouette: | **__Servers & Users:__**", value=f"Total Servers: [`{len(self.client.guilds)}`]\nTotal Users: [`{len(set(self.client.get_all_members()))}`]", inline=False)
    em.add_field(name=":question: | **__Prefix:__**", value=f"Default: [`!`]\nServer: [`{ctx.prefix}`]", inline=False)
    em.add_field(name=":bar_chart: | **__Ping:__**", value=f"Ping: [`{round(self.client.latency * 1000)}`]", inline=False)
    em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}.")
    await ctx.send(embed=em)

  @commands.command()
  async def whois(self,ctx,user:Optional[Member]):
    user = user or ctx.author
    rolesinuser = ""
    for role in user.roles:
      rolesinuser += f"{role.mention}, "
      
    embed = Embed(title="User Information",
                  color=user.color,
                  timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=user.avatar_url)
    fields = [("Name",str(user),True),
              ("ID",user.id,True),
              ("Bot",user.bot,True),
              ("Top role",user.top_role.mention,True),              
              ("Status",str(user.status).title(),True),
              ("Created Discord at",user.created_at.strftime("%d/%m/%Y %H:%M:%S"),True),
              ("Joined Server at",user.joined_at.strftime("%d/%m/%Y %H:%M:%S"),True),
              ("Boosted Server",bool(user.premium_since),True),
              ("Roles", rolesinuser, True)]
    for name,value,inline in fields:
      embed.add_field(name = name,value = value,inline=inline)
    await ctx.send(embed=embed)
  
  

def setup(client):
  client.add_cog(Info(client))