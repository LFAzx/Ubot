import calendar
from datetime import datetime
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}age <YYYY-MM-DD>", "Hitung umur persis dari tanggal lahir", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}age (\d{{4}}-\d{{2}}-\d{{2}})$"))
async def age_handler(event):
    date_str = event.pattern_match.group(1)
    try:
        birth = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()

        years = today.year - birth.year
        months = today.month - birth.month
        days = today.day - birth.day

        if days < 0:
            months -= 1
            prev_month = today.month - 1 or 12
            prev_year = today.year if today.month > 1 else today.year - 1
            days += calendar.monthrange(prev_year, prev_month)[1]
        if months < 0:
            years -= 1
            months += 12

        total_days = (today - birth).days

        await event.edit(
            f"🎂 **Umur dari {date_str}:**\n"
            f"{years} tahun, {months} bulan, {days} hari\n"
            f"(total {total_days:,} hari)"
        )
    except Exception as e:
        await event.edit(f"❌ Error: {e} (format: YYYY-MM-DD)")
