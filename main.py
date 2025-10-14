import discord
import os
import logging
import random
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD_ID = discord.Object(id='1423048695259201640')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.guilds = True

bot = commands.Bot(command_prefix='!',intents=intents)

#readycheck
@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=1423048695259201640))
    print(f"Good Nomnomnomming!")


#code for adding a role via reaction
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == bot.role_message_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        reaction_role_map = {
        "🎥": "Watch Partiers", 
        "⛏️": "Cool Pro Fortnite Gamer", 
        "⚔️": "Warriors of Light", 
        "🎲": "TableToppers", 
        "🔞": "NSFW"
        }
        emoji = str(payload.emoji) 
        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name= role_name)
            await member.add_roles(role)

#code for removing role via reaction
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == bot.role_message_id:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        reaction_role_map = {
        "🎥": "Watch Partiers", 
        "⛏️": "Cool Pro Fortnite Gamer", 
        "⚔️": "Warriors of Light", 
        "🎲": "TableToppers", 
        "🔞": "NSFW"
        }
        emoji = str(payload.emoji) 
        if emoji in reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name= role_name)
            await member.remove_roles(role)            

#code for displaying the role message
@bot.tree.command(name="roles", description="lets users pick a role",guild=GUILD_ID)
async def roles(interaction: discord.Interaction): 
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not allowed to run this command.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)

    embed_description = (
    "React to this message to recieve or remove a role!\n\n"
    "🎥 Watch Partiers\n"
    "⛏️ Cool Pro Fortnite Gamer\n"
    "⚔️ Warriors of Light\n"
    "🎲 TableToppers\n"
    "🔞 NSFW"
    )

    embed_message = discord.Embed(title="Role Selection!", description=embed_description, color=discord.Color.purple())
    message = await interaction.channel.send(embed=embed_message)

    emojis = ['🎥', '⛏️', '⚔️', '🎲', '🔞']

    for emoji in emojis:
        await message.add_reaction(emoji)

    bot.role_message_id = message.id

    await interaction.followup.send("Role message created", ephemeral=True)

@bot.command()
async def goodnomnomnomming(ctx):
    await ctx.send(f"<:nomnomnomming:1423118737942511776> Good Nomnomnomming! <:nomnomnomming:1423118737942511776>")

@bot.command()
async def feeling(ctx):
    blackwhite = random.choice(['black','white'])
    match blackwhite:
        case 'black':
            await ctx.send(f"<:monokumablack:1427714063437140029>")
        case 'white':
            await ctx.send(f"<:monokumawhite:1427714075185647759>")

    

bot.run(token, log_handler=handler, log_level=logging.DEBUG)