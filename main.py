from credentials import *

import asyncio
import discord
import json

from random import randint

class Frase (object):

    def __init__(self, jsonRow):
        self.frase = str(jsonRow['frase'])
        self.contexto = str(jsonRow['contexto'])
        self.fuente = str(jsonRow['fuente'])

    def descripcion(self):

        if self.contexto == '' and self.fuente == '':
            descripcion = ''

        elif self.contexto != '' and self.fuente == '':
            descripcion = 'Hablando sobre {}'.format(self.contexto)

        elif self.contexto == '' and self.fuente != '':
            descripcion = 'Escuchado en {}'.format(self.fuente)

        else:
            descripcion = 'Hablando sobre {} y escuchado en {}'.format(self.contexto, self.fuente)

        return descripcion

DEBUG = True

client = discord.Client()

@client.event
async def on_ready():
    print('Logueado como')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):

    # Ignoramos mensajes de bots
    if message.author.bot: return False

    if message.content.startswith('!frase'):

        # Cargamos el archivo JSON en memoria
        with open('frases.json', encoding='utf-8') as frases:

            # Creamos un objeto JSON en base al archivo frases.json
            data = json.load(frases)

            # Generamos un indice random desde 0 hasta el tamaño del JSON
            index = randint(0, len(data['frases']) - 1)

            # Agarramos la frase en ese indice
            f = Frase(data['frases'][index])

            # Hacemos un embeded message con la informacion de esa frase
            mensaje = discord.Embed(title=f.frase, description=f.descripcion(), colour=0x3E41E0)
            mensaje.set_author(name='Dieguito dice', icon_url=client.user.default_avatar_url)

            # Y lo mandamos
            await client.send_message(message.channel, embed=mensaje)

    if message.content.startswith('!dieguitobot'):

        desc = '''
        **dieguitobot**

        Repositorio: https://github.com/sqrg/dieguitobot

        Agradecimientos:
            * Miguel Angel Faldutti por recopilar tantas frases
            * Checkpoint por ser quienes son <3
        '''

        mensaje = discord.Embed(description=desc, colour=0x3E41E0)
        await client.send_message(message.channel, embed=mensaje)

if DEBUG:
    token = TOKEN_TEST
else:
    token = TOKEN

client.run(token)
