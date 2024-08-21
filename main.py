import os
import dotenv
import discord

from configs import *
from discord.ext import commands
from discord import File
from easy_pil import Editor, load_image_async, Font


dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="Bzzz Bzzz"))
    await load_extensions()
    await bot.tree.sync()

    print("Bão? 😎")
    print(bot.user.name)
    print(bot.user.id)
    print("-------------------")


@bot.event
async def on_member_join(member): # Usuário entrou no server
    canal = bot.get_channel(1272728958407807058) # ID do canal da mensagem

    background = Editor("./images/welcome.png")
    profile_image = await load_image_async(str(member.avatar.url))

    profile = Editor(profile_image).resize((size, size)).circle_image()###

    poppins = Font.poppins(size=font_size, variant="bold")

    poppins_small = Font.poppins(size=font_size//2, variant="light")

    background.paste(profile, (pos_x, pos_y))
    background.ellipse((pos_x, pos_y), size, size, outline="white", stroke_width=5)

    background.text((text_x, text_y), f"WELCOME TO {member.guild.name}", color="white", font=poppins, align="center")
    background.text((text_x, small_text_y), f"{member.name}", color="white", font=poppins_small, align="center")

    file = File(fp=background.image_bytes, filename="welcome.png")
    await canal.send(f"Bem-vindo ao {member.guild.name} {member.mention}!")
    await canal.send(file=file)

@bot.event
async def on_member_remove(member): # Usuário saiu no server
    canal = bot.get_channel(1272728958407807058) # ID do canal da mensagem
    msg = f"{member.mention} foi de base 😢"
    await canal.send(msg)


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")



bot.run(TOKEN)