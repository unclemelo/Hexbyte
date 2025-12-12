import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import aiohttp
import traceback
import json

load_dotenv()
API_LINK = os.getenv("API_LINK")
API_STAT= "playerStats?steamID={}"
API_URL = API_STAT + API_STAT

class PlayerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.debug = True  # Toggle debug output

    async def debug_log(self, *msg):
        """Print debugging information if enabled."""
        if self.debug:
            print("[PlayerStats DEBUG]:", *msg)

    async def fetch_stats(self, steamid: str):
        """Fetch player stats from the WTF API."""
        url = API_URL.format(steamid)
        await self.debug_log(f"Fetching URL: {url}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    await self.debug_log(f"Status Code: {resp.status}")

                    if resp.status != 200:
                        await self.debug_log("Non-200 response:", resp.status)
                        return None

                    data = await resp.json()
                    await self.debug_log("Raw API Response:", data)

                    return data

        except Exception as e:
            await self.debug_log("Exception occurred in fetch_stats:", str(e))
            traceback.print_exc()
            return None

    @app_commands.command(name="wtfstats", description="Get WTF player stats using a Steam ID.")
    async def wtfstats(self, interaction: discord.Interaction, steamid: str):
        await interaction.response.defer()

        await self.debug_log(f"Command invoked by: {interaction.user} | SteamID: {steamid}")

        data = await self.fetch_stats(steamid)

        if not data:
            await self.debug_log("No data returned — API offline or invalid SteamID.")
            return await interaction.followup.send("❌ Could not fetch stats. Invalid SteamID or API offline.")

        # API returns array or single obj depending on implementation
        if isinstance(data, list):
            await self.debug_log("API returned list, selecting first index.")
            data = data[0]

        await self.debug_log("Parsed data:", data)

       # Calculate useful stats
        kills = data.get("TotalKills", 0)
        deaths = data.get("TotalDeaths", 0)
        assists = data.get("TotalAssists", 0)
        accuracy = 0
        if data.get("TotalShotsFired", 0) > 0:
            accuracy = round((data.get("TotalShotsHit", 0) / data.get("TotalShotsFired", 1)) * 100, 1)

        kd = round(kills / deaths, 2) if deaths > 0 else kills

        level = data.get("Level", 0)

        # Color based on KD (gamer style)
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

        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1446974550943465636/1447108236280070155/jcg14Ni.jpeg")

        # --- CORE PERFORMANCE ---
        embed.add_field(
            name="🔥 Performance",
            value=(
                f"**K/D:** `{kd}`\n"
                f"**Kills:** `{kills}` | **Deaths:** `{deaths}` | **Assists:** `{assists}`\n"
                f"**Headshots:** `{data.get('TotalHeadshots', 0)}`\n"
                f"**Accuracy:** `{accuracy}%`\n"
            ),
            inline=False
        )

        # --- MATCH INFO ---
        embed.add_field(
            name="🏆 Match Stats",
            value=(
                f"**Matches Played:** `{data.get('TotalMatches', 0)}`\n"
                f"**Wins / Losses:** `{data.get('MatchesWon', 0)} / {data.get('MatchesLost', 0)}`\n"
                f"**Rounds:** `{data.get('TotalRoundsWon', 0)}W / {data.get('TotalRoundsLost', 0)}L`\n"
                f"**Quit Early:** `{data.get('TotalMatchesQuitEarly', 0)}`\n"
            ),
            inline=False
        )

        # --- COMBAT DAMAGE ---
        embed.add_field(
            name="💥 Combat Stats",
            value=(
                f"**Damage Dealt:** `{data.get('TotalDamageDealt', 0)}`\n"
                f"**Damage Taken:** `{data.get('TotalDamageTaken', 0)}`\n"
                f"**Score:** `{data.get('TotalScore', 0)}`\n"
            ),
            inline=False
        )

        # --- EXTRA ---
        embed.add_field(
            name="📊 Additional",
            value=(
                f"**XP Earned:** `{data.get('TotalXP', 0)}`\n"
                f"**Time Played:** `{data.get('TotalTimePlayed', 'N/A')}`\n"
                f"**Last Updated:** `{data.get('LastUpdated', 'Unknown')}`"
            ),
            inline=False
        )

        embed.set_footer(text="WTF Game — Player Stats")

        await self.debug_log("Sending final embed.")
        await interaction.followup.send(embed=embed)




async def setup(bot):
    await bot.add_cog(PlayerStats(bot))
