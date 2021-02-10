import discord
from discord.ext import commands
import asyncio

class ModMail(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self,message):
        sent_users = []
        
        if message.guild:
            return
        if message.author == self.client.user:
            return
        if message.author.id in sent_users:
            return
        modmail_channel = self.client.get_channel("798824651681824768")
        embed = discord.Embed(color = message.author.color)
        embed.set_author(name=f"Deez ModMail System", icon_url="https://i.ytimg.com/vi/HBA1Ny_QK6I/hqdefault.jpg")
    
        embed.add_field(name='Report a member:', value=f"React with 1️⃣ if you want to report a member.")
        embed.add_field(name='Report a Staff Member:', value=f"React with 2️⃣ if you want to report a Staff Member.")
        embed.add_field(name='Warn Appeal:', value=f"React with 3️⃣ if you would like to appeal a warning.")
        embed.add_field(name='Question:', value=f"React with 4️⃣ if you have a question about our moderation system or the server rules.")
        embed.set_footer(text="DEEZ | Modmail")
        msg = await message.author.send(embed=embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
        await msg.add_reaction("4️⃣")
        sent_users.append(message.author.id)
        try:
            def check(reaction,user):
                return user == message.author and str(reaction.emoji) in ['1️⃣','2️⃣','3️⃣','4️⃣']
            reaction,user = await self.client.wait_for("reaction_add",timeout = 60,check=check)
            if str(reaction.emoji) == "1️⃣":
                embed = discord.Embed(color=0x00FFFF)
                embed.set_author(name=f"Deez MoadMail System", icon_url="https://i.ytimg.com/vi/HBA1Ny_QK6I/hqdefault.jpg")
                embed.add_field(name='How to Report:', value="Send the ID of the person you are reporting and attach add a screen shot of them breaking a rule (can be ToS or a server rule).")
                embed.set_footer(text="DEEZ | Report a member ")
                await message.author.send(embed=embed)
                message = await self.client.wait_for("message", timeout=60, check=lambda m: m.channel == message.channel and m.author == message.author)
                embed = discord.Embed(title=f"{message.content}", color=0x00FFFF)
                await modmail_channel.send(embed=embed)
        except asyncio.TimeoutError:
            await message.delete()

def setup(client):
    client.add_cog(ModMail(client))