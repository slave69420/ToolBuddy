from code import interact
from enum import IntEnum
from pydoc import visiblename
from re import A
from tkinter import dnd
from turtle import title
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction
import datetime
import random
import json
import asyncio


with open('config.json') as f:  
    data = json.load(f)
    token = data['Token']
    prefix = data['Prefix']

us = 0
um = 0
uh = 0
ud = 0


intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    print(f'Bot online. Bot discriminator: {client.user}')
    uptimecounter.start()
    await client.change_presence(status='dnd', activity = nextcord.Game(name='-help | Made by slave#3507'))
        
        

@client.event
async def on_message_delete(message):
    embed = nextcord.Embed(title =f'{message.author.name} has deleted a message | {message.author.id}', description=f'{message.content}')
    channel = client.get_channel(964097417194659849)
    await channel.send(embed=embed)

@client.event
async def on_message_edit(message_before, message_after):
    embed = nextcord.Embed(title =f'{message_before.author.name} has edited a message | {message_before.author.id}')
    embed.add_field(name='Before message:', value=f'{message_before.content}', inline=True)
    embed.add_field(name='After message:', value=f'{message_after.content}', inline=True)
    channel = client.get_channel(964097417194659849)
    await channel.send(embed=embed)




@tasks.loop(seconds=2.0)
async def uptimecounter():
    global us, um, uh, ud
    us += 2
    if us == 60:
        us = 0
        um += 1
        if um == 60:
            um = 0
            uh += 1
            if uh == 24:
                uh = 0
                ud = 1
@uptimecounter.before_loop
async def beforeuptimecounter():
    await client.wait_until_ready()

@client.command(description = 'Help command for the official ToolBuddy discord bot')
async def help(ctx):
    embed = nextcord.Embed(title='help | ToolBuddy official discord bot', description='Help command for the official ToolBuddy discord bot')
    for command in client.walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = 'no description provided.'
        embed.add_field(name=f'`-{command.name}{command.signature if command.signature is not None else ""}`', value=description)
    await ctx.reply(embed=embed)


        


@client.command(name='status', description='shows bot uptime')
async def uptime(ctx):
    global us, um, uh, ud
    embed = nextcord.Embed(title = 'My uptime!')
    embed.add_field(name='days:', value=ud, inline=True)
    embed.add_field(name='Hours:', value=uh, inline=True)
    embed.add_field(name='Minutes:', value=um, inline=True)
    embed.add_field(name='Seconds:', value=us, inline=False)
    await ctx.reply(embed=embed)




testserverId = 964097416464859156

@client.slash_command(name = 'ping', description ='lets try this', guild_ids=[testserverId])
async def test(interaction: Interaction):
    await interaction.response.send_message('hello guys! i have slash commands now! arf arf arf')




@client.command(name='8ball Mystery', description='ask a question and toolbuddy shall answer',aliases=['8ball', '8b'])
async def eightball(ctx, *, question):
    responses = [
        'Hell no.',
        'Prolly not.',
        'Idk bro.',
        'Prolly.',
        'Hell yeah my dude.',
        'It is certain.',
        'idfk', #lmfao
        'It is decidedly so.',
        'Without a Doubt.',
        'Yes - Definitaly.',
        'You may rely on it.',
        'As i see it, Yes.',
        'Most Likely.',
        'Outlook Good.',
        'Yes!',
        'No!',
        'Signs a point to Yes!',
        'Reply Hazy, Try again.',
        'IDK but u should try again for a better answer.',
        'Better not tell you know.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't Count on it.",
        'My reply is No.',
        'My sources say No.',
        'Outlook not so good.',
        'Very Doubtful',
        'What do you think?',
        'I have no idea.',
        'I have no idea what you are talking about.',
        'wait, what?',
        'ayo, what?',
        'sure!',
        'my systems say yes.'] 
        # ok

        #im adding ??? answers

    await ctx.reply(f'{random.choice(responses)}')

@client.command(name='Kick', description='Kicks a member. Args: <member> <Reason>',aliases=['boot', 'minishit'])
async def kick(ctx, member:nextcord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.send('You do not have the following permission(s): ```kick_members```')
        return
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked!! arf arf arf')

@client.command(name='ban', description='Bans a member. Args: <member> <Reason>',aliases=['hammer', 'bigshit'])
async def ban(ctx, member : nextcord.Member, guild, *, reason=None):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You do not have the following permission(s): ```ban_members```')
        return
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been ban hammered!')

@client.command(name='unban', description='Unbans a member. Args: <discriminator>',aliases=['unhammer'])
async def unban(ctx, *, guild, member : nextcord.Member):

    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You do not have the following permission(s): ```ban_members```')
        return

    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned{user.mention}')
            return

@client.command(name='purge', description='Purges a certain number of messages. Args: <number of messages>')
async def purge(ctx, amount=10):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You do not have the following permission(s): ```manage_messages```')
        return
    amount = amount+1
    if amount > 101:
        await ctx.send('Cannot purge more than 100 messages')
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'purged {amount} messages')

@client.command(name='mute', description='Mutes a member. Args: <member> <Reason>',aliases=['shush'])
async def mute(ctx, member : nextcord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You do not have the following permission(s): ```manage_messages```')
        return
    guild = ctx.guild
    muterole = nextcord.utils.get(guild.roles, name="Muted")
    
    if not muterole:
        await ctx.send('there is no mute role, creating a mure role now!')
        muterole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(muterole, speak=False, send_messages=False, read_message_history=False, read_messages=True)
    await member.add_roles(muterole, reason=reason)
    await member.send(f'you have been muted from: **{guild.name}** | Reason: **{reason}**')

@client.command(name='unmute', description='Unmutes a member. Args: <member> <Reason>',aliases=['unshush'])
async def unmute(ctx, member : nextcord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You do not have the following permission(s): ```manage_messages```')
        return
    guild = ctx.guild
    muterole = nextcord.utils.get(guild.roles, name="Muted")
    
    if not muterole:
        await ctx.send('There is no muterole to be removed from this user.')
        return

    await member.remove_roles(muterole, reason=reason)
    await member.send(f'you have been unmuted from: **{guild.name}** | Reason: **{reason}**')


class Dropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Python", description="Easy language for bot creation"),
            nextcord.SelectOption(label="JS", description="a little annoying"),
            nextcord.SelectOption(label="Lua", description="Could you even make bots?")
        ]
        super().__init__(placeholder="Select a cool ass language", min_values=1, max_values=1, options = options)

async def callback(self, interaction: nextcord.Interaction):
    await interaction.response.send_message(f'you chose {self.values[0]}')

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


@client.command(name='Dropdown', description='Dropdown test')
async def dropdown(ctx):
    view = DropdownView()
    await ctx.send('pick some cool stuff', view=view)

@client.command(name='suggest', description='basically a command to suggest stuff to add/remove in the server, script or even our bot!')
async def suggest(ctx, *, suggestion):
    await ctx.channel.purge(limit=1)
    channel = nextcord.utils.get(ctx.guild.text_channels, name='🤔│suggestions')
    suggest = nextcord.Embed(title='a new suggestion has appeared', description=f'{ctx.author.name} has suggested `{suggestion}`')
    sugg = await channel.send(embed=suggest)
    await channel.send(f'^^ Suggestion ID: {sugg.id}')
    await sugg.add_reaction('👍')
    await sugg.add_reaction('👎')

@client.command(name='approve', description='Only for staff use. approves a suggestion from the -suggest command')
async def approve(ctx, id:int=None, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You do not have the following permission(s): ```manage_messages```')
        return 
    if id is None:
        return
    channel = nextcord.utils.get(ctx.guild.text_channels, name='🤔│suggestions')
    if channel is None:
        return
    suggestionMSG = await channel.fetch_message(id)
    embed = nextcord.Embed(title = f'Suggestion has been approved!', description=f'the suggestion with the following id:{suggestionMSG.id} has been approved by {ctx.author.name}. | Reason: {reason}')
    await channel.send(embed=embed)

@client.command(name='deny', description='Only for staff use. denies a suggestion from the -suggest command')
async def deny(ctx, id:int=None, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('You do not have the following permission(s): ```manage_messages```')
        return     
    if id is None:
        return
    channel = nextcord.utils.get(ctx.guild.text_channels, name='🤔│suggestions')
    if channel is None:
        return
    suggestionMSG = await channel.fetch_message(id)
    embed = nextcord.Embed(title = f'Suggestion has been denied.', description=f'the suggestion with the following id:{suggestionMSG.id} has been denied by {ctx.author.name}. | Reason: {reason}')

    
    await channel.send(embed=embed)



# Tf i am kegit getting errors everywhere :skull:
client.run(token)