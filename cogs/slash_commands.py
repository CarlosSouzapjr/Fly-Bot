import discord
import io
import random

from discord import app_commands
from discord.ext import commands

from discord import File
from easy_pil import Editor, load_image_async, Font

class Slash(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    

    ##### INFO #####

    @app_commands.command(name="roles", description="Listar seus cargos com cores.")
    async def roles(self, interaction: discord.Interaction):
        
        user = interaction.user
        
        if len(user.roles) - 1 > 0:  # Removendo o "@everyone"
            roles = [r for r in user.roles if r != "@everyone"]
            response = ""
            embed = discord.Embed(title="**Seus cargos são:**", colour=discord.Colour.blurple())
            for r in roles:
                if r.name !=  "@everyone":
                    response += f"<@&{r.id}>\n"
            embed.add_field(name= "", value=response, inline=False)
                        
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Você ainda não tem cargos nesse servidor.")

    @app_commands.command(name="profile", description="Mostra o perfil de um usuário.")
    async def profile(self, interaction: discord.Interaction, mention: str = ""):
        ### Transformando o mention em user id ###
        mention = mention.replace("<", "").replace(">", "").replace("@", "").replace("!", "")

        try:
            user_id = int(mention)
            user = interaction.guild.get_member(user_id)
        except Exception as e:
            user = interaction.user  # O próprio usuário que executou o comando
        
        # Carrega e redimensiona a imagem do avatar
        avatar_bytes = await load_image_async(user.avatar.url)
        avatar_image = Editor(avatar_bytes).resize((600, 600))  # Redimensiona para 600x600

        # Converte a imagem redimensionada para um objeto BytesIO
        with io.BytesIO() as image_binary:
            avatar_image.save(image_binary, file_format="PNG")
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename="avatar.png")

            # Cria um embed e adiciona a imagem redimensionada
            embed = discord.Embed(title=f"Perfil de {user.name}", colour=discord.Colour.blurple())
            embed.set_footer(text=f"Pedido por {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.set_image(url="attachment://avatar.png")

            # Envia o embed com a imagem redimensionada
            await interaction.response.send_message(embed=embed, file=file) 
    
    


    

async def setup(bot):
    await bot.add_cog(Slash(bot))