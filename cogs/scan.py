import discord
from discord.ext import commands
import pandas as pd
import logging
import os
logging.basicConfig(level = logging.INFO)
class Scan(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.Cog.listener
  async def on_ready(self):
    print("scan")
  @commands.Cog.listener
  async def on_message(self,message):
    if message.author == self.client.user:
      return
    elif message.content.startswith('deez '):
      cmd = message.content.split()[0].replace('deez',"")
      if len(message.content.split()) > 1:
        parameters = message.content.split()[1:]
      if cmd == "scan":
        data = pd.DataFrame(columns = ['content','time','author'])
        if len(message.channel_mention) > 0:
          channel =message.channel_mention[0]
        else:
          channel = message.channel
        if (len(message.content.split()) > 1 and len(message.channel_mentions) == 0) or len(message.content.split()) > 2:
          for parameter in parameters:
            if parameter == "help":
              answer = discord.Embed(title = "Format",description= "deez scan <channel> <number of messages>\n\n<channel>: **the channel you wish to scan**\n`<number of messages>`: **the number of messages you want to scan**\n\n",
              colour = message.author.color)
              await message.channel.send(embed = answer)
              return
            elif parameter[0] != "<":
              limit = int(parameter)
        else:
          limit = 100
        answer = discord.Embed(title ="Creating the Message's History",
                               description="Please wait until the messages are captured,it would be sent to your dms once completed",
                               colour = message.author.color)
        await message.channel.send(embed = answer)
        def is_command(self,message):
          if len(message.content) == 0:
            return False
          elif message.content.split()[0] == "deez scan":
            return True
          else:
            return False
        async for message in message.channel.history(limit = limit+1000):
          if message.author != self.client.user:
            if not is_command(message):
              data = data.append({'content':message.content,'time':message.created_at,"author":message.author.name},ignore_index = True)
            if len(data) == limit:
              break
        file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv"
        data.to_csv(file_location)
        answer = discord.Embed(title="Here's the file!",description = f"""It might have taken a while, but here is what you asked for.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{limit}**""",colour = 0x1a7794)
        await message.author.send(embed = answer)
        await message.author.send(file = discord.File(file_location,filename='data.csv'))
        os.remove(file_location)