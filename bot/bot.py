"""
A module that contains all commands of the Discord bot oriented to simple roleplaying with friends
"""

import hikari
import lightbulb
import os
from General import *


"""
First, configure the bot according to your needs, example:

bot = lightbulb.BotApp(
    token='Your bot's Token',
    default_enabled_guilds=(Your guild id)
    )

To see your guild id, go to Discord, configuration->advanced->developer mode, and turn to on,
    after right click in your guild and select copy ID
"""

bot = lightbulb.BotApp()

adminsNames = ["Atlantox#0325"]
#A list of the names and discriminator of the users with permisson to use specific commands

#--------------------------------------- PERMISSON DECORATOR ---------------------------------------

def RequirePermisson(command):
    """
    A decorator, put just before the commands you considere necessary

    param function command: The command that only admins will can call    
    """

    async def CheckAdmin(ctx):
        author = f"{ctx.author.username}#{ctx.author.discriminator}"
        global adminsNames
        if author in adminsNames:
            await command(ctx)
        else:
            await ctx.respond("Tu no puede, ere pobre, no tiene permiso")
    return CheckAdmin


#--------------------------------------- DICES COMMANDS ---------------------------------------

@bot.command
@lightbulb.option('rep', 'se pueden repetir?', type=bool, default=True)
@lightbulb.option('min', 'mínimo', type=int)
@lightbulb.option('max', 'máximo', type=int)
@lightbulb.option('times', 'número de dados', type=int)
@lightbulb.command('launch_dice', 'Lanza X dados de X caras')
@lightbulb.implements(lightbulb.SlashCommand)
async def launch_dice(ctx):
    await ctx.respond(
        LaunchDice(
            ctx.options.min,
            ctx.options.max,
            ctx.options.times,
            ctx.options.rep))


@bot.command
@lightbulb.command('simple_dice', 'Lanza un dado de 6 caras')
@lightbulb.implements(lightbulb.SlashCommand)
async def simple_dice(ctx):
    """
    The bot launch a simple dice of 6 faces
    """
    await ctx.respond(LaunchDice(1,6,1))


#--------------------------------------- SENDING LOCAL FILES COMMANDS ---------------------------------------

@bot.command
@lightbulb.option('image_name', 'nombre de la imágen', type=str)
@lightbulb.command('send_image', 'Envía una imágen')
@lightbulb.implements(lightbulb.SlashCommand)
async def send_image(ctx):
    """
    The bot respond with a image, be sure that you internet is sufficent to upload that image in less of 3 seconds
        or the command will cancel up.

    param str imate_name: The image name in /images folder, with the extension included (example.png)
    """
    path = os.getcwd()
    path = path.replace('\\', '/')
    path = f"{path}/bot/images/{ctx.options.image_name}"
    f =hikari.File(path)
    print(path)
    await ctx.respond(f)


#--------------------------------------- INVENTORY MANAGEMENT ---------------------------------------

@bot.command
@lightbulb.option('profession', 'Profesión del personaje', type=str)
@lightbulb.option('name', 'Nombre del personaje', type=str)
@lightbulb.command('init_character_inventory', 'Resetea el inventario de un personaje según su clase')
@lightbulb.implements(lightbulb.SlashCommand)
@RequirePermisson
async def init_character_inventory(ctx):
    await ctx.respond(InitCharacterInventory(ctx.options.name, ctx.options.profession))


@bot.command
@lightbulb.option('name', 'Nombre del personaje', type=str)
@lightbulb.command('get_inventory', 'Muestra el inventario de un personaje')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_inventory(ctx):
    await ctx.respond(GetInventory(ctx.options.name))


@bot.command
@lightbulb.option('value', 'Número de items a agregar o quitar', type=int)
@lightbulb.option('item', 'Nombre del item a modificar', type=str)
@lightbulb.option('name', 'Nombre del personaje', type=str)
@lightbulb.command('modify_inventory', 'Modifica el inventario de un personaje')
@lightbulb.implements(lightbulb.SlashCommand)
@RequirePermisson
async def modify_inventory(ctx):
    await ctx.respond(ModifyIventory(ctx.options.name, ctx.options.item, ctx.options.value))


@bot.command
@lightbulb.option('name', 'Nombre del personaje', type=str)
@lightbulb.command('delete_character_inventory', 'Borra el inventario de un personaje')
@lightbulb.implements(lightbulb.SlashCommand)
@RequirePermisson
async def delete_character_inventory(ctx):
    await ctx.respond(DeleteCharacter(ctx.options.name))


#--------------------------------------- CHARACTERS AND STATISTICS MANAGEMENT ---------------------------------------

@bot.command
@lightbulb.command('get_characters', 'Obtiene las estadísticas de un personaje')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_characters(ctx):
    await ctx.respond(GetCharacters())


@bot.command
@lightbulb.option('name', 'Nombre del personaje', type=str)
@lightbulb.option('stat', 'Estadística a modificar', type=str)
@lightbulb.option('value', 'Cantidad', type=int)
@lightbulb.command('add_stat', 'Actualiza un stat de un personaje')
@lightbulb.implements(lightbulb.SlashCommand)
@RequirePermisson
async def add_stat(ctx):
    await ctx.respond(AddStad(ctx.options.name, ctx.options.stat, ctx.options.value))


@bot.command
@lightbulb.option('stad_name', 'Nombre de la estadística', type=str)
@lightbulb.command('delete_stad', 'Borra la estadística de todos los personajes')
@lightbulb.implements(lightbulb.SlashCommand)
@RequirePermisson
async def delete_stad(ctx):
    await ctx.respond(DeleteStad(ctx.options.stad_name))


#--------------------------------------- RUNNING BOT ---------------------------------------

bot.run()