
from mcstatus import JavaServer
import discord
import dotenv
import os
import subprocess


server_ip = "147.185.221.29:47011"

server_process = None

def start_server():
    global server_process

    if server_process is None or server_process.poll() is not None:
        try:
            print("Starting server...")
            server_process = subprocess.Popen("start.bat", creationflags=subprocess.CREATE_NEW_CONSOLE)
            return 1

        except FileNotFoundError:
            print("Error: start script not found.")
            return -1

        except Exception as e:
            print(f"An error occurred: {e}")
            return -1

    else:
        print("Server is already running.")
        return 0


dotenv.load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"bot ready! logged in as {bot.user}")

@bot.slash_command(name="startserver", description="Starts the SMP server.")
async def test(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Server offline, starting...",
        description="This might take a few moments, please be patient.",
        color=discord.Colour.blurple(),
    )

    embed.set_author(name="Furry Team", icon_url="https://cdn.discordapp.com/attachments/1033783709364670464/1419624423610122352/avatar_e3d00202-c001-4ab3-9f50-32baf29d0fd8.png?ex=68d26fc5&is=68d11e45&hm=12e224421976bd93fe94e706a966c8e88d2c77e3c47cfa449101ef960f6f8908&")
    
    res = start_server()
    if res == 1:
        embed.title = "Server offline, starting..."
        embed.description = "This might take a few moments, please be patient."
        await ctx.respond(embed=embed)

    elif res == 0:
        server = JavaServer.lookup("147.185.221.29:47011")
        status = server.status()
        embed.title = "Server is already running"
        embed.description = f"The server has {status.players.online}/{status.players.max} players online."
        await ctx.respond(embed=embed)

    else:
        embed.title = "ERROR starting server!"
        embed.description = "An Error occurred while starting the server."
        await ctx.respond(embed=embed)


bot.run(os.getenv('TOKEN'))
