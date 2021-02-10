import asyncio
import discord
import os
import time
import string
from pathlib import Path
from discord.ext import commands
from discord import Embed, Color
from discord.utils import get
from dpymenus import Page, PaginatedMenu
from PIL import Image, ImageFont, ImageDraw
from random import choice

class Verification(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content.startswith("deez verify"):
            role = get(message.guild.roles,name ="✔Verified")
            image = Image.new("RGBA",(500,500),'white')
            word = ''.join(choice(string.ascii_letters) for _ in range(10))
            font = ImageFont.truetype('./data/arial.ttf',75)
            w,h = font.getsize(word)
            draw = ImageDraw.Draw(image)
            draw.text(((500 - w) /2, (500 - h) /2), word, font=font, fill='black')
            image.save('./data/captcha.png')
            await message.channel.send(file = discord.File("./data/captcha.png"))

            embed = discord.Embed(color = message.author.color)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text = f"TimeStamp: {time.ctime()}\nInvoked by {message.author}",icon_url=message.author.avatar_url)
            embed.add_field(name = "Verification!",value = f"{message.author.mention} to verify your self on the server, solve the captcha that I've sent. Write in the chat the correct word to get verified.")
            await message.channel.send(embed =embed)

            def _check(member : discord.Member):
                if message.author.id == member.author.id:
                    return message.content
            
            captcha = str(word.split(" "))
            captcha = "".join(captcha)

            msg = await self.client.wait_for('message', timeout=120.0, check=_check)

            if msg.content == str(captcha.strip("[]''")):
                embed = Embed(color=discord.Color.green())
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text=f"Timstamp: {time.ctime()}\nInvoked by {message.author}", icon_url=message.author.avatar_url)
                embed.add_field(name="✅ VERIFY SYSTEM",
                                value=f"{message.author.mention} you got correctly verified. You can now interact on the server. Write messages, join vocals and much more.")
                
                await message.channel.send(embed=embed)
                await message.author.add_roles(role)
            
            else:
                embed = Embed(color=discord.Color.red())
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text=f"Timstamp: {time.ctime()}\nInvoked by {message.author}", icon_url=message.author.avatar_url)
                embed.add_field(name=":x: VERIFY SYSTEM",
                                value=f"{message.author.mention} you didn't pass the Captcha verification. Please re-try.")
                
                await message.channel.send(embed=embed)
def setup(client):
    client.add_cog(Verification(client))