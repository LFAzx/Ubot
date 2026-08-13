from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}bmi <berat_kg> <tinggi_cm>", "Hitung BMI + kategori", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}bmi ([\d.]+) ([\d.]+)$"))
async def bmi_handler(event):
    weight = float(event.pattern_match.group(1))
    height_cm = float(event.pattern_match.group(2))
    height_m = height_cm / 100

    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category = "Berat badan kurang"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Berat badan berlebih"
    else:
        category = "Obesitas"

    await event.edit(f"⚖️ **BMI: {bmi:.1f}**\nKategori: {category}")
