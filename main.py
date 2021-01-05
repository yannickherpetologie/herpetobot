import discord
import os
import requests
from discord.ext.commands import Bot
import sqlite3
import re
import datetime

client = Bot(command_prefix="!")
token = os.getenv("DISCORD_BOT_TOKEN")

""" Section Recherche """
@client.command(pass_context=True)
async def scholar(ctx, *, arg):
    """ direct open scholar with parameters as research (current year -4 for filter) """
    year = datetime.datetime.now().year - 4
    parameters = arg.replace(' ', '+')
    url = f"https://scholar.google.com/scholar?as_ylo={year}&q={parameters}&hl=fr&as_sdt=0,5"
    await ctx.send(url)

@client.command(pass_context=True)
async def inaturalist(ctx, *, arg):
    """ look data of iNaturalist """
    parameters = arg.replace(' ', '%20')
    url = f"https://www.inaturalist.org/search?q={parameters}"
    await ctx.send(url)

@client.command(pass_context=True)
async def repdb(ctx, *, arg):
    """ look data of iNaturalist """
    parameters = arg.replace(' ', '+')
    url = f"https://reptile-database.reptarium.cz/search?search={parameters}&submit=Search"
    await ctx.send(url)


@client.command(pass_context=True)
async def amphibianworldsearch(ctx, *, arg):
    """ search an amphibian species on amphibianoftheworld """
    parameters = arg.replace(' ', '%20')
    url = f"https://amphibiansoftheworld.amnh.org/amphib/basic_search?basic_query=ranitomeya&stree=&stree_id={parameters}"
    await ctx.send(url)

@client.command(pass_context=True)
async def amphibianworld(ctx):
    """ return url of amphibiansoftheworld """
    url = f"https://amphibiansoftheworld.amnh.org/"
    await ctx.send(url)

@client.command(pass_context=True)
async def newamphibiansp(ctx):
    """ return url of new amphibian sp zotero """
    url = f"https://www.zotero.org/groups/2232608/new_amphibian_species/items/6W9AMET5/library"
    await ctx.send(url)

@client.command(pass_context=True)
async def ranitomeya(ctx):
    url = f"http://www.ranitomeya.org"
    await ctx.send(url)

@client.command(pass_context=True)
async def dendrobates(ctx):
    url = f"http://www.dendrobates.org"
    await ctx.send(url)

@client.command(pass_context=True)
async def dendrocall(ctx):
    url = f"http://www.dendrocall.com"
    await ctx.send(url)

@client.command(pass_context=True)
async def video(ctx, *, arg):
    parameters = arg.replace(' ', '+')
    url = requests.get(f"http://www.youtube.com/results?search_query={parameters}")
    video_ids = re.findall(r"watch\?v=(\S{11})", url.text)

    await ctx.send(f"https://www.youtube.com/watch?v={video_ids[0]}")
""" /Section Recherche """

""" Section Divers """
@client.command(pass_context=True)
async def zotero(ctx):
    """ return url of new amphibian sp zotero """
    url = f"https://www.zotero.org/groups/2593419/herpetologie/library"
    await ctx.send(url)

@client.command(pass_context=True)
async def yblog(ctx):
    """ return url of new amphibian sp zotero """
    url = f"https://yannickherpetologie.blogspot.com/"
    await ctx.send(url)

@client.command(pass_context=True)
async def pt(ctx):
    await ctx.send("https://www.planete-terrario.com")

@client.command(pass_context=True)
async def apv(ctx):
    await ctx.send("https://www.asian-pitvipers.com")

@client.command(pass_context=True)
async def tch(ctx):
    await ctx.send("https://www.terrariophilie.ch")
""" /Section Divers"""

""" Section Humour """
@client.command(pass_context=True)
async def humour(ctx):
    conn = sqlite3.connect('herpetobot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT phrase FROM humour ORDER BY RANDOM() LIMIT 1;")
    row = cursor.fetchone()
    cursor.close()
    await ctx.send(f"*{row[0]}*")

@client.command(pass_context=True)
async def addhumour(ctx, *, arg):
    conn = sqlite3.connect('herpetobot.db')
    cursor = conn.cursor()
    req = f"INSERT INTO humour(phrase) VALUES({arg})"
    cursor.execute(req)
    conn.commit()
    cursor.close()
    await ctx.send("Message d'humour ajouté avec succès !")
""" /Section Humour"""


@client.command(pass_context=True)
async def aide(ctx):
    """ return url of new amphibian sp zotero """
    message = """
    ```
    -----------------------------------------Aide--------------------------------------------------------------------
    !aide                       Affiche ce message
    
    -----------------------------------------Recherche --------------------------------------------------------------
    !scholar args               Renvoie l'url de google scholar avec les arguments (filtrer automatique à 4 ans max)
                                    utilisation: !scholar pantherophis guttatus reproduction
    !inaturalist args           Renvoie l'url de iNaturlist avec les arguments:
                                    utilisation: !inaturalist Echis pyramidum
    !repdb args                 Renvoie l'url de reptile-database avec les arguments:
                                    utilisation: !repdb Morelia viridis
    !video args                 Renvoie la première vidéo youtube des args
                                    utilisation: !video Bufotes viridis calling
    ```
    """
    message2 = """
    ```
    -----------------------------------------Amphibien --------------------------------------------------------------
    !amphibianworldsearch args  Renvoie l'url de amphibiansoftheworld avec les arguments:
                                    utilisation: !amphibianworldsearch Ranitomeya imitator
    !amphibianworld             Renvoie l'url de amphibiansoftheworld
    !newamphibiansp             Renvoie l'url de Zotero sur la découverte de nouvelle espèce
    !ranitomeya                 Renvoie l'adresse de ranitomeya
    !dendrobates                Renvoie l'adresse de dendrobates
    !dendrocall                 Renvoie l'adresse de dendrocall
    
    -----------------------------------------Divers -----------------------------------------------------------------
    !zotero                     Renvoie le zotero de yannick.
    !pt                         Renvoie l'adresse de planete-terrario
    !apv                        Renvoie l'adresse d'asian-pitvipers
    !tch                        Renvoie l'adresse de terrariophilie suisse
    !yblog                      Renvoie l'adresse du blog de yannick
    ```"""
    await ctx.send(message)
    await ctx.send(message2)

@client.event
async def on_ready():
    print(f"{client.user.name} connecté\r\n")
    print(f"{client.user.name} est connecté aux serveurs suivant: ")
    for server in client.guilds:
        print(server.name)

print("Connection en cours...")
client.run(token)