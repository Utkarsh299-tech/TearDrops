# TODO - transfer, casino, etc commands


import aiohttp
import time
import random

import os
import ssl
import discord
from discord.ext import commands, tasks
from itertools import cycle

from pymongo import MongoClient


# temp->

# modules for wiki and wolfram queries
# import wolframalpha
# import requests

# Standard modules

# TOKEN, MONGO URI are env-vars
from utils import get_environment_variable


DISCORD_BOT_TOKEN = get_environment_variable("DISCORD_BOT_TOKEN")
MONGO_CONNECTION_STRING = get_environment_variable("MONGO_CONNECTION_STRING")


DB_CLIENT = MongoClient(MONGO_CONNECTION_STRING)
db = DB_CLIENT.get_database('users_db')

print(db.list_collection_names())
timelast = 0
timecheck = 0
ssl._create_default_https_context = ssl._create_unverified_context


# intents (new discord feature to limit bots to certain bucket events)
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# NOTE- The initial version of the bot used TinyDB, but I've migrated to MongoDB (still considering sql tho)

# client pointer for API-reference
client = commands.Bot(command_prefix='qq ',
                      case_insensitive=True, intents=intents)

# discord.py has an inbuilt help command, which doesn't look good''
client.remove_command('help')


# status-change-cycle(The bot changes presence after a few mins.)
STATUS = cycle([
    "qq help | :(",
    "with your heart"
    "in tears",
    "with tears",
    "with ",
    "I'm so sad",
    "with your tears...",
    "with your feelings",
    "with sparkles"])


ls_cog = ['cogs.fun_cog',
          'cogs.ping_cog',
          'cogs.help_cog',
          'cogs.coffee_cog',
          'cogs.meme_cog',
          'cogs.utils_cog',
          'cogs.name_cog',
          'cogs.game_cog']
@client.event
async def on_ready():
    '''
    This prints a message when the on_ready event is detected.
    That is, when the bot logs onto discord when the script is ran.
    '''

    change_status.start()  # Triggers status change task

    print("Processing.....")
    print("|||||||||||||||")
    print("Bot has Successfully logged onto Discord...")
    print('Successfully logged in as {0.user}...'.format(client))
    # client.user gives the bots discord username tag
    print([guild.id for guild in client.guilds])


@client.event
async def on_guild_join(guild):
    '''
    This sends a message in the main channel, when the bot joins a guild.
    Joining a guild is synonymous to joining a server.
    Basically, a hi message the bot sends on enterring the server.
    '''

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            if guild.id not in db.list_collection_names():
                col = db[str(guild.id)]
                col.insert_one(
                    {'server_name': guild.name, 'server_id': guild.id})
            icon_url = 'https://cdn.discordapp.com/attachments/582605227081990233/627388598181953548/unknown.png'
            embed = discord.Embed(title='**Tear Drops:tm:**', description='A dynamic bot for _crying_, entertainment, economy and _other_ purposes...\n\
I am here to reek sorrow and depression. Come let\'s cry together 😢\
The prefix for the bot is _"qq"_, cuz you know _"less qq, more pew pew..."_ \
The currency credits for the bot are _tears_(hahah obviously). Have fun being sad...\
\nNOTE- Even though this is OpenSource and under MIT license, I request you to not start a commercial bot with the same name "Tear Drops:tm:"\
This bot is under MIT License(provided as is, do whatever you want) \
This has been uploaded to GitHub for educational and referencial purposes', colour=discord.Color.purple(), url='https://github.com/Py-Contributors/awesomeScripts/Tear-Drops_DiscordBot/')
            embed.set_footer(text='I Hope that you enjoyed the bot....😭')
            embed.set_image(url=icon_url)
            await channel.send(embed=embed)
        break
    print(f'Entered server {guild.name} : {guild.id}')


@tasks.loop(seconds=600)
async def change_status():
    '''
    loops through the cycle of the STATUS list and sets that as bot presence
    '''
    await client.change_presence(activity=discord.Game(next(STATUS)))
    # NOTE- There are other methods, that can be utilised instead of just 'playing'


@client.event
async def on_member_join(member):
    '''
    Event triggered when a new member enters server
    This prints the message out on Terminal.
    Also, this awaits the update_data() function, to add member to the database.
    '''
    print(f'{member} has joined the server.....')
    await update_data(member)


@client.event
async def on_member_remove(member):
    '''
    Event triggered when a member leaves the server
    NOTE- This can also be displayed on the server
    '''
    print(f'{member} has left the server......')


@client.event
async def on_message(message):
    '''
    Event triggered when a message is sent on the server
    This is associated with a few if-else responses(you can add more by looking at the examples)
    And finally, this triggers client.process_commands() which registers bot commands.
    '''
    if message.author == client.user:
        # self-ignore, to prevent responses to self
        return
    elif(message.author.bot):
        # To ignore the messages of other bots
        return
    else:
        # message_xp updation block
        global timelast
        await update_data(message.author)
        timlst = timelast
        if time.time() - timlst > 25:
            await add_experience(message, message.author, 10)
            timelast = time.time()
        # message if-else response examples(you can add more)
        if message.content.startswith('owo'):
            await message.channel.send('uwu')
        elif message.content.startswith('hi' or 'hey'):
            await message.channel.send('Hi there!👋')
        elif 'bitch' in message.content:
            await message.author.send('**BIRCH**')  # dms

    # prevents commands from not being processed
    await client.process_commands(message)


async def update_data(user):
    '''
    This Updates the user data in the db to add entry for new members
    '''
    if str(user.guild.id) not in db.list_collection_names():
        server = db[str(user.guild.id)]
        server.insert_one({'server_name': user.guild.name,
                           'server_id': user.guild.id})
        server.insert_one({'id': user.id, 'experience': 0,
                           'level': 1, 'credits': 0, 'crytime': 0})
        print(f'{user.guild.name} : {user.guild.id} added to database')
        print(f'{user.id} added to database...')
    else:
        server = db[str(user.guild.id)]
        # print(list(server.find({'id':user.id}))[-1].values())
        try:
            if len(list(server.find({'id': user.id}))) == 0:
                server.insert_one(
                    {'id': user.id, 'experience': 0, 'level': 1, 'credits': 0, 'crytime': 0})
                print(f'{user.id} added to database')
            elif user.id not in list(server.find({'id': user.id}))[-1].values():
                server.insert_one(
                    {'id': user.id, 'experience': 0, 'level': 1, 'credits': 0, 'crytime': 0})
                print(f'{user.id} added to database')
        except Exception as e:
            print(e)


async def add_experience(message, user, exp):
    """Adds xp to the user in the database, and calls the level up function"""
    server = db[str(user.guild.id)]
    stats = list(server.find({'id': user.id}))
    exp = stats[-1]['experience'] + exp
    new_stats = {"$set": {'experience': exp}}
    server.update_one(stats[-1], new_stats)
    await level_up(message.author, message.channel)


async def level_up(user, channel):
    """Takes care of checking the level-up parameters to boot ppl to next level when sufficient xp obtained"""
    server = db[str(user.guild.id)]
    stats = list(server.find({'id': user.id}))
    lvl_start = stats[-1]['level']
    experience = stats[-1]['experience']
    x = 35
    cnt = 1
    while (x < experience):
        x = 2 * x + 10
        cnt += 1

    if experience >= x:
        lvl_end = cnt - 1
    else:
        lvl_end = lvl_start

    if lvl_start < lvl_end:
        new_stats = {"$set": {'level': lvl_end}}
        server.update_one(stats[-1], new_stats)
        ls = lvl_end * 150
        server = db[str(user.guild.id)]
        stats = list(server.find({'id': user.id}))
        cred = stats[-1]['credits'] + ls
        new_stats = {"$set": {'credits': cred}}
        server.update_one(stats[-1], new_stats)
        embed = discord.Embed(title=f'{user} has leveled up to {lvl_end}.', description=f'You have been given {ls} tears for your active-ness.\n\
Saving {ls} tears in your vault of tears.', color=discord.Color.teal())
        embed.set_footer(text='😭')
        await channel.send(embed=embed)


@client.command(aliases=['daily'])
async def cry(ctx):
    '''credit gain command for crying'''
    user = ctx.message.author
    server = db[str(user.guild.id)]
    stats = list(server.find({'id': user.id}))
    trs = [0, 100, 150, 150, 200, 100, 50, 250, 500, 200, 1, 200, 150, 100]
    tim = stats[-1]['crytime']
    if time.time() - tim > 10800:
        tr = random.choice(trs)
        if tr > 1:
            embed = discord.Embed(title='**Tear Dispenser**', description=f'You cried {tr} tears.\n\
Storing them in the vaults of tears.Spend them wisely...💦\nSpend them wisely...', color=discord.Color.blue())
            embed.set_footer(text='😭')
            await ctx.send(embed=embed)
        elif tr == 1:
            embed = discord.Embed(title='**Tear Dispenser**', description='You really tried but only 1 tear came out...\n\
Storing it in the vaults of tears.Spend them wisely...💧\nSpend it wisely...', color=discord.Color.blue())
            embed.set_footer(text='😭')
            await ctx.send(embed=embed)
        else:
            tr2 = [
                'You were not sad',
                'You were surprisingly too happy to cry',
                'You cried so much already that the tears are not coming out',
                'You really tried but you could not cry',
                'The tears are not coming out...']
            message = random.choice(tr2)
            embed = discord.Embed(
                title='**Tear Dispenser**', description=f"You can't cry rn.{message}", color=discord.Color.blue())
            embed.set_footer(text='😭')
            embed.add_field(name='Try again after like 3 hours.',
                            value='oof', inline=False)
            await ctx.send(embed=embed)
        cred = tr + stats[-1]['credits']
        new_stats = {"$set": {'credits': cred, 'crytime': time.time()}}
        server.update_one(stats[-1], new_stats)
    else:
        embed = discord.Embed(title='**Tear Dispenser**', description=f"You can't cry rn. Let your eyes hydrate.\n\
Wait for like {round((10800 - time.time()+tim)//3600)} hours or something.", color=discord.Color.blue())
        embed.set_footer(text='😭')
        await ctx.send(embed=embed)


@client.command(aliases=['vaultoftears', 'tearvault'])
async def vault(ctx, member: discord.Member = None):
    '''Gives the users economy balance'''
    if not member:
        user = ctx.message.author
    else:
        user = member
    server = db[str(user.guild.id)]
    stats = server.find({'id': user.id})
    trp = list(stats)[-1]['credits']
    embed = discord.Embed(title='**Vault of Tears**',
                          description=f"Opening {user}'s vault-of-tears....", colour=discord.Color.blurple())
    embed.set_footer(text='Cry, cry, let the emotions flow through you...😭')
    embed.add_field(name='Tears', value=trp)
    await ctx.send(embed=embed)


@client.command(aliases=['lvl', 'dep_level'])
async def level(ctx, member: discord.Member = None):
    '''Gives the users level'''
    if not member:
        user = ctx.message.author
    else:
        user = member
    server = db[str(user.guild.id)]
    stats = server.find({'id': user.id})
    lvl = list(stats)[-1]['level']
    embed = discord.Embed(title=f'**Depression-Level of {user}**',
                          description="._.", colour=discord.Color.blurple())
    embed.set_footer(text='Cry, cry, let the emotions flow through you...😭')
    embed.add_field(name='Level', value=lvl)
    await ctx.send(embed=embed)


@client.command(aliases=['share', 'send', 'cryon'])
async def transfer(ctx, amount: int, member: discord.Member):
    '''transfer command'''
    user1 = ctx.message.author
    user2 = member
    server = db[str(user1.guild.id)]
    stat1 = list(server.find({'id': user1.id}))
    bal1 = stat1[-1]['credits'] - amount
    if bal1 >= 0:
        new_stat1 = {"$set": {'credits': bal1}}
        server.update_one(stat1[-1], new_stat1)

        stat2 = list(server.find({'id': user2.id}))
        bal2 = stat2[-1]['credits'] + amount
        new_stat2 = {"$set": {'credits': bal2}}
        server.update_one(stat2[-1], new_stat2)
        embed = discord.Embed(title='**Heart_to_heart**',
                              description=f"You tried to cry tears for {member}",
                              colour=discord.Color.green())
        embed.set_footer(
            text='Cry, cry, let the emotions flow through you...😭')
        embed.add_field(
            name=f"You handed out a vial of {amount} tears to {member}", value="._.")

    else:
        embed = discord.Embed(title='**Heart_to_heart**',
                              description=f"You tried to cry tears for {member}",
                              colour=discord.Color.green())
        embed.set_footer(
            text='Cry, cry, let the emotions flow through you...😭')
        embed.add_field(
            name=f"Failed to share {amount} tears.\nYou have insufficient tears in TearVault", value="._.")
    await ctx.send(embed=embed)


"""
@client.command(aliases=['market'])
async def shop(ctx):
    '''market command'''
    items= []
    embed=discord.Embed(title='**TearShops**',description = '',colour=discord.Color.red())
"""

# error_handling
@client.event
async def on_command_error(ctx, error):
    # TODO- Error Handling
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used..... ")
    else:
        await ctx.send(error)


# cog-loader
if __name__ == "__main__":
    for extension in ls_cog:
        client.load_extension(extension)

# Running the BOT:
client.run(str(DISCORD_BOT_TOKEN))
