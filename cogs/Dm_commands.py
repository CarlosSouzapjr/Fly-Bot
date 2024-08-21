import discord
from discord.ext import commands

class Dm(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Esse comando não existe. Use `.help` para ver os comandos disponíveis.")
        else:
            await ctx.send("Ocorreu um erro ao processar o comando.")

    @commands.command()
    async def hello(self, ctx):
        user = ctx.message.author.name
        embed = discord.Embed(
            title= "Hey there!",
            description=f"Hello {user}! :grin:"
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def dmme(self, ctx):
        user = ctx.message.author

        await user.send(f"Hey yo {ctx.author.name}")


async def setup(bot):
    await bot.add_cog(Dm(bot))