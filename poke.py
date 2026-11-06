import os
import random

import discord
import requests
from discord.ext import commands

from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print(f"Você logou com {bot.user}")


#! 1. bot lendo uma imagem
# @bot.command()
# async def mem(ctx):
#     with open(
#         "IMAGES/mem1.png", "rb"
#     ) as f:  # rb = ready binary, lido como bytes e não texto
#         picture = discord.File(f)
#     await ctx.send(file=picture)


#! 2. leitura de imagem aleatória
@bot.command()
async def mem(ctx):
    img_name = random.choice(os.listdir("IMAGES"))
    with open(f"IMAGES/{img_name}", "rb") as f:
        picture = discord.File(f)

    await ctx.send(file=picture)


#!3 puxando imagens de uma API de patos
def get_duck_image_url():
    url = "https://random-d.uk/api/random"
    res = requests.get(url)
    data = res.json()
    return data["url"]


@bot.command("duck")
async def duck(ctx):
    """Sempre que a requisição de pato é chamada, o programa chama a função **get_duck_image_url**."""
    image_url = get_duck_image_url()
    await ctx.send(image_url)


#!4 usando a API DE POKEMON


def get_pokemon_image_url():
    # Escolhe um Pokémon aleatório pelo número
    pokemon_id = random.randint(1, 1025)

    # Endpoint da PokéAPI
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"

    # Faz a requisição para a API
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Converte a resposta para um dicionário Python
    data = response.json()

    # Pega o nome do Pokémon
    pokemon_name = data["name"]

    # Pega a imagem oficial; usa a imagem padrão como alternativa
    image_url = (
        data["sprites"]["other"]["official-artwork"]["front_default"]
        or data["sprites"]["front_default"]
    )

    return pokemon_name, image_url


@bot.command(name="poke")
async def poke(ctx):
    try:
        pokemon_name, image_url = get_pokemon_image_url()

        if image_url is None:
            await ctx.send("Não encontrei a imagem desse Pokémon!")
            return

        # Cria uma mensagem com a imagem incorporada
        embed = discord.Embed(
            title=f"Pokémon: {pokemon_name.capitalize()}", color=discord.Color.red()
        )

        embed.set_image(url=image_url)

        await ctx.send(embed=embed)

    except requests.RequestException:
        await ctx.send("Não consegui acessar a PokéAPI. Tente novamente!")


bot.run(TOKEN)
