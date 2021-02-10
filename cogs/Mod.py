import discord
from discord.ext import commands
import json
import datetime
import time

date = datetime.datetime.now()

class Mod(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def prefix(self, ctx, *, prefix):
    with open('./data/prefixes.json', 'r') as f:
      prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('./data/prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)
  
    em = discord.Embed(title=f"Prefix Changed!", description=f":white_check_mark: Succesfully changed prefix to: **{prefix}**", color=discord.Color.green())
    await ctx.send(embed=em)

  @commands.command(name="kick", aliases=['kick_user'])
  async def kick_command(self, ctx, user : discord.Member, *, reason):
      await user.ban(reason=reason)

      embed = discord.Embed(color=discord.Color.red())
      embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
      embed.set_thumbnail(url=ctx.author.avatar_url)
      embed.add_field(name=f"KICK CASE | BY {ctx.author.mention}",
                      value=f"The user {user.mention} has been kiccked from the guild.\nREASON: **{reason}**\nMODERATOR: {ctx.author.mention}")
      await ctx.send(embed=embed)


  

  @commands.command()
  async def createchannel(self,ctx,channel):
    guild = ctx.guild
    embed = discord.Embed(title = "Success",description = f"Channel: {channel} has been created")
    if ctx.author.guild_permissions.manage_channels == True:
      await guild.create_text_channel(name = '{}'.format(channel))
      await ctx.send(embed=embed)
    else:
      embed_fail = discord.Embed(title = "Fail",description = f"Channel: {channel} couldn't be created because of permissions")
      await ctx.send(embed =embed_fail)
  
  @commands.has_permissions(manage_channels = True)
  @commands.command(name = "createvoice")
  async def createvoice(self,ctx,name,*,bitrate:int = None,user_limit:int = None):
      if bitrate == None:
          await ctx.send("Please give bitrate (recommended : 64)")
          if user_limit == None:
              await ctx.send("Please give user limit")
          else:
              return
      else:
          embed = discord.Embed(title = "Success",description ="Channel : {name} has been created!")
          await ctx.guild.create_voice_channel(name = name,bitrate = bitrate*1000,user_limit=user_limit)
          await ctx.send(embed = embed)

def setup(client):
  client.add_cog(Mod(client))