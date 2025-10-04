
import sys
import yaml
import subprocess
import asyncio
import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer


default_config = {
    "bot_token": "YOUR_BOT_TOKEN",
    "embed_color": "#2d3b60",
    "embed_author": "Kunter",
    "embed_icon": "https://github.com/kuntercode.png",
    "command_cooldown": 60,
    "server_address": "localhost",
    "start_command": "start.bat"
}

config = None

# create config file with default settings if not exists
try:
    with open("mcss_config.yaml", "x") as file:
        yaml.safe_dump(default_config, file, default_flow_style=False)

# read config file if exists
except FileExistsError:
    with open("mcss_config.yaml", "r") as file:
        config = yaml.safe_load(file)

if config is None:
    sys.exit()


bot = discord.Bot()

server = JavaServer.lookup(config["server_address"])

# default embed
embed = discord.Embed(
    title="[title]",
    description="[description]",
    color=int(config["embed_color"].replace("#", "0x"), 16),
)

if config["embed_author"] is not None:
    embed.set_author(name=config["embed_author"], icon_url=config["embed_icon"])


@bot.event
async def on_ready():
    print(f"bot ready! logged in as {bot.user}")
    check_server_status.start()


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"This command is on cooldown! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    else:
        raise error


@tasks.loop(seconds=45)
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

    await ctx.defer()
    
    try:
        status = await asyncio.wait_for(server.async_status(), timeout=10.0)
        embed.title = "Server Status"
        embed.description = f"The server is online, `{status.players.online}/{status.players.max}` players playing."
        await ctx.followup.send(embed=embed)

    except Exception:
        embed.title = "Server Status"
        embed.description = f"The server is offline."
        await ctx.followup.send(embed=embed)



@bot.slash_command(name="startserver", description="Starts the SMP server.")
@commands.cooldown(1, config["command_cooldown"], commands.BucketType.guild)
async def startserver(ctx: discord.ApplicationContext):
    global embed
    global server

    await ctx.defer()
    
    try:
        status = await asyncio.wait_for(server.async_status(), timeout=10.0)
        embed.title = "Server is already running"
        embed.description = f"The server has `{status.players.online}/{status.players.max}` players online."
        await ctx.followup.send(embed=embed)

    except Exception as e:
        subprocess.Popen(config["start_command"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        embed.title = "Server offline, starting..."
        embed.description = "This might take a few moments, please be patient."
        await ctx.followup.send(embed=embed)


# login to discord
bot.run(config["bot_token"])
