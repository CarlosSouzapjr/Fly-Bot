import discord
import io

from discord.ext import commands
from discord import File
from easy_pil import Editor, load_image_async, Font

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Esse comando não existe. Use `.help` para ver os comandos disponíveis.")
        else:
            await ctx.send("Ocorreu um erro ao processar o comando.")
        
    # @commands.command()
    # async def getchannel(self, ctx):
    #     # Get the channels names
    #     channels = [c.name for c in ctx.guild.channels]
    #     print(channels)

    @commands.command()
    async def roles(self, ctx):
        user = ctx.message.author
        
        if len(user.roles) - 1 > 0:  # Removendo o "@everyone"
            roles = [r for r in user.roles if r != "@everyone"]
            response = ""
            embed = discord.Embed(title="**Seus cargos são:**", colour=discord.Colour.blurple())
            for r in roles:
                if r.name !=  "@everyone":
                    response += f"<@&{r.id}>\n"
            embed.add_field(name= "", value=response, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Você ainda não tem cargos nesse servidor.")

    @commands.command()
    async def profile(self, ctx, mention: str = ""):
        ### Transformando o mention em user id ###
        mention = mention.replace("<","").replace(">","").replace("@","").replace("!","")


        try:
            user_id = int(mention)        
            user = ctx.guild.get_member(user_id)
            
        except Exception as e:
            user = ctx.message.author
            
        avatar_bytes = await load_image_async(user.avatar.url)
        avatar_image = Editor(avatar_bytes).resize((600, 600))  # Redimensiona para 600x600

        # Converte a imagem redimensionada para um objeto BytesIO
        with io.BytesIO() as image_binary:
            avatar_image.save(image_binary, file_format="PNG")
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename="avatar.png")

            # Cria um embed e adiciona a imagem redimensionada
            embed = discord.Embed(title=user, colour=discord.Colour.blurple())
            embed.set_footer(text=f"Pedido por {ctx.message.author.name}", icon_url=ctx.message.author.avatar.url)
            embed.set_image(url="attachment://avatar.png")

            # Envia o embed com a imagem redimensionada
            await ctx.send(embed=embed, file=file)  

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member = "", *, reason="No reason provided"):
        if user == "":
            await ctx.send(f"Quem é o meliante?! 😡")
        else:
            user_id = user.id
            try:
                # Expulsa o usuário e cria o embed
                await user.kick(reason=reason)
                kick_embed = discord.Embed(
                    title=f":boot: Kicked {user.name}!",
                    description=f"Reason: {reason}\nBy: {ctx.author.mention}"
                )

                # Apaga a mensagem original do comando
                await ctx.message.delete()

                # Envia o embed no canal e para o usuário
                await ctx.channel.send(embed=kick_embed)

                userName = self.client.get_user(int(user_id))

                await userName.send(embed=kick_embed)
            
            except Exception as e:
                pass

    @kick.error
    async def kick_error(self, ctx, error):
        # Adiciona uma verificação para saber exatamente o tipo de erro
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para usar este comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Usuário inválido. Por favor, mencione um membro válido.")
        else:
            # Debug: log do erro exato
            await ctx.send(f"Erro inesperado: {error}")

    
    @commands.command()
    async def ban(self, ctx, user: discord.User):
          pass
    
    @commands.command()
    async def unban(self, ctx, user: discord.User):
          pass
    
    @commands.command()
    async def clear(self, ctx, user: discord.User):
          pass
    
    @commands.command()
    async def renamechannel(self, ctx, user: discord.User):
          pass

async def setup(bot):
    await bot.add_cog(Moderation(bot))