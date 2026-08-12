import socket
import asyncio
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}portcheck <host> <port1,port2,...>", "Cek status port (max 10 port sekaligus)", "OSINT")

MAX_PORTS = 10


def _check_ports(host, ports):
    results = {}
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, port))
            results[port] = (result == 0)
            sock.close()
        except Exception:
            results[port] = False
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}portcheck (\S+) ([\d,]+)$"))
async def portcheck_handler(event):
    host = event.pattern_match.group(1)
    ports_str = event.pattern_match.group(2)

    try:
        ports = [int(p) for p in ports_str.split(",") if p.strip()][:MAX_PORTS]
    except ValueError:
        await event.edit("⚠️ Format port salah, contoh: `80,443,22`")
        return

    await event.edit(f"🔌 Cek {len(ports)} port di {host}...")
    try:
        results = await asyncio.to_thread(_check_ports, host, ports)
        lines = []
        for port, is_open in results.items():
            mark = "🟢 Open" if is_open else "🔴 Closed/Filtered"
            lines.append(f"Port {port}: {mark}")
        await event.edit(f"🔌 **{host}**\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
