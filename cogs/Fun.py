import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Esse comando não existe. Use `.help` para ver os comandos disponíveis.")
        else:
            await ctx.send("Ocorreu um erro ao processar o comando.")

    @commands.command()
    async def moeda(self, ctx):
        moeda = random.choice(["😀", "👑"]) # Cara ou coroa
        await ctx.message.add_reaction(moeda)
    
    @commands.command()
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)
        await ctx.send(f"🏓** | Pong!** ``{latency}ms``")


    @commands.command()
    async def print(self, ctx, *, message):
        try:
            await ctx.send(message)
            await ctx.message.delete()
        except:
             await ctx.send("É O QUE?")

    @commands.command()
    async def random(self, ctx, *, range = "1 10"):

        try:
            nums = range.split()
            
            num1 = int(max(nums))
            num2 = int(min(nums))
            

            await ctx.send(random.randint(num1, num2))
        except:
            await ctx.send("Tem alguma coisa errada aí")

    @commands.command()
    async def choice(self, ctx, *options):
        try:
            await ctx.send(random.choice(options))
        except:
             await ctx.send("Quais as opções?")
    
    @commands.command()
    async def math(self, ctx, *, expression):
        ### Ignorar strings com letras para não entrar no eval ###
        valid_expression = True
        for char in expression:
            if char.isalpha(): 
                valid_expression = False
                break
        # Checa se a expressão é válida pela flag #
        if valid_expression:
            try:
                await ctx.send(eval(expression))
            except:
                await ctx.send("A expressão tá errada")
        else:
            await ctx.send("Tem alguma coisa errada aí mano")


async def setup(bot):
    await bot.add_cog(Fun(bot))