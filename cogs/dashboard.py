import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

class Dashboard(commands.Cog):
    """Cog that provides a dashboard for reporting bugs."""

    def __init__(self, bot):
        self.bot = bot

    def build_dashboard_view(self):
        view = ui.View()

        report_button = ui.Button(label="Report Bug", emoji="<:AA_Noted:1448897319444680917>", style=discord.ButtonStyle.gray, custom_id="dashboard:report")
        support_button = ui.Button(label="Get Support", emoji="<:Erm:1448898129310257172>", style=discord.ButtonStyle.gray, custom_id="dashboard:support")
        docs_button = ui.Button(label="Docs", style=discord.ButtonStyle.gray, custom_id="dashboard:docs")

        report_button.callback = self._report_button_callback
        support_button.callback = self._support_button_callback
        docs_button.callback = self._docs_button_callback

        view.add_item(report_button)
        view.add_item(support_button)
        view.add_item(docs_button)
        return view

    @app_commands.command(name="dashboard", description="Show the dashboard for reporting bugs.")
    async def dashboard(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # Create a advanced embed for the dashboard with buttons
        embed = discord.Embed(
            title="🛠️ WTF Dashboard",
            description="Use the buttons below to report bugs or get support.",
            color=discord.Color.orange()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        # if user has a dev roles add extra more buttons and info
        member = interaction.guild.get_member(interaction.user.id) if interaction.guild else None
        if member and any(role.id in [954135885392252940] for role in member.roles):
            embed.add_field(
                name="Developer Options",
                value="As a developer, you have access to additional options in the dashboard.",
                inline=False
            )
        
        view = self.build_dashboard_view()
        await interaction.followup.send(embed=embed, view=view)

    # Button callbacks: keep these small and focused. They respond ephemerally #
    ############################################################################
    async def _report_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "In Development: Bug reporting functionality is coming soon!",
            ephemeral=True,
        )

    async def _support_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "In Development: Support functionality is coming soon! (Aka: This will be ModMail or similar)",
            ephemeral=True,
        )

    async def _docs_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"In Development: Documentation is coming soon!",
            ephemeral=True,
        )

async def setup(bot):
    await bot.add_cog(Dashboard(bot))