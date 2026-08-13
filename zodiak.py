from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}zodiak <DD-MM>", "Cek zodiak dari tanggal lahir", "Fun")

ZODIAC_RANGES = [
    ((1, 20), (2, 18), "Aquarius"),
    ((2, 19), (3, 20), "Pisces"),
    ((3, 21), (4, 19), "Aries"),
    ((4, 20), (5, 20), "Taurus"),
    ((5, 21), (6, 20), "Gemini"),
    ((6, 21), (7, 22), "Cancer"),
    ((7, 23), (8, 22), "Leo"),
    ((8, 23), (9, 22), "Virgo"),
    ((9, 23), (10, 22), "Libra"),
    ((10, 23), (11, 21), "Scorpio"),
    ((11, 22), (12, 21), "Sagittarius"),
    ((12, 22), (1, 19), "Capricorn"),
]


def _get_zodiac(day, month):
    for start, end, name in ZODIAC_RANGES:
        start_month, start_day = start
        end_month, end_day = end
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return name
    return "?"


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}zodiak (\d{{1,2}})-(\d{{1,2}})$"))
async def zodiak_handler(event):
    day = int(event.pattern_match.group(1))
    month = int(event.pattern_match.group(2))
    zodiac = _get_zodiac(day, month)
    await event.edit(f"♈ **Zodiak: {zodiac}**")
