import discord
from discord.ext import commands
import random
import reddit
import praw

def getMeme():
  reddit = praw.Reddit(client_id = "5T3myV5BQSWmvQ",
                  client_secret = "j2NeTcoFNEYyV6hCp6erdk1h3cO7vQ",
                  username = "nocopyrights101",
                  password = "Myindian@123",
                  user_agent = "NoahBot")  
  subreddit = reddit.subreddit("meme")   
  top = subreddit.top(limit=50)
  all_subs =[]
  for submission in top:
    all_subs.append(submission)
  random_sub = random.choice(all_subs)
  name = random_sub.title
  url = random_sub.url
  return name, url

class reddit(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(name="meme")
  async def _meme(self, ctx):
    if not hasattr(self.client, 'nextMeme'):
      self.client.nextMeme = getMeme()
    name, url = self.client.nextMeme
    embed = discord.Embed(title = name)
    embed.set_image(url=url)
    await ctx.send(embed=embed)
    self.client.nextMeme = getMeme()


def setup(client):
  client.add_cog(reddit(client))