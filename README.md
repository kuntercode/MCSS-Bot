# MCSS Bot (Minecraft Server Starter Discord Bot)

**MCSS** is a Discord bot that allows you to remotely start and monitor your Minecraft server directly from your Discord server.
It’s built using **[Pycord](https://docs.pycord.dev/)** and **[mcstatus](https://pypi.org/project/mcstatus/)**.

## Installation

1. **Create a Discord Bot**
   Start by creating a new bot in the [Discord Developer Portal](https://guide.pycord.dev/getting-started/creating-your-first-bot).
   Make sure the bot has the `application.commands` permission — otherwise, slash commands will not work.

2. **Invite the Bot**
   After inviting the bot to your server, copy your **bot token** and store it securely. **Never share your token** with anyone.

3. **Install MCSS**

   - The easiest way to install MCSS is to download the **EXE** file from the [Releases](../../releases) page and place it in your Minecraft server folder (the same folder as your start script).
   - Alternatively, you can run the bot using Python by downloading `main.py` from the source code.
     Make sure you have **Pycord** and **mcstatus** installed beforehand:

     ```bash
     pip install py-cord mcstatus
     ```

## Configuration

When the bot is run for the first time, it will automatically create a configuration file named `mcss_config.yaml`.
An example configuration looks like this:

```yaml
bot_token: YOUR_BOT_TOKEN # Paste your bot token here
command_cooldown: 60 # Cooldown (in seconds) for the /startserver command
embed_author: Kunter # Embed author name, set to null to disable
embed_color: "#2d3b60" # Embed color (in HEX format)
embed_icon: https://github.com/kuntercode.png # Embed icon URL, null to disable
server_address: localhost # Minecraft server address
start_command: start.bat # Minecraft server start script
```

After adjusting the settings to your preference, save the file and run the bot again.

## Usage

Once the bot is running:

- Use `/startserver` to start your Minecraft server.
- Use `/serverstatus` to check the current server status.

The bot updates its own Discord presence approximately every 45 seconds, showing whether the server is online and how many players are currently active.

## Contributing and Issues

Contributions are always welcome!
You can:

- Suggest new features or improvements.
- Submit a pull request with enhancements or fixes.
- Report bugs or issues on the [Issues](../../issues) page.

## License

This project is licensed under the [MIT License](LICENSE).
