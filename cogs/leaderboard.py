import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import traceback

# MOCK DATA FOR TESTING
TEST_LEADERBOARD = [
    {"SteamID": "1234567890", "PlayerName": "TestPlayer1", "TotalKills": 150, "TotalDeaths": 75, "TotalAssists": 20, "Level": 10},
    {"SteamID": "9876543210", "PlayerName": "TestPlayer2", "TotalKills": 50, "TotalDeaths": 50, "TotalAssists": 10, "Level": 5},
    {"SteamID": "1112223330", "PlayerName": "TestPlayer3", "TotalKills": 5, "TotalDeaths": 20, "TotalAssists": 2, "Level": 2},
    {"SteamID": "4445556660", "PlayerName": "TestPlayer4", "TotalKills": 200, "TotalDeaths": 100, "TotalAssists": 50, "Level": 15},
    {"SteamID": "7778889990", "PlayerName": "TestPlayer5", "TotalKills": 75, "TotalDeaths": 25, "TotalAssists": 15, "Level": 7},
    {"SteamID": "2223334440", "PlayerName": "TestPlayer6", "TotalKills": 10, "TotalDeaths": 5, "TotalAssists": 1, "Level": 3},
    {"SteamID": "5556667770", "PlayerName": "TestPlayer7", "TotalKills": 120, "TotalDeaths": 60, "TotalAssists": 30, "Level": 12},
    {"SteamID": "8889990001", "PlayerName": "TestPlayer8", "TotalKills": 30, "TotalDeaths": 40, "TotalAssists": 5, "Level": 4},
    {"SteamID": "3334445550", "PlayerName": "TestPlayer9", "TotalKills": 0, "TotalDeaths": 10, "TotalAssists": 0, "Level": 1},
    {"SteamID": "6667778880", "PlayerName": "TestPlayer10", "TotalKills": 90, "TotalDeaths": 45, "TotalAssists": 25, "Level": 8},
]


class LeaderboardTest(commands.Cog):
    """Test cog for public leaderboard once API is ready."""

    def __init__(self, bot):
        self.bot = bot
        self.debug = True

    async def debug_log(self, *msg):
        if self.debug:
            print("[LeaderboardTest DEBUG]:", *msg)

    async def fetch_leaderboard(self):
        """Mock fetch function. Replace with API call later."""
        await self.debug_log("Fetching mock leaderboard...")
        await asyncio.sleep(0.5)  # simulate network delay
        return TEST_LEADERBOARD

    @app_commands.command(name="wtfleaderboard", description="Get the WTF leaderboard (test version).")
    async def wtfleaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.debug_log("Leaderboard command invoked by", interaction.user)

        try:
            leaderboard = await self.fetch_leaderboard()
            if not leaderboard:
                return await interaction.followup.send("❌ Leaderboard data is empty.")

            # Build embed
            embed = discord.Embed(
                title="WTF Leaderboard (Test)",
                description="Top players (mock data).",
                color=discord.Color(0x8fb5f0)
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1448886491416629349/1448887023803961447/wtf-waifu-tactical-force.png?ex=693ce4b1&is=693b9331&hm=99784c82217f0fc1ad21b710f9d6f7c5570d5e97a234485e255ca7e35c792e7f&")

            for idx, player in enumerate(leaderboard, start=1):
                kills = player.get("TotalKills", 0)
                deaths = player.get("TotalDeaths", 0)
                kd = round(kills / deaths, 2) if deaths > 0 else kills

                # Use special emojis for top 3
                if idx == 1:
                    rank_display = "<:letterw:1448898982725025812>"
                elif idx == 2:
                    rank_display = "<:lettert:1448898946951942175>"
                elif idx == 3:
                    rank_display = "<:letterf:1448898880665161728>"
                else:
                    rank_display = str(idx)

                embed.add_field(
                    name=f"{rank_display}. {player.get('PlayerName', 'Unknown')} (Level {player.get('Level', 0)})",
                    value=f"Kills: {kills} | Deaths: {deaths} | K/D: {kd} | Assists: {player.get('TotalAssists',0)}",
                    inline=False
                )


            await interaction.followup.send(embed=embed)
            await self.debug_log("Sent leaderboard embed.")
            
        except Exception as e:
            await self.debug_log("Exception in leaderboard command:", e)
            traceback.print_exc()
            await interaction.followup.send("❌ An error occurred while fetching the leaderboard.")

async def setup(bot):
    await bot.add_cog(LeaderboardTest(bot))
