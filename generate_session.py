"""
Jalankan file ini SEKALI di Termux (lokal) untuk generate SESSION_STRING.
JANGAN dijalankan di Railway.

Cara pakai:
    python generate_session.py

Nanti akan diminta:
- API_ID dan API_HASH (ambil dari https://my.telegram.org -> API Development Tools)
- Nomor HP kamu (format internasional, contoh: +6281234567890)
- Kode OTP yang dikirim Telegram
- Password 2FA (kalau aktif)

Setelah selesai, SESSION_STRING akan ditampilkan di layar.
COPY dan simpan baik-baik string itu -> itu setara dengan password akun Telegram kamu.
Masukkan ke Railway sebagai environment variable SESSION_STRING.
"""

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("API_ID: ").strip())
api_hash = input("API_HASH: ").strip()

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print("\n=== SESSION_STRING KAMU (JANGAN SEBAR KE SIAPA PUN) ===\n")
    print(session_string)
    print("\n========================================================")
    print("Simpan string di atas, masukkan sebagai env var SESSION_STRING di Railway.")

