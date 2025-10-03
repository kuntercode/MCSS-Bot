
from mcstatus import JavaServer
import discord
from discord.ext import tasks, commands
import yaml
import subprocess
import asyncio

# load config file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

bot = discord.Bot()

server = JavaServer.lookup(config["server_address"])

# default embed
embed = discord.Embed(
    title="[title]",
    description="[description]",
    color=discord.Colour.blurple(),
)

embed.set_author(name="Furry Team", icon_url="https://cdn.discordapp.com/attachments/1033783709364670464/1419624423610122352/avatar_e3d00202-c001-4ab3-9f50-32baf29d0fd8.png?ex=68d26fc5&is=68d11e45&hm=12e224421976bd93fe94e706a966c8e88d2c77e3c47cfa449101ef960f6f8908&")


@bot.event
async def on_ready():
    print(f"bot ready! logged in as {bot.user}")
    #await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="/startserver"))
    check_server_status.start()


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"This command is on cooldown! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    else:
        raise error


@tasks.loop(seconds=7)
async def check_server_status():
    global server

    try:
        status = await asyncio.wait_for(server.async_status(), timeout=10.0)
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"Server, {status.players.online}/{status.players.max} online"))

    except Exception:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="/startserver"))



@bot.slash_command(name="serverstatus", description="Checks the server status.")
async def serverstatus(ctx: discord.ApplicationContext):
    global embed
    global server

    await ctx.defer(ephemeral=True)
    
    try:
        status = await asyncio.wait_for(server.async_status(), timeout=10.0)
        embed.title = "Server Status"
        embed.description = f"The server is online, `{status.players.online}/{status.players.max}` players playing."
        await ctx.followup.send(embed=embed, ephemeral=True)

    except Exception:
        embed.title = "Server Status"
        embed.description = f"The server is offline."
        await ctx.followup.send(embed=embed, ephemeral=True)



@bot.slash_command(name="startserver", description="Starts the SMP server.")
@commands.cooldown(1, config["command_cooldown"], commands.BucketType.guild)
async def startserver(ctx: discord.ApplicationContext):
    global embed
    global server

    await ctx.defer(ephemeral=True)
    
    try:
        status = await asyncio.wait_for(server.async_status(), timeout=10.0)
        embed.title = "Server is already running"
        embed.description = f"The server has `{status.players.online}/{status.players.max}` players online."
        await ctx.followup.send(embed=embed, ephemeral=True)

    except Exception as e:
        subprocess.Popen(config["start_command"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        embed.title = "Server offline, starting..."
        embed.description = "This might take a few moments, please be patient."
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Server Online"))
        await ctx.followup.send(embed=embed, ephemeral=True)


# login to discord
bot.run(config["bot_token"])
