import discord
from discord.ext import commands
import asyncio
from typing import Optional
from pathlib import Path
from discord.utils import get
from dpymenus import Page,PaginatedMenu
import time

class TicketSystem(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(name = "openticket")
    async def open_ticket(self,ctx):
        Mute = get(ctx.guild.roles,name="muted")
        overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True),
        Mute: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False, manage_messages=False),
    }
        ticket_role = await ctx.guild.create_role(name =f"!ticket-{ctx.author}")
        ticket_r = get(ctx.guild.roles,name=f"{ticket_role}")
        ticket_channel = await ctx.guild.create_text_channel(f'❗ticket-{ctx.author}', overwrites=overwrites)
        await ctx.author.add_roles(ticket_r)
        embed = discord.Embed(color = discord.Color.gold())
        embed.set_author(name = ctx.author,icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"Timestamp: {time.ctime()}\nInvoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name = "DEEZ TICKET",value = f"{ctx.author.mention} your ticket has been created: {ticket_channel}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def closeticket(self,ctx,member:discord.Member,roles):
        r_ole = get(ctx.guild.roles,name = roles)
        await member.remove_roles(member.guild.roles,name=roles)
        await ctx.channel.delete(reason="Ticket Closed")
        await roles.delete()
        

def setup(client):
    client.add_cog(TicketSystem(client))