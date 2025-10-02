
from mcstatus import JavaServer
import discord
from discord.ext import commands
import yaml
import subprocess
import asyncio

# load config file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


bot = discord.Bot()

server_process = None

server = JavaServer.lookup(config["mc_server"]["ip"])
#server = JavaServer.lookup("mc.hypixel.net")


embed = discord.Embed(
    title="[title]",
    description="[description]",
    color=discord.Colour.blurple(),
)

embed.set_author(name="Furry Team", icon_url="https://cdn.discordapp.com/attachments/1033783709364670464/1419624423610122352/avatar_e3d00202-c001-4ab3-9f50-32baf29d0fd8.png?ex=68d26fc5&is=68d11e45&hm=12e224421976bd93fe94e706a966c8e88d2c77e3c47cfa449101ef960f6f8908&")



@bot.event
async def on_ready():
    print(f"bot ready! logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="/startserver"))


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"This command is on cooldown! Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    else:
        raise error



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

    except Exception as e:
        embed.title = "Server Status"
        embed.description = f"The server is offline."
        await ctx.followup.send(embed=embed, ephemeral=True)



@bot.slash_command(name="startserver", description="Starts the SMP server.")
@commands.cooldown(1, config["command_cooldwon"], commands.BucketType.guild)
async def startserver(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")
    return
    
    global server_process
    global server
    global embed


    # check if the server is already running using mc status



    # check if the server is already running from script
    if server_process is None or server_process.poll() is not None:
        try:
            await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Server Online"))
            server_process = subprocess.Popen(config["mc_server"]["start_command"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            embed.title = "Server offline, starting..."
            embed.description = "This might take a few moments, please be patient."
            await ctx.respond(embed=embed, ephemeral=True)

        except FileNotFoundError:
            await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="/startserver"))
            embed.title = "ERROR starting server!"
            embed.description = "Start script not found!"
            await ctx.respond(embed=embed, ephemeral=True)


        except Exception as e:
            print(f"An error occurred: {e}")
            await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="/startserver"))
            embed.title = "ERROR starting server!"
            embed.description = "An Error occurred while starting the server."
            await ctx.respond(embed=embed, ephemeral=True)

    else:
        server = JavaServer.lookup(config["mc_server"]["ip"])
        status = server.status()
        embed.title = "Server is already running"
        embed.description = f"The server has `{status.players.online}/{status.players.max}` players online."
        await ctx.respond(embed=embed, ephemeral=True)



# login to discord
bot.run(config["bot_token"])
