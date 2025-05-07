import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# load env file
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()  #every single permission will be include in one of these intents
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secrets_role = "Gamer"
#Three action handle in this bot
#when the bot is ready
#when a new member joins the server
#when a message is recevied

@bot.event
async def on_ready():
    print(f"We are rady to go in {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the sever {member.name}")

@bot.event
async def on_message(message):
     if message.author == bot.user:
         return

     if "shit" in message.content.lower():
         await message.delete()
         await message.channel.send(f"{message.author.mention} - don't use that word !")

     await bot.process_commands(message)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secrets_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx .send(f"{ctx.author.mention} - You are now assigned to {secrets_role}")
    else:
        await ctx.send("Role Does Not Exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secrets_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secrets_role} removed")
    else:
        await ctx.send("Role Does Not Exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg} ")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is the reply your message")

@bot.command()
async def poll(ctx, *, question):
    embed  =discord.Embed(title="New Poll", description=question, color=discord.Color.green())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secrets_role)
async def secret(ctx):
    await ctx.send("Welcome to the club")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have permission to do that")

bot.run(token,log_handler=handler,log_level=logging.DEBUG)
