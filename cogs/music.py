import asyncio
import json
import discord
import youtube_dl
import random
from discord.ext import commands
import datetime

date = datetime.datetime.now()

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel=None):
        """Joins a voice channel"""
        if channel == None:
          em = discord.Embed(title=f"Join Command", description=f"Usage: `{ctx.prefix}join (channel name)`", color=random.randint(0, 0xFFFFF))
          em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
          await ctx.send(embed=em)
          return

        if ctx.voice_client is not None:
          return await ctx.voice_client.move_to(channel)
        
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f'Connected to: {channel}'
        await ctx.send(embed=em, delete_after=5)
        await channel.connect()
        await ctx.message.delete()

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""
        player = await YTDLSource.from_url(url, loop=self.client.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f'Now playing: {player.title}'
        await ctx.send(embed=em)
     

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        with open(f"./data/premium.json", 'r+') as f:
          data = json.load(f)
          members = data['members']
          if ctx.message.author.id in members:
            if ctx.voice_client is None:
              return await ctx.send("Not connected to a voice channel.")

            ctx.voice_client.source.volume = volume / 100
            em = discord.Embed(color=random.randint(0, 0xFFFFFF))
            em.description = f'Changed volume to {volume}%'
            await ctx.send(embed=em, delete_after=5)
            await ctx.message.delete()
          else:
            em = discord.Embed(title=f":x: No permissions!", description=f"You aren't a premium user. You can't use this command!", color=discord.Color.red())
            await ctx.send(embed=em)

    @commands.command(aliase=["disconnect", "leave"])
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        DJRole = discord.utils.get(ctx.guild.roles, name="DJ")
        if ctx.voice_client is not None:
          if ctx.author.voice:
            if DJRole in ctx.author.roles:
              pass
            else:
              em = discord.Embed(title=f":x: No permissions!", description=f"You need {DJRole.mention} to use this command!", color=discord.Color.red())
              em.set_footer(text=f"Today at {date:%I}:{date:%M} {date:%p}")
              await ctx.send(embed=em)
              return
          else:
            await ctx.send("You are not connected to a voice channel.")
            return            
        em = discord.Embed(color=random.randint(0, 0xFFFFFF))
        em.description = f'Succesfully Stopped The Current Song And Disconnected My Self From The Voice Channel'
        await ctx.send(embed=em, delete_after=5)
        await ctx.voice_client.disconnect()
        await ctx.message.delete()
    

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(client):
    client.add_cog(Music(client))