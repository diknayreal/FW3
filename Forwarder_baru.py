# source by telegram > @abimanyu_real

from telethon import TelegramClient, events
import time
import logging
import asyncio

# Konfigurasi logging
logging.basicConfig(filename='forward_telethon.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Informasi akun Telegram Anda
api_id = 'disini'  # Ganti dengan API ID Anda
api_hash = 'disini'  # Ganti dengan API Hash Anda
phone_number = '+disini'  # Ganti dengan nomor telepon Anda

# Link pesan yang ingin Anda forward
message_link = "disini"  # Ganti dengan link pesan yang ingin diforward

# Waktu berhenti dalam jam contoh seharian (24 * 60 * 60)
stop_time = time.time() + (720 * 60 * 60)  

# Jeda antara pengiriman (misal: 300 detik = 5 menit untuk menghindari batasan Telegram)
delay_between_messages = 120

# Batasi jumlah grup yang ingin diforward dalam satu kali proses untuk menghindari masalah dengan Telegram
max_groups = 30  # Ubah sesuai kebutuhan

# Buat client Telethon dengan file session
client = TelegramClient('my_account.session', api_id, api_hash)

async def forward_message_to_group(from_chat_id, message_id, group_id):
    try:
        await client.forward_messages(group_id, message_id, from_chat_id)
        logging.info(f"Pesan berhasil diforward ke grup ID: {group_id}")
        print(f"Pesan berhasil diforward ke grup ID: {group_id}")  # Cetak ke terminal
    except Exception as e:
        logging.error(f"Gagal forward pesan ke grup ID {group_id}: {str(e)}")

async def send_message_to_all_groups(from_chat_id, message_id):
    try:
        dialogs = await client.get_dialogs()
        groups = [d for d in dialogs if d.is_group]

        logging.info(f"Total grup ditemukan: {len(groups)}")
        if not groups:
            logging.warning("Tidak ada grup ditemukan. Pastikan akun ini sudah join grup.")
            return

        # Batasi grup yang akan diproses
        groups = groups[:max_groups]
        tasks = []  # List untuk menyimpan task

        for group in groups:
            logging.info(f"Memulai forward pesan ke grup ID: {group.id}")
            tasks.append(forward_message_to_group(from_chat_id, message_id, group.id))  # Tambahkan task ke list

        await asyncio.gather(*tasks)  # Jalankan semua task secara serentak
        logging.info("Pesan selesai diforward ke semua grup yang dibatasi.")
        
    except Exception as e:
        logging.error(f"Terjadi kesalahan saat mengirim pesan: {str(e)}")

async def main():
    try:
        logging.info("Memulai program...")
        from_chat_username = message_link.split('/')[-2]  # Username/channel dari link
        message_id = int(message_link.split('/')[-1])  # ID pesan dari link
        logging.info(f"Username: {from_chat_username}, Message ID: {message_id}")

        await client.start(phone_number)  # Start client with phone number
        logging.info("Client berhasil terhubung.")

        # Dapatkan chat ID dari channel/group source
        from_chat = await client.get_entity(from_chat_username)
        from_chat_id = from_chat.id
        logging.info(f"Dari chat ID: {from_chat_id}")

        while time.time() < stop_time:  # Looping sampai waktu berhenti tercapai
            logging.info("Mengirim pesan ke semua grup yang ditemukan...")
            await send_message_to_all_groups(from_chat_id, message_id)
            logging.info(f"Menunggu {delay_between_messages} detik sebelum forward berikutnya...")
            await asyncio.sleep(delay_between_messages)  # Jeda antar forward

    except Exception as e:
        logging.error(f"Gagal menjalankan program: {str(e)}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())