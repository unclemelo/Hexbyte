import discord
import os
import io
import traceback
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import aiohttp
from utils.stats_img import generate_stats_image

load_dotenv()
API_LINK = os.getenv("API_LINK", "")
API_STAT = "playerStats?steamID={}"
API_URL = API_LINK + API_STAT

class PlayerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.debug = True

    async def debug_log(self, *msg):
        if self.debug:
            print("[PlayerStats DEBUG]:", *msg)

    async def fetch_stats(self, steamid: str):
        url = API_URL.format(steamid)
        await self.debug_log("Fetching URL:", url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    await self.debug_log("Status Code:", resp.status)
                    if resp.status != 200:
                        return None
                    data = await resp.json()
                    return data
        except Exception as e:
            await self.debug_log("Exception in fetch_stats:", e)
            traceback.print_exc()
            return None

    @app_commands.command(name="wtfstats", description="Get WTF player stats using a Steam ID.")
    async def wtfstats(self, interaction: discord.Interaction, steamid: str):
        await interaction.response.defer()
        await self.debug_log("Command invoked by", interaction.user, "steamid", steamid)

        data = await self.fetch_stats(steamid)
        if not data:
            return await interaction.followup.send("❌ Could not fetch stats. Invalid SteamID or API offline.")

        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        # Build embed summary
        kills = data.get("TotalKills", 0)
        deaths = data.get("TotalDeaths", 0)
        assists = data.get("TotalAssists", 0)
        kd = round(kills / deaths, 2) if deaths > 0 else kills
        level = data.get("Level", 0)

        if kd >= 2:
            embed_color = discord.Color.green()
        elif kd >= 1:
            embed_color = discord.Color.blue()
        else:
            embed_color = discord.Color.red()

        embed = discord.Embed(
            title=f"🎮 WTF Player Stats",
            description=f"**SteamID:** `{steamid}`\n**Level:** `{level}` ⭐",
            color=embed_color
        )
        embed.add_field(name="🔥 Performance", value=(
            f"**K/D:** `{kd}`\n"
            f"**Kills:** `{kills}` | **Deaths:** `{deaths}` | **Assists:** `{assists}`\n"
        ), inline=False)

        # generate image (this generator is synchronous, so run in executor to avoid blocking)
        try:
            loop = interaction.client.loop
            img_buffer = await loop.run_in_executor(None, generate_stats_image, data)
            file = discord.File(img_buffer, filename="wtfstats.png")
            embed.set_image(url="attachment://wtfstats.png")
            await interaction.followup.send(embed=embed, file=file)
            await self.debug_log("Sent embed + image (split version).")
        except Exception as e:
            await self.debug_log("Failed to generate or send image:", e)
            traceback.print_exc()
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PlayerStats(bot))
