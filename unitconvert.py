from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}unitconvert <nilai> <dari> <ke>", "Convert satuan (km/mile, kg/lb, celsius/fahrenheit, dll)", "Utility")

CONVERSIONS = {
    ("km", "mile"): lambda v: v * 0.621371,
    ("mile", "km"): lambda v: v / 0.621371,
    ("kg", "lb"): lambda v: v * 2.20462,
    ("lb", "kg"): lambda v: v / 2.20462,
    ("m", "ft"): lambda v: v * 3.28084,
    ("ft", "m"): lambda v: v / 3.28084,
    ("liter", "gallon"): lambda v: v * 0.264172,
    ("gallon", "liter"): lambda v: v / 0.264172,
    ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
    ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
    ("kg", "gram"): lambda v: v * 1000,
    ("gram", "kg"): lambda v: v / 1000,
}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}unitconvert ([\d.]+) (\S+) (\S+)$"))
async def unitconvert_handler(event):
    value = float(event.pattern_match.group(1))
    from_unit = event.pattern_match.group(2).lower()
    to_unit = event.pattern_match.group(3).lower()

    key = (from_unit, to_unit)
    if key not in CONVERSIONS:
        supported = ", ".join(f"{a}->{b}" for a, b in CONVERSIONS.keys())
        await event.edit(f"⚠️ Konversi gak didukung. Yang ada:\n{supported}")
        return

    result = CONVERSIONS[key](value)
    await event.edit(f"🔄 {value} {from_unit} = **{result:.4f} {to_unit}**")
