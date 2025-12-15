import json
import traceback
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui


class WeaponData(commands.Cog):
    """Cog that exposes weapon information from data/weapons.json."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.weapons = {}
        self._load_weapons()

    def _load_weapons(self):
        try:
            data_path = Path(__file__).resolve().parents[1] / "data" / "weapons.json"
            if not data_path.exists():
                data_path = Path("data") / "weapons.json"

            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw = data.get("WeaponStats", {}) if isinstance(data, dict) else {}
            # normalize keys to ints
            self.weapons = {int(k): v for k, v in raw.items()}

        except Exception:
            traceback.print_exc()
            self.weapons = {}

    def get_weapon(self, wid: int) -> Optional[dict]:
        return self.weapons.get(wid)

    @app_commands.command(name="weaponinfo", description="Show how weapon stats work and some example weapons.")
    async def weaponinfo(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if not self.weapons:
            return await interaction.followup.send("⚠️ Weapon data not available.")

        # Prepare ordered weapon id list for pagination
        ordered_ids = sorted(self.weapons.keys())

        def make_embed_for(index: int) -> discord.Embed:
            wid = ordered_ids[index]
            w = self.get_weapon(wid) or {}
            name = w.get("Name", f"Weapon {wid}")

            e = discord.Embed(title=f"🔫 {name} (ID {wid})", color=discord.Color.dark_gold())
            # main stats summary
            dmg = w.get("BaseDamage", "—")
            fr = w.get("FireRate", "—")
            mag = w.get("MaxMagazineAmmo", "—")
            pellets = w.get("PelletsPerCartridge", "—")
            e.add_field(name="Stats", value=(
                f"**BaseDamage:** `{dmg}`\n"
                f"**FireRate (RPM):** `{fr}`\n"
                f"**Magazine:** `{mag}`\n"
                f"**Pellets:** `{pellets}`\n"
            ), inline=False)

            # other useful fields
            misc_lines = []
            for key in ("MovementSpeed", "ADSSpeed", "LoadedReloadSpeed", "EmptyReloadSpeed", "EquipSpeed", "BulletVelocity", "MaximumRange"):
                if key in w:
                    misc_lines.append(f"**{key}:** `{w.get(key)}`")
            if misc_lines:
                e.add_field(name="Other", value="\n".join(misc_lines), inline=False)

            # show image if present
            for key in ("SideImage", "Image", "Thumbnail"):
                url = w.get(key)
                if url:
                    try:
                        e.set_thumbnail(url=url)
                    except Exception:
                        pass
                    break

            e.set_footer(text=f"Weapon {index+1}/{len(ordered_ids)}")
            return e

        # UI view for navigation
        class WeaponPager(ui.View):
            def __init__(self, *, timeout: Optional[float] = 120.0):
                super().__init__(timeout=timeout)
                self.index = 0

            async def update_message(self, interaction: discord.Interaction):
                embed = make_embed_for(self.index)
                await interaction.response.edit_message(embed=embed, view=self)

            @ui.button(label="⏮️", style=discord.ButtonStyle.secondary)
            async def first(self, interaction: discord.Interaction, button: ui.Button):
                self.index = 0
                await self.update_message(interaction)

            @ui.button(label="◀️", style=discord.ButtonStyle.primary)
            async def prev(self, interaction: discord.Interaction, button: ui.Button):
                self.index = max(0, self.index - 1)
                await self.update_message(interaction)

            @ui.button(label="▶️", style=discord.ButtonStyle.primary)
            async def next(self, interaction: discord.Interaction, button: ui.Button):
                self.index = min(len(ordered_ids) - 1, self.index + 1)
                await self.update_message(interaction)

            @ui.button(label="⏭️", style=discord.ButtonStyle.secondary)
            async def last(self, interaction: discord.Interaction, button: ui.Button):
                self.index = len(ordered_ids) - 1
                await self.update_message(interaction)

            @ui.button(label="❌ Close", style=discord.ButtonStyle.danger)
            async def close(self, interaction: discord.Interaction, button: ui.Button):
                for child in list(self.children):
                    # child is a discord.ui.Item which may wrap a Button; safely set disabled
                    if isinstance(child, ui.Button):
                        child.disabled = True
                    else:
                        try:
                            setattr(child, "disabled", True)
                        except Exception:
                            pass
                await interaction.response.edit_message(view=self)
                self.stop()

        view = WeaponPager()
        embed0 = make_embed_for(0)
        await interaction.followup.send(embed=embed0, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(WeaponData(bot))
