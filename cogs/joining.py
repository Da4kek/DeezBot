import discord
import os
import time
import json
import typing as t
from pathlib import Path
from discord.ext import commands
from discord.utils import get
import asyncio
from dpymenus import Page,PaginatedMenu

class Guildjoin(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        Verified = await guild.create_role(name ="✔Verified",color = discord.Colour.green())
        Mute = await guild.create_role(name = "Muted",color = discord.Color.red())
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False)
        }
        login = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }
        logout = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Verified: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=True, embed_links=False, attach_files=False, read_message_history=True, external_emojis=True, manage_messages=False),
            Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
        }
        await guild.create_text_channel("✅verify",overwrites=overwrites)
        await guild.create_text_channel("💢log-in",overwrites=login)
        await guild.create_text_channel("🧨log-out",overwrites=logout)
        welcome = await guild.create_text_channel("📌welcome")
        embed = discord.Embed(color=discord.Colour.orange())
        embed.add_field(name="Deez Bot is Online 📱",value = "Deez is working on this server! \n\n 💢Bot prefix: Custom Prefix **Mention him to reveal his prefix**(```Use prefix command to change for this server```)")
        await welcome.send(embed = embed)
        time.sleep(30)
        await welcome.delete(reason = "Auto delete function")

def setup(client):
    client.add_cog(Guildjoin(client))

    