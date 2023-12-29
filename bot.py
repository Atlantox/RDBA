"""
A module that contains all commands of the Discord bot oriented to simple roleplaying with friends
"""

import hikari
import lightbulb
from general import *

if __name__ == '__main__':
    config = {}
    # Get settings from settings.txt
    with open('settings.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            split = line.split('=')
            header, value = split[0].strip(), split[1].strip()
            config[header] = value
        f.close()

    guilds_id = config['DEFAULT_GUILDS'].split(',')
    print(guilds_id)
    guilds_id = [int(id.strip()) for id in guilds_id]

    admins = config['ADMIN_NAMES'].split(',')
    admins = [id.strip() for id in admins]

    # Settings constants
    BOT_TOKEN = config['BOT_TOKEN']
    DEFAULT_GUILDS = guilds_id
    ADMIN_NAMES = admins
    DEBUG = bool(int(config['DEBUG']))

    bot = lightbulb.BotApp(
        token= BOT_TOKEN,
        default_enabled_guilds= DEFAULT_GUILDS
        )

    #--------------------------------------- PERMISSON DECORATOR ---------------------------------------

    def RequirePermisson(command):
        """
        A decorator, put just before the commands you considere necessary

        param function command: The command that only admins will can call    
        """

        async def CheckAdmin(ctx):
            author = f"{ctx.author.username}#{ctx.author.discriminator}"
            global ADMIN_NAMES
            if author in ADMIN_NAMES:
                await command(ctx)
            else:
                await ctx.respond("No tienes permiso para usar ese comando")
        return CheckAdmin


    #--------------------------------------- DICES COMMANDS ---------------------------------------

    @bot.command
    @lightbulb.option('rep', 'se pueden repetir?', type=bool, default=True)
    @lightbulb.option('times', 'número de dados', type=int)
    @lightbulb.option('max', 'máximo', type=int)
    @lightbulb.option('min', 'mínimo', type=int)
    @lightbulb.command('launch_dice', 'Lanza X dados de X caras')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def launch_dice(ctx):
        await ctx.respond(
            Dice.launch_dice(
                ctx.options.min,
                ctx.options.max,
                ctx.options.times,
                ctx.options.rep))


    @bot.command
    @lightbulb.command('d6', 'Lanza un dado de 6 caras')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def d6(ctx):
        """
        The bot launch a simple dice of 6 faces sending an image
        """

        f =hikari.File(Dice.get_dice_path(randrange(1,7)))
        await ctx.respond(f)


    @bot.command
    @lightbulb.command('d20', 'Lanza un dado de 20 caras')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def d20(ctx):
        await ctx.respond(f'{Dice.launch_dice(1,20,1)}')

        
    @bot.command
    @lightbulb.option('roll', 'Ejemplo: 2d10', type=str)
    @lightbulb.command('roll', 'Lanza el o los dados indicados')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def roll(ctx):
        await ctx.respond(f'{Dice.launch_many_dices(ctx.options.roll)}')


    #--------------------------------------- SENDING LOCAL FILES COMMANDS ---------------------------------------

    @bot.command
    @lightbulb.option('file_name', 'nombre del archivo', type=str)
    @lightbulb.command('send_file', 'Envía un archivo (con extensión)')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def send_file(ctx):
        """
        The bot respond with a file, be sure that you internet is sufficent to upload that file in less of 3 seconds
            or the command will cancel up.

        param str file_name: The file name in /bot_files folder, with the extension included (example.png)
        """
        path = os.getcwd()
        path = path.replace('\\', '/')
        path = f"{path}/bot_files/{ctx.options.file_name}"
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
        await ctx.respond(character_manager.initialize_character_inventory(ctx.options.name, ctx.options.profession))


    @bot.command
    @lightbulb.option('name', 'Nombre del personaje', type=str)
    @lightbulb.command('get_inventory', 'Muestra el inventario de un personaje')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def get_inventory(ctx):
        await ctx.respond(character_manager.get_inventory(ctx.options.name))


    @bot.command
    @lightbulb.option('value', 'Número de items a agregar o quitar', type=int)
    @lightbulb.option('item', 'Nombre del item a modificar', type=str)
    @lightbulb.option('name', 'Nombre del personaje', type=str)
    @lightbulb.command('modify_inventory', 'Modifica el inventario de un personaje')
    @lightbulb.implements(lightbulb.SlashCommand)
    @RequirePermisson
    async def modify_inventory(ctx):
        await ctx.respond(character_manager.modify_inventory(ctx.options.name, ctx.options.item, ctx.options.value))


    @bot.command
    @lightbulb.option('name', 'Nombre del personaje', type=str)
    @lightbulb.command('delete_character', 'Borra un personaje del todo')
    @lightbulb.implements(lightbulb.SlashCommand)
    @RequirePermisson
    async def delete_character(ctx):
        await ctx.respond(character_manager.delete_character(ctx.options.name))


    #--------------------------------------- CHARACTERS AND STATISTICS MANAGEMENT ---------------------------------------

    @bot.command
    @lightbulb.command('get_characters', 'Obtiene las estadísticas de los personajes')
    @lightbulb.implements(lightbulb.SlashCommand)
    async def get_characters(ctx):
        await ctx.respond(character_manager.get_characters())


    @bot.command
    @lightbulb.option('name', 'Nombre del personaje', type=str)
    @lightbulb.command('get_stads', 'Obtiene las estadísticas de un personaje')
    @lightbulb.implements(lightbulb.SlashCommand)
    @RequirePermisson
    async def get_stads(ctx):
        await ctx.respond(character_manager.get_stads(ctx.options.name))


    @bot.command
    @lightbulb.option('name', 'Nombre del personaje', type=str)
    @lightbulb.option('stad', 'Estadística a modificar', type=str)
    @lightbulb.option('value', 'Cantidad', type=int)
    @lightbulb.command('add_stad', 'Actualiza una estadística de un personaje')
    @lightbulb.implements(lightbulb.SlashCommand)
    @RequirePermisson
    async def add_stad(ctx):
        await ctx.respond(character_manager.add_stad(ctx.options.name, ctx.options.stad, ctx.options.value))


    @bot.command
    @lightbulb.option('stad_name', 'Nombre de la estadística', type=str)
    @lightbulb.command('delete_stad', 'Borra la estadística de todos los personajes')
    @lightbulb.implements(lightbulb.SlashCommand)
    @RequirePermisson
    async def delete_stad(ctx):
        await ctx.respond(character_manager.delete_stad(ctx.options.stad_name))


    #--------------------------------------- RUNNING BOT ---------------------------------------

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event):
        print('\nEncendiendo bot\n')
        character_manager.initialize_database()
        if DEBUG:
            print('\n****** PROFESIONES ******')
            professions = character_manager.get_professions()
            for profession in professions:
                print(profession)

            print('\n****** PERSONAJES ******')
            print(character_manager.get_characters().replace('*',''), '\n')

    bot.run()