from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

import os

TOKEN = os.getenv("BOT_TOKEN")  # Ganti dengan token BotFather
# ================= INFO LUMENSIA =================
info_lumensia = "🌟 *PT LUMENSIA SMART TECHNOLOGIE*\n\n_Hallo Sobat! Selamat bergabung dalam kebersamaan. Green Energy Smart Living for Future Generation_"

visi = """
*Visi:*
Menjadi pelopor solusi properti berbasis teknologi pintar dan terintegrasi digital yang mendukung kemudahan hidup masyarakat serta memperkuat kemandirian ekonomi komunitas melalui inovasi berkelanjutan.
"""

misi = """
*Misi:*
1. Mengembangkan produk dan layanan smart home yang terjangkau dan berkualitas.
2. Mendorong integrasi teknologi digital dengan sektor properti.
3. Membangun kolaborasi dengan komunitas, asosiasi, dan lembaga keuangan.
4. Menjadi jembatan dalam transformasi digital properti menuju era blockchain dan Web3.
"""

target_pendek = """
*🎯 Target Jangka Pendek (Pencapaian):*
• Legalitas resmi (badan hukum, NIB, SIUP, NPWP) telah terverifikasi sukses.
• Tergabung aktif dengan asosiasi developer properti.
• *Update:* Sedang dalam tahap penjajakan kemitraan strategis dengan developer perumahan subsidi untuk kolaborasi proyek pilot ke depan.
"""

target_panjang = """
*🚀 Target Jangka Panjang (2026-2030):*
• Integrasi penuh dengan ekosistem Pi Network.
• Menjadi pionir properti berbasis Pi (Wallet SDK Testnet, Pi Venture).
• *Keberhasilan Listing:* Token LUME berhasil listing dan diperdagangkan dalam ekosistem Pi Tokens.
• Siap menghadapi Open Mainnet dan implementasi transaksi properti berbasis Pi secara masif.
"""
# ================= DATA TIPE RUMAH =================
tipe_rumah = [
    {
        "judul": "🏡 Basic (Elite Entry)",
        "deskripsi": "• Luas: 130 m² | Harga: 0.25 Pi\n• 3 Kamar Tidur, 2 Kamar Mandi, 1 Carport\n• Smart door lock, CCTV basic, listrik 3500 VA, dapur bersih & kotor, lantai granit premium 60x60"
    },
    {
        "judul": "🏡 Standar (Luxury)",
        "deskripsi": "• Luas: 150 m² | Harga: 0.5 Pi\n• 3+1 (ART) Kamar Tidur, 3 Kamar Mandi, 2 Carport\n• Balkon, smart home basic, CCTV 4 titik, listrik 4400 VA, lantai granit 80x80"
    },
    {
        "judul": "🏡 Premium",
        "deskripsi": "• Luas: 190 m² | Harga: 1 Pi\n• 4+1 (ART) Kamar Tidur, 4 Kamar Mandi, 2 Carport\n• Smart home lengkap, balkon luas, mini bar, CCTV 6 titik, listrik 5500 VA, lantai granit 100x100 premium"
    },
    {
        "judul": "🏡 Ultimate (Luxury Mansion)",
        "deskripsi": "• Luas: 225–250 m² | Harga: 2 Pi\n• 5+1 (ART) Kamar Tidur, 5 Kamar Mandi, 3 Carport\n• Smart home full, home theater, ruang kerja, rooftop garden, CCTV 8 titik, listrik 7700 VA, lantai marmer premium"
    }
]

# ================= MENU BUTTON =================
def get_menu():
    keyboard = [
        [InlineKeyboardButton("🌟 Visi", callback_data="visi")],
        [InlineKeyboardButton("📜 Misi", callback_data="misi")],
        [InlineKeyboardButton("🎯 Target Jangka Pendek", callback_data="pendek")],
        [InlineKeyboardButton("🚀 Target Jangka Panjang", callback_data="panjang")],
        [InlineKeyboardButton("🏡 Daftar Tipe Rumah", callback_data="rumah_0")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_rumah_keyboard(index):
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"rumah_{index-1}"))
    if index < len(tipe_rumah)-1:
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"rumah_{index+1}"))
    buttons.append(InlineKeyboardButton("🏠 Menu Utama", callback_data="menu"))
    return InlineKeyboardMarkup([buttons])

# ================= HANDLER =================
async def start(update: Update, context):
    await update.message.reply_text(
        f"{info_lumensia}\n\nPilih informasi yang ingin kamu lihat:",
        reply_markup=get_menu(),
        parse_mode="Markdown"
    )

async def welcome(update: Update, context):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"Selamat datang {member.full_name}! 🎉\n\n{info_lumensia}\n\nPilih informasi yang ingin kamu lihat:",
            reply_markup=get_menu(),
            parse_mode="Markdown"
        )

async def button_click(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "visi":
        await query.edit_message_text(text=visi, parse_mode="Markdown", reply_markup=get_menu())
    elif query.data == "misi":
        await query.edit_message_text(text=misi, parse_mode="Markdown", reply_markup=get_menu())
    elif query.data == "pendek":
        await query.edit_message_text(text=target_pendek, parse_mode="Markdown", reply_markup=get_menu())
    elif query.data == "panjang":
        await query.edit_message_text(text=target_panjang, parse_mode="Markdown", reply_markup=get_menu())
    elif query.data.startswith("rumah_"):
        index = int(query.data.split("_")[1])
        rumah = tipe_rumah[index]
        await query.edit_message_text(
            text=f"*{rumah['judul']}*\n{rumah['deskripsi']}",
            parse_mode="Markdown",
            reply_markup=get_rumah_keyboard(index)
        )
    elif query.data == "menu":
        await query.edit_message_text(
            text=f"{info_lumensia}\n\nPilih informasi yang ingin kamu lihat:",
            reply_markup=get_menu(),
            parse_mode="Markdown"
        )

# ================= JALANKAN BOT =================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(CallbackQueryHandler(button_click))

print("Bot berjalan...")
app.run_polling()

