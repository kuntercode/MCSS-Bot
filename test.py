
from mcstatus import JavaServer
import discord
import yaml
import subprocess

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

server_process = None

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"bot ready! logged in as {bot.user}")

@bot.slash_command(name="startserver", description="Starts the SMP server.")

async def test(ctx: discord.ApplicationContext):
    global server_process

    embed = discord.Embed(
        title="[title]",
        description="[description]",
        color=discord.Colour.blurple(),
    )

    embed.set_author(name="Furry Team", icon_url="https://cdn.discordapp.com/attachments/1033783709364670464/1419624423610122352/avatar_e3d00202-c001-4ab3-9f50-32baf29d0fd8.png?ex=68d26fc5&is=68d11e45&hm=12e224421976bd93fe94e706a966c8e88d2c77e3c47cfa449101ef960f6f8908&")

    if server_process is None or server_process.poll() is not None:
        try:
            print("Starting server...")
            server_process = subprocess.Popen(config["mc_server"]["start_command"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            embed.title = "Server offline, starting..."
            embed.description = "This might take a few moments, please be patient."
            await ctx.respond(embed=embed)

        except FileNotFoundError:
            print("Error: start script not found.")
            embed.title = "ERROR starting server!"
            embed.description = "Start script not found!"
            await ctx.respond(embed=embed)


        except Exception as e:
            print(f"An error occurred: {e}")
            embed.title = "ERROR starting server!"
            embed.description = "An Error occurred while starting the server."
            await ctx.respond(embed=embed)

    else:
        print("Server is already running.")
        server = JavaServer.lookup(config["mc_server"]["ip"])
        status = server.status()
        embed.title = "Server is already running"
        embed.description = f"The server has {status.players.online}/{status.players.max} players online."
        await ctx.respond(embed=embed)


bot.run(config["bot_token"])
