import os
from aiohttp import web

from drive_auth import handle_callback


async def oauth_callback_handler(request):
    code = request.query.get("code")
    state = request.query.get("state")
    if not code or not state:
        return web.Response(text="Missing code/state parameter.", status=400)

    user_id = handle_callback(state, code)
    if user_id is None:
        return web.Response(text="Link ini udah gak valid/expired. Coba .drive connect lagi.", status=400)

    return web.Response(text="✅ Google Drive berhasil terhubung! Kamu bisa balik ke Telegram sekarang.")


async def start_webserver():
    app = web.Application()
    app.router.add_get("/oauth/callback", oauth_callback_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
