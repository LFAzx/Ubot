import phonenumbers
from phonenumbers import geocoder, carrier as pn_carrier
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}phoneinfo <nomor>", "Cek negara & carrier nomor telepon (offline)", "OSINT")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}phoneinfo (\+?\d+)$"))
async def phoneinfo_handler(event):
    number = event.pattern_match.group(1)
    try:
        parsed = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed):
            await event.edit("⚠️ Nomor gak valid. Pakai format internasional (misal +6281234567890).")
            return

        country = geocoder.description_for_number(parsed, "id")
        operator = pn_carrier.name_for_number(parsed, "id") or "?"

        text = (
            f"📱 **{number}**\n"
            f"Negara: {country}\n"
            f"Operator: {operator}\n"
            f"Valid: ✅"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
