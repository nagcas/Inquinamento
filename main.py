# IMPORT: librerie che utilizzeremo nel programma

import random  # Sceglie un elemento casuale da una lista
import os  # Permette di lavorare con cartelle e file
import requests  # Permette di comunicare con le API tramite Internet
import discord  # Libreria per creare bot Discord

from consigli import consigli  # Libreria personalizzata consigli
from sfide import sfide  # Libreria personalizzata sfide
from riciclo import riciclo  # Libreria personalizzarta riciclo

from discord.ext import commands  # Permette di creare comandi come $somma

from settings import *  # Importa le impostazioni, incluso il TOKEN

# Configuriamo gli intent, cioè gli eventi che il bot può ricevere.
intents = discord.Intents.default()
intents.message_content = True  # Permette di leggere i messaggi per i comandi


# Creiamo il bot e scegliamo il prefisso dei comandi: $
bot = commands.Bot(command_prefix=settings['PREFIX'], intents=intents)

comandi = '''
        🌱 **GreenBot — Comandi disponibili**

        `$consiglio` → visualizza un consiglio
        `$sfida` → visualizza la sfida del giorno
        `$smaltimento carta` → informazioni sullo smaltimento
        `$info` → mostra questa guida
        
        Categorie: carta, plastica, vetro, alluminio,
        pile, organico, farmaci, elettronica, vestiti, olio.
        '''

# Questa funzione viene eseguita quando il bot si collega a Discord.
@bot.event
async def on_ready():
    print(f'Bot online: {bot.user}')
    
    channel_id = settings['CHANNEL']
    
    channel = bot.get_channel(channel_id)

    # Mostriamo i nomi dei file presenti nella cartella images.
    print('\nFile presenti nella cartella images:')
    print(os.listdir('images'))
    print(comandi)
    
    image = os.listdir('images')
    
    with open(f'images/{image[0]}', 'rb') as file:
        picture = discord.File(file)
    
    if channel is not None:
        await channel.send(
            '🌍 Ciao! Sono GreenBot, il tuo alleato per proteggere il pianeta!', file=picture)
        
        await channel.send(comandi)


# COMANDO 1: $consiglio
@bot.command()
async def consiglio(ctx):
    messaggio = random.choice(consigli)
    await ctx.send(f'Consiglio ecologico: {messaggio}')


# COMANDO 2: $sfida
@bot.command()
async def sfida(ctx):
    sfida = random.choice(sfide)
    await ctx.send(f'Sfida del giorno: {sfida}')


# COMANDO 3: $smaltimento carta
@bot.command()
async def smaltimento(ctx, category: str):
    if category in riciclo:
        print(riciclo[category])
        await ctx.send(f'{category}: {riciclo[category]}')
    else:
        print(f'{category}: Categoria non valida!!!')
        await ctx.send(f'{category}: Categoria non valida!!!')


# COMANDO 4: $info
@bot.command()
async def info(ctx):
    await ctx.send(comandi)


# Avviamo il bot utilizzando il token presente nelle impostazioni.
bot.run(settings['TOKEN'])
