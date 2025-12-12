import io
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# --- Level progression ---
LEVEL_PROGRESSION = {1:0,2:4000,3:8000,4:10000,5:13200,6:26400,7:52800,8:16000,9:18000,10:20000,
    11:22000,12:24000,13:26000,14:28000,15:30000,16:32000,17:34000,18:36000,
    19:38000,20:40000,21:42000,22:44000,23:46000,24:48000,25:50000,26:52000,
    27:54000,28:56000,29:58000,30:60000,31:62000,32:64000,33:66000,34:68000,
    35:70000,36:72000,37:74000,38:76000,39:78000,40:80000,41:82000,42:84000,
    43:86000,44:88000,45:90000,46:92000,47:94000,48:96000,49:98000,50:100000,
    51:102000,52:104000,53:106000,54:108000,55:110000,56:112000,57:114000,
    58:116000,59:118000,60:120000,61:122000,62:124000,63:126000,64:128000,
    65:130000,66:132000,67:134000,68:136000,69:138000,70:140000,71:142000,
    72:144000,73:146000,74:148000,75:150000,76:152000,77:154000,78:156000,
    79:158000,80:160000,81:162000,82:164000,83:166000,84:168000,85:170000,
    86:172000,87:174000,88:176000,89:178000,90:180000,91:182000,92:184000,
    93:186000,94:188000,95:190000,96:192000,97:194000,98:196000,99:198000,
    100:200000
}

def load_font(size=20):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            return ImageFont.load_default()

def get_progress(level: int, xp: int):
    if level >= 100:
        return 1.0, "MAX LEVEL", 0, 0
    current_req = LEVEL_PROGRESSION.get(level, 0)
    next_req = LEVEL_PROGRESSION.get(level + 1, current_req)
    xp_into_level = max(0, xp - current_req)
    xp_needed = max(1, next_req - current_req)
    progress = max(0.0, min(1.0, xp_into_level / xp_needed))
    return progress, f"{xp_into_level} / {xp_needed}", xp_into_level, xp_needed

def generate_stats_image(data: dict, width=900, height=520) -> io.BytesIO:
    W, H = width, height

    # ---- Anime colors ----
    color_bg = (35, 31, 32)           # #231f20
    color_accent = (217, 254, 0)      # #d9fe00
    color_secondary = (145, 180, 240) # #91b4f0
    color_text = (235, 235, 235)
    color_muted = (160, 160, 160)
    color_card = (50, 46, 48)         # slightly lighter than bg
    color_bar_bg = (80, 70, 72)       # bar background

    img = Image.new("RGB", (W, H), color_bg)
    draw = ImageDraw.Draw(img)

    font_title = load_font(46)
    font_level = load_font(44)
    font_big = load_font(28)
    font_label = load_font(20)

    padding = 30
    draw.text((padding, padding), "Waifu Tactical Force", fill=color_accent, font=font_title)

    # ---- Circular avatar ----
    circle_size = 120
    circle_x = W - 170
    circle_y = padding
    avatar_box = (circle_x, circle_y, circle_x + circle_size, circle_y + circle_size)

    # Draw background circle
    draw.ellipse(avatar_box, fill=color_secondary)  # nice background behind avatar

    avatar_path = "animegirl.png"
    try:
        avatar = Image.open(avatar_path).convert("RGBA").resize((circle_size, circle_size))
        
        # Create circular mask
        mask = Image.new("L", (circle_size, circle_size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, circle_size, circle_size), fill=255)
        
        # Create transparent avatar circle
        avatar_circle = Image.new("RGBA", (circle_size, circle_size), (0, 0, 0, 0))
        avatar_circle.paste(avatar, (0, 0), mask=mask)
        
        # Paste onto main image using alpha
        img.paste(avatar_circle, (circle_x, circle_y), avatar_circle)
    except:
        draw.text((circle_x + 15, circle_y + 40), "NO IMG", fill=color_muted, font=font_label)

    # ---- Card background ----
    card_x = padding
    card_y = 120
    card_w = W - padding*2
    card_h = H - card_y - padding
    draw.rectangle([card_x, card_y, card_x+card_w, card_y+card_h], fill=color_card)

    # ---- Level and Rounded XP Bar ----
    level = int(data.get("Level", 0))
    xp = int(data.get("TotalXP", 0))
    progress, prog_text, _, _ = get_progress(level, xp)
    level_label = "MAX LEVEL" if level >= 100 else f"Level {level}"
    level_x = card_x + 25
    level_y = card_y + 20
    draw.text((level_x, level_y), level_label, fill=color_accent, font=font_level)

    # Rounded/pill-style bar parameters
    bar_x = level_x
    bar_y = level_y + 64
    bar_w = card_w - 150
    bar_h = 28
    radius = bar_h // 2

    # Draw background bar (full width)
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=radius, fill=color_bar_bg)

    # Draw filled portion
    fill_w = int(bar_w * progress)
    draw.rounded_rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], radius=radius, fill=color_secondary)

    # XP text inside or below the bar
    xp_text = "XP: MAX" if level >= 100 else f"XP: {prog_text} ({int(progress*100)}%)"
    draw.text((bar_x, bar_y + bar_h + 6), xp_text, fill=color_text, font=font_label)



    # ---- Stats ----
    left_x = level_x
    left_y = bar_y + 80
    line_h = 36
    kills = int(data.get("TotalKills",0))
    deaths = int(data.get("TotalDeaths",0))
    assists = int(data.get("TotalAssists",0))
    total_shots = int(data.get("TotalShotsFired",0))
    hit_shots = int(data.get("TotalShotsHit",0))
    accuracy = round((hit_shots / total_shots) * 100, 1) if total_shots>0 else 0
    kd = round(kills/deaths,2) if deaths>0 else float(kills)

    draw.text((left_x, left_y), f"Kills: {kills}", fill=color_text, font=font_big)
    draw.text((left_x, left_y+line_h), f"Deaths: {deaths}", fill=color_text, font=font_big)
    draw.text((left_x, left_y+line_h*2), f"Assists: {assists}", fill=color_text, font=font_big)
    draw.text((left_x, left_y+line_h*3), f"K/D: {kd}", fill=color_text, font=font_big)
    draw.text((left_x, left_y+line_h*4), f"Accuracy: {accuracy}%", fill=color_text, font=font_big)

    right_x = card_x + card_w//2 + 10
    right_y = left_y
    matches = int(data.get("TotalMatches",0))
    wins = int(data.get("MatchesWon",0))
    losses = int(data.get("MatchesLost",0))
    dmg_dealt = int(data.get("TotalDamageDealt",0))
    dmg_taken = int(data.get("TotalDamageTaken",0))
    score = int(data.get("TotalScore",0))

    draw.text((right_x, right_y), f"Matches: {matches}", fill=color_text, font=font_big)
    draw.text((right_x, right_y+line_h), f"W/L: {wins}/{losses}", fill=color_text, font=font_big)
    draw.text((right_x, right_y+line_h*2), f"Damage Dealt: {dmg_dealt}", fill=color_text, font=font_big)
    draw.text((right_x, right_y+line_h*3), f"Damage Taken: {dmg_taken}", fill=color_text, font=font_big)
    draw.text((right_x, right_y+line_h*4), f"Score: {score}", fill=color_text, font=font_big)

    # ---- Footer ----
    footer_y = card_y + card_h - 25
    updated_raw = data.get("LastUpdated","Unknown")
    try:
        dt = datetime.fromisoformat(updated_raw)
        updated = dt.strftime("%b %d, %Y %H:%M")
    except:
        updated = updated_raw

    draw.text((card_x + 25, footer_y), f"Last Updated: {updated}", fill=color_muted, font=font_label)
    draw.text((W - 300, footer_y), "WTF Game — Player Stats", fill=color_muted, font=font_label)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
