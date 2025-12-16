import discord
from discord.ext import commands
from discord import app_commands


class LookingForGame(commands.Cog):
    """Test cog for public leaderboard once API is ready."""

    def __init__(self, bot):
        self.bot = bot
        self.debug = True

    async def debug_log(self, *msg):
        if self.debug:
            print("[LFG DEBUG]:", *msg)

    # TODO: Implement LFG functionality here for Waifu Tactical Force
    @app_commands.command(name="wtflfg", description="Find or create a Looking For Game (LFG) session.")
    async def wtflfg(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.debug_log("LFG command invoked by", interaction.user)

        # Placeholder response
        await interaction.followup.send("🔍 LFG functionality is under development. Stay tuned!")

async def setup(bot):
    await bot.add_cog(LookingForGame(bot))
