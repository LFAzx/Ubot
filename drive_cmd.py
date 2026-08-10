import io
import re
import asyncio
from telethon import events
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

from client import client, PREFIX, register
from drive_auth import build_auth_url, get_credentials, disconnect

register(f"{PREFIX}drive connect", "Hubungkan akun Google Drive", "Drive")
register(f"{PREFIX}drive disconnect", "Putus koneksi Google Drive", "Drive")
register(f"{PREFIX}drive save", "Reply file/foto untuk disimpan ke Drive", "Drive")
register(f"{PREFIX}drive download <link_gdrive>", "Copy file dari link Drive orang lain ke Drive kamu", "Drive")
register(f"{PREFIX}drive list <tipe>", "List file di Drive (png/jpg/img/file/zip/dst, kosong = semua)", "Drive")
register(f"{PREFIX}drive remove <nama_file>", "Hapus file dari Drive", "Drive")
register(f"{PREFIX}drive send <nama_file>", "Kirim file dari Drive ke Telegram", "Drive")

TYPE_MIMES = {
    "png": ["image/png"],
    "jpg": ["image/jpeg"],
    "jpeg": ["image/jpeg"],
    "gif": ["image/gif"],
    "zip": ["application/zip"],
    "pdf": ["application/pdf"],
    "img": ["image/png", "image/jpeg", "image/gif", "image/webp"],
}


def _get_service(user_id):
    creds = get_credentials(user_id)
    if not creds:
        return None
    return build("drive", "v3", credentials=creds)


def _do_save(user_id, file_bytes, filename, mimetype):
    service = _get_service(user_id)
    media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mimetype, resumable=False)
    return service.files().create(body={"name": filename}, media_body=media, fields="id, webViewLink").execute()


def _do_copy(user_id, file_id):
    service = _get_service(user_id)
    return service.files().copy(fileId=file_id, fields="id, name, webViewLink").execute()


def _do_list(user_id, filter_type):
    service = _get_service(user_id)
    query = None
    if filter_type == "img":
        query = " or ".join(f"mimeType='{m}'" for m in TYPE_MIMES["img"])
    elif filter_type == "file":
        query = " and ".join(f"mimeType!='{m}'" for m in TYPE_MIMES["img"])
    elif filter_type and filter_type in TYPE_MIMES:
        query = " or ".join(f"mimeType='{m}'" for m in TYPE_MIMES[filter_type])

    results = service.files().list(q=query, pageSize=20, fields="files(id, name, webViewLink)").execute()
    return results.get("files", [])


def _do_remove(user_id, filename):
    service = _get_service(user_id)
    results = service.files().list(q=f"name='{filename}'", fields="files(id, name)").execute()
    files = results.get("files", [])
    for f in files:
        service.files().delete(fileId=f["id"]).execute()
    return len(files)


def _do_get_bytes(user_id, filename):
    service = _get_service(user_id)
    results = service.files().list(q=f"name='{filename}'", fields="files(id, name)").execute()
    files = results.get("files", [])
    if not files:
        return None

    file_id = files[0]["id"]
    request = service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    buf.seek(0)
    return buf


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}drive connect$"))
async def drive_connect_handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    if get_credentials(user_id):
        await event.edit("✅ Drive kamu udah terhubung. Pakai `.drive disconnect` dulu kalau mau ganti akun.")
        return

    url = build_auth_url(user_id)
    await event.edit(f"🔗 Klik link ini buat hubungin Google Drive kamu:\n{url}\n\nSetelah approve di Google, balik ke sini.")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}drive disconnect$"))
async def drive_disconnect_handler(event):
    sender = await event.get_sender()
    disconnect(sender.id)
    await event.edit("🔌 Drive udah diputus koneksinya.")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}drive save$"))
async def drive_save_handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    if not get_credentials(user_id):
        await event.edit("⚠️ Drive belum terhubung. Pakai `.drive connect` dulu.")
        return

    if not event.is_reply:
        await event.edit("⚠️ Reply ke file/foto yang mau disimpan.")
        return

    reply = await event.get_reply_message()
    if not (reply.photo or reply.document):
        await event.edit("⚠️ Pesan yang di-reply harus berupa file atau foto.")
        return

    await event.edit("☁️ Upload ke Drive...")
    try:
        file_bytes = await client.download_media(reply, file=bytes)

        filename = "file"
        mimetype = "application/octet-stream"
        if reply.document:
            for attr in reply.document.attributes:
                if hasattr(attr, "file_name"):
                    filename = attr.file_name
            mimetype = reply.document.mime_type or mimetype
        elif reply.photo:
            filename = "photo.jpg"
            mimetype = "image/jpeg"

        result = await asyncio.to_thread(_do_save, user_id, file_bytes, filename, mimetype)
        await event.edit(f"☁️ Tersimpan: **{filename}**\n{result.get('webViewLink')}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}drive download (\S+)$"))
async def drive_download_handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    if not get_credentials(user_id):
        await event.edit("⚠️ Drive belum terhubung. Pakai `.drive connect` dulu.")
        return

    link = event.pattern_match.group(1)
    match = re.search(r"[-\w]{25,}", link)
    if not match:
        await event.edit("⚠️ Gak nemu file ID dari link itu. Pastikan itu link Google Drive yang valid.")
        return
    file_id = match.group(0)

    await event.edit("☁️ Copy file ke Drive kamu...")
    try:
        result = await asyncio.to_thread(_do_copy, user_id, file_id)
        await event.edit(f"☁️ Ter-copy: **{result.get('name')}**\n{result.get('webViewLink')}")
    except Exception as e:
        await event.edit(f"❌ Error: {e} (pastikan file di-share/accessible)")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}drive list(?:\s(\S+))?$"))
async def drive_list_handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    if not get_credentials(user_id):
        await event.edit("⚠️ Drive belum terhubung. Pakai `.drive connect` dulu.")
        return

    filter_type = event.pattern_match.group(1)

    await event.edit("☁️ Ambil list file...")
    try:
        files = await asyncio.to_thread(_do_list, user_id, filter_type)
        if not files:
            await event.edit("📭 Gak ada file yang ketemu.")
            return

        lines = [f"- {f['name']}" for f in files]
        await event.edit(f"☁️ **Files di Drive** ({filter_type or 'semua'}):\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}drive remove (.+)$"))
async def drive_remove_handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    if not get_credentials(user_id):
        await event.edit("⚠️ Drive belum terhubung. Pakai `.drive connect` dulu.")
        return

    filename = event.pattern_match.group(1)

    await event.edit("☁️ Cari & hapus file...")
    try:
        count = await asyncio.to_thread(_do_remove, user_id, filename)
        if count == 0:
            await event.edit(f"❌ File `{filename}` gak ketemu.")
            return
        await event.edit(f"🗑️ **{filename}** dihapus dari Drive.")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}drive send (.+)$"))
async def drive_send_handler(event):
    sender = await event.get_sender()
    user_id = sender.id

    if not get_credentials(user_id):
        await event.edit("⚠️ Drive belum terhubung. Pakai `.drive connect` dulu.")
        return

    filename = event.pattern_match.group(1)

    await event.edit("☁️ Cari & download file...")
    try:
        buf = await asyncio.to_thread(_do_get_bytes, user_id, filename)
        if buf is None:
            await event.edit(f"❌ File `{filename}` gak ketemu.")
            return
        buf.name = filename

        await event.delete()
        await client.send_file(event.chat_id, buf, caption=f"☁️ {filename}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
