import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

# ──────────────────────────────────────────────
# Load environment
load_dotenv()
TOKEN = os.getenv("TOKEN")

# ──────────────────────────────────────────────
# Bot setup
intents = discord.Intents.all()
client = commands.AutoShardedBot(command_prefix="bt!", shard_count=1, intents=intents)
client.remove_command("help")

# ──────────────────────────────────────────────
# Logging helper
def log(message: str):
    time = datetime.now().strftime("%H:%M:%S")
    print(f"[{time}] {message}")

# ──────────────────────────────────────────────
# Events
@client.event
async def on_ready():
    log(f"Buggy online as {client.user} ({client.user.id})")
    log(f"Connected to {len(client.guilds)} guilds.")

    # Set streaming presence
    await client.change_presence(
        activity=discord.Streaming(
            name="🐛 | Tracking Bugs on WTF",
            url="https://www.youtube.com/@WaifuTacticalForce"
        )
    )

    # Sync slash commands
    try:
        synced = await client.tree.sync()
        log(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        log(f"Slash command sync failed: {e}")

# ──────────────────────────────────────────────
# Cog loader
async def load_cogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            try:
                await client.load_extension(f"cogs.{filename[:-3]}")
                log(f"Loaded cog: {filename}")
            except Exception as e:
                log(f"Failed to load {filename}: {e}")

# ──────────────────────────────────────────────
# Main entry
async def main():
    await load_cogs()
    log("Starting BugTracker...")
    try:
        await client.start(TOKEN)
    except KeyboardInterrupt:
        log("Shutdown requested.")
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
