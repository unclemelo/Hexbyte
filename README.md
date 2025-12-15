# 🐛 Buggy

**Maintained by UncleMelo**
Built for the **WTF community** to track stats and expose in-game data.

---

## ✨ Overview

**Buggy** is a Discord bot designed to surface game data for the WTF community. It provides clean, easy-to-use **slash commands** for viewing levels, weapons, and player-related stats, all powered by structured JSON data and optional external APIs.

The bot focuses on:

* Clear stat presentation
* Fast slash-command interactions
* Modular cog-based architecture

---

## 🤖 Commands

### 📈 `/levelinfo`

Explains how the leveling system works using `data/levels.json`, including:

* XP thresholds per level
* Example progression milestones
* XP reward sources

### 🔫 `/weaponinfo`

Opens an interactive, **paged weapon viewer**.

Features:

* Button-based navigation
* Detailed weapon stats
* Automatic image display when `Image` or `SideImage` URLs are present in the data

### 📊 `/wtfstats <steamid>`

Fetches a player’s stats from the configured API and returns:

* A generated stat image
* A summarized breakdown of key values

### 🏆 `/wtfleaderboard`

Displays a leaderboard embed.

> ⚠️ Currently uses mock/test data and is intended for layout and feature testing.

### 🛠️ Developer / Maintenance Commands

The following commands are intended for development and maintenance use (see `updater.py`):

* `/update` — Run the update system
* `/update_commits` — View recent commits
* `/update_reload` — Reload updated modules
* `/update_status` — Check updater status
* `/update_info` — View updater configuration and metadata

---

## 🗂️ Data Files

| File                | Description                                     |
| ------------------- | ----------------------------------------------- |
| `data/levels.json`  | Level thresholds and `XPRewards` configuration  |
| `data/weapons.json` | Weapon stat definitions and optional image URLs |

---

## 🧪 Running Locally

### 1️⃣ Environment Setup

Create a `.env` file in the project root:

```env
TOKEN=your_bot_token_here
```

### 2️⃣ Virtual Environment & Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3️⃣ Run the Bot

```powershell
python bot.py
```

On startup, Buggy will:

* Load all cogs from the `cogs/` directory
* Sync slash commands automatically

---

## 📦 Dependencies

Buggy relies on the following Python packages:

* **discord.py (v2.x)** — slash commands & UI components
* **python-dotenv** — environment variable loading
* **aiohttp** — async HTTP requests
* **Pillow** — stat card image generation
* **colorama** — colored console logging
* **requests** — webhook and error reporting

### Example `requirements.txt`

```txt
discord.py>=2.0.0
python-dotenv
aiohttp
Pillow
colorama
requests
```

---

## 🔐 `.env` Configuration

Supported environment variables:

| Key        | Required | Description                          |
| ---------- | -------- | ------------------------------------ |
| `TOKEN`    | ✅        | Discord bot token                    |
| `API_LINK` | ❌        | Base API URL used by `cogs/stats.py` |
| `WEBHOOK`  | ❌        | Discord webhook for error reporting  |

Example:

```env
TOKEN=your_bot_token_here
API_LINK=https://api.example.com/
WEBHOOK=https://discord.com/api/webhooks/...
```

---

## 🛠️ Development Notes

* All cogs must expose:

```py
async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

* `/weaponinfo` automatically displays images if valid URLs are present in the weapon JSON
* For faster slash-command iteration, consider **guild-specific syncing** during development instead of global sync

---

## 📌 Additional Notes

* Weapon images are optional but recommended for a richer UI
* JSON schemas are flexible but should remain consistent to avoid runtime errors
* Error handling supports webhook-based reporting if configured

---

## 🤝 Contributing

Contributions are welcome!

* Open an issue for bugs or feature requests
* Submit a PR to improve commands, visuals, or data structures
* Help expand weapon or level datasets

Built with ❤️ for the WTF community.
