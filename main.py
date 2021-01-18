#Imports
import discord
from discord.ext import commands
import json
import os
import datetime
import asyncio
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import aiohttp
import random
import reddit
import praw
#Variables

date = datetime.datetime.now()

with open("./data/config.json", 'r+') as f:
  data = json.load(f)
  token = data['token']
  ownerids = data['ownerids']
  default_prefix = data['default_prefix']

def get_prefix(client, message):

  with open("./data/prefixes.json", 'r+') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]


#Prefix
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=(get_prefix), intents=intents)

#Code
#Events
#on ready
@client.event
async def on_ready():
  print(f'''
Logged in as [{client.user}]
============================
ID: [{client.user.id}]
============================
Default Prefix: [{default_prefix}]
============================
Servers: [{len(client.guilds)}] 
============================
Members: [{len(set(client.get_all_members()))}]
============================
  ''')


#on_guild_join
@client.event
async def on_guild_join(guild):
  with open ("./data/prefixes.json", 'r') as f:
    prefixes = json.load(f)
  prefixes[str(guild.id)] = f'{default_prefix}'
  with open ("./data/prefixes.json", 'w') as f:
    json.dump(prefixes, f, indent=4)

# on guild remove
@client.event
async def on_guild_remove(guild):
  with open("./data/prefixes.json", 'r+') as f:
    prefixes = json.load(f)
  prefixes.pop(str(guild.id))
  with open("./data/prefixes.json", 'r+') as f:
    json.dump(prefixes, f, indent=4)

#on message
@client.event
async def on_message(message):
  if message.content.startswith('<@!800013428936278068>'):
    with open("./data/prefixes.json", 'r+') as f:
      data = json.load(f)
      prefix = data[f'{message.guild.id}']
    em = discord.Embed(title=f"My prefix is {prefix}")
    await message.channel.send(embed=em)
    return
  if isinstance(message.channel, discord.channel.DMChannel):
    return get_prefix
    return
  await client.process_commands(message)
#cog

@client.command()
async def load(ctx, *, extension):
  if ctx.author.id in ownerids:
    try:
      if extension == 'all':
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
      else:
        client.load_extension(f'cogs.{extension}')
      em = discord.Embed(title=f":white_check_mark: Loaded Cog(s)", description=f"Succesfully loaded {extension} cog(s)!", color=discord.Color.green())
      em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
      await ctx.send(embed=em)

    except Exception as error:
      em = discord.Embed(title=f":x: Error", description=f"Error: {error}", color=discord.Color.red())
      em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
      await ctx.send(embed=em)
      return
  else:
    em = discord.Embed(title=f":x: No permissions!", description=f"You don't have permissions to use this command!", color=discord.Color.red())
    em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
    await ctx.send(embed=em)

@client.command()
async def reload(ctx, *, extension):
  if ctx.author.id in ownerids:
    try:
      if extension == 'all':
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
      else:
        client.unload_extension(f'cogs.{extension}')
        await asyncio.sleep(0.5)
        client.load_extension(f'cogs.{extension}')
      await asyncio.sleep(1)
      em = discord.Embed(title=f":white_check_mark: Reloaded Cog(s)", description=f"Succesfully reloaded **{extension}** cog(s)!", color=discord.Color.green())
      em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
      await ctx.send(embed=em)

    except Exception as error:
      em = discord.Embed(title=f":x: Error", description=f"Error: {error}", color=discord.Color.red())
      em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
      await ctx.send(embed=em)
  
  else:
    em = discord.Embed(title=f":x: No permissions!", description=f"You don't have permissions to use this command!", color=discord.Color.red())
    em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
    await ctx.send(embed=em)

@client.command()
async def unload(ctx, *, extension):
  if ctx.author.id in ownerids:
    try:
      if extension == 'all':
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
      else:
        client.unload_extension(f'cogs.{extension}')
      em = discord.Embed(title=f":white_check_mark: Unloaded Cog(s)", description=f"Succesfully unloaded {extension} cog(s)!", color=discord.Color.green())
      em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
      await ctx.send(embed=em)

    except Exception as error:
      em = discord.Embed(title=f":x: Error", description=f"Error: {error}", color=discord.Color.red())
      em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
      await ctx.send(embed=em)
      return
  else:
    em = discord.Embed(title=f":x: No permissions!", description=f"You don't have permissions to use this command!", color=discord.Color.red())
    em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
    await ctx.send(embed=em)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def speak(ctx):
  data = open("./data/nfL6.json", 'r+')
  train = []
  for k,row in enumerate(data):
      train.append(row['question'])
      train.append(row['answer'])
  chatbot = ChatBot("Deez")
  trainer = ListTrainer(chatbot)
  trainer.train(train)
  while True:
      request = client.wait_for('message')
      response = chatbot.get_response(request)
      await ctx.send(request)
      await ctx.send(response)
      

 

client.run(token)

