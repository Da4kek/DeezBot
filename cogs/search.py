import random
import discord
from discord.ext import commands
import requests
import datetime

class Search(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.command(helpinfo='Wikipedia summary', aliases=['w', 'wiki'])
  async def wikipedia(self,ctx, *, query: str=None):
    if query == None:
      await ctx.send("Give me a query to search")
    else:
        sea = requests.get(
            ('https://en.wikipedia.org//w/api.php?action=query'
            '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
            ).format(query)).json()['query']
        if sea['searchinfo']['totalhits'] == 0:
            await ctx.send('Sorry, your search could not be found.')
        else:
            for x in range(len(sea['search'])):
                article = sea['search'][x]['title']
                req = requests.get('https://en.wikipedia.org//w/api.php?action=query'
                                '&utf8=1&redirects&format=json&prop=info|images'
                                '&inprop=url&titles={}'.format(article)).json()['query']['pages']
                if str(list(req)[0]) != "-1":
                    break
            else:
                await ctx.send('Sorry, your search could not be found.')
                return
            article = req[list(req)[0]]['title']
            arturl = req[list(req)[0]]['fullurl']
            artdesc = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+article).json()['extract']
            lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'], "%Y-%m-%dT%H:%M:%SZ")
            embed = discord.Embed(title='**'+article+'**', url=arturl, description=artdesc, color=0x3FCAFF)
            embed.set_footer(text='Wiki entry last modified',
                            icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/',
                            icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.timestamp = lastedited
            await ctx.send('**Search result for:** ***"{}"***:'.format(query), embed=embed)

def setup(client):
  client.add_cog(Search(client))