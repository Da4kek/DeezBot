import discord
from discord.ext import commands
import contextlib
import io
class Eval(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def eval(self,ctx,*,code):
        str_obj = io.StringIO()
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"```{e.__class__.__name__}: {e}```")
        await ctx.send(f'```{str_obj.getvalue()}```')

def setup(client):
    client.add_cog(Eval(client))