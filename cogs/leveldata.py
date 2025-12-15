import json
import traceback
from pathlib import Path

import discord
from discord.ext import commands
from discord import app_commands


class LevelData(commands.Cog):
    """Cog that exposes level information from data/levels.json."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.levels = {}
        self.xp_rewards = {}
        self._load_levels()

    def _load_levels(self):
        try:
            data_path = Path(__file__).resolve().parents[1] / "data" / "levels.json"
            # Fallback to relative 'data/levels.json' if layout differs
            if not data_path.exists():
                data_path = Path("data") / "levels.json"

            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_levels = data.get("levels", {}) if isinstance(data, dict) else {}
            # Convert keys to ints for easier lookup
            self.levels = {int(k): int(v) for k, v in raw_levels.items()}

            # Load XP rewards table if present
            raw_xp = data.get("XPRewards", {}) if isinstance(data, dict) else {}
            for k, v in raw_xp.items():
                try:
                    self.xp_rewards[k] = int(v)
                except Exception:
                    self.xp_rewards[k] = v

        except Exception as e:
            traceback.print_exc()
            self.levels = {}

    def xp_for(self, level: int):
        return self.levels.get(level)

    def reward_for(self, key: str):
        return self.xp_rewards.get(key)

    @app_commands.command(name="levelinfo", description="Explain the WTF leveling system based on current level table.")
    async def levelinfo(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not self.levels:
            return await interaction.followup.send("⚠️ Level data not available.")

        embed = discord.Embed(title="📊 WTF Level System", color=discord.Color.blurple())
        # General explanation + examples based on the loaded `levels` table
        embed.description = (
            "The WTF leveling system uses total XP thresholds per level. "
            "When a player's total XP meets or exceeds the value for a level, they reach that level.\n\n"
            "Below are some example level thresholds from the current table:"
        )

        sample_levels = [1, 5, 10, 25, 50, max(self.levels.keys())]
        table = []
        for lv in sample_levels:
            xp = self.xp_for(lv)
            if xp is None:
                continue
            table.append(f"**{lv}** ➜ `{xp}` XP")

        embed.add_field(name="Example thresholds", value="\n".join(table), inline=False)
        # Include XP rewards information from the table
        if self.xp_rewards:
            reward_lines = []
            for k, v in self.xp_rewards.items():
                # Skip any internal/id fields
                if k.lower() == "id":
                    continue
                reward_lines.append(f"**{k}** ➜ `{v}` XP")

            if reward_lines:
                embed.add_field(name="XP Rewards", value="\n".join(reward_lines), inline=False)
        embed.add_field(name="How it works", value=(
            "- XP is cumulative (stored as total XP).\n"
            "- Reaching the XP threshold awards the level.\n"
            "- The table defines total XP required per level; higher levels require more total XP."
        ), inline=False)

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(LevelData(bot))
