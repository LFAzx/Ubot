import io
import asyncio
from datetime import datetime
from telethon import events
from PIL import Image, ImageDraw, ImageFont

from client import client, PREFIX, register

register(f"{PREFIX}sert <nama>", "Generate sertifikat apresiasi cyber custom", "Fun")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def _generate_certificate(name):
    width, height = 1200, 800
    img = Image.new("RGB", (width, height), "#0d1b2a")
    draw = ImageDraw.Draw(img)

    draw.rectangle([20, 20, width - 20, height - 20], outline="#e0a458", width=6)
    draw.rectangle([35, 35, width - 35, height - 35], outline="#e0a458", width=2)

    try:
        font_title = ImageFont.truetype(FONT_BOLD, 54)
        font_sub = ImageFont.truetype(FONT_REGULAR, 26)
        font_name = ImageFont.truetype(FONT_BOLD, 60)
        font_small = ImageFont.truetype(FONT_REGULAR, 22)
    except Exception:
        font_title = font_sub = font_name = font_small = ImageFont.load_default()

    def center_text(y, text, font, fill):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((width - w) / 2, y), text, font=font, fill=fill)

    center_text(110, "SERTIFIKAT APRESIASI", font_title, "#e0a458")
    center_text(190, "CYBER SECURITY EXCELLENCE", font_sub, "#ffffff")
    center_text(320, "Diberikan kepada:", font_small, "#cccccc")
    center_text(370, name, font_name, "#ffffff")
    draw.line([(300, 470), (900, 470)], fill="#e0a458", width=2)

    today = datetime.now().strftime("%d %B %Y")
    center_text(600, f"Diterbitkan pada {today}", font_small, "#cccccc")
    center_text(650, "— SilentCyber Userbot —", font_small, "#e0a458")

    buf = io.BytesIO()
    buf.name = "sertifikat.png"
    img.save(buf, "PNG")
    buf.seek(0)
    return buf


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}sert (.+)$"))
async def sert_handler(event):
    name = event.pattern_match.group(1)
    await event.edit("🏆 Generate sertifikat...")
    try:
        buf = await asyncio.to_thread(_generate_certificate, name)
        await event.delete()
        await client.send_file(event.chat_id, buf, caption=f"🏆 Sertifikat untuk {name}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
