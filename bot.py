from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import json

# ================== TAVO DUOMENYS ==================
TOKEN = "8644750183:AAFCk_oXv4v_r1kwIpgxqMztNEfNQwYmBdw"          # ← Pakeisk
ADMIN_ID = 7406366737                         # ← Pakeisk į savo Telegram ID

PRICE = "15€ / vnt"

flavors = {
    "watermelon": "🍉 Watermelon Ice",
    "strawberry": "🍓 Strawberry Ice",
    "blueberry": "🫐 Blueberry Raspberry",
    "grape": "🍇 Grape Ice",
    "mix": "🌈 Mix Fruit"
}

STOCK_FILE = "stock.json"

def load_stock():
    try:
        with open(STOCK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        default = {"watermelon": 45, "strawberry": 32, "blueberry": 28, "grape": 51, "mix": 19}
        save_stock(default)
        return default

def save_stock(stock):
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(stock, f, ensure_ascii=False, indent=2)

stock = load_stock()

bot = Bot(token=TOKEN)
dp = Dispatcher()

def main_menu():
    builder = InlineKeyboardBuilder()
    for code, name in flavors.items():
        builder.button(text=name, callback_data=f"flavor_{code}")
    builder.adjust(1)
    return builder.as_markup()

# ================== START SU NUOTRAUKA ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.delete()
    
    caption = (
        "🔥 **CLOUDAZZ.LT** — Premium Vape Parduotuvė\n\n"
        "🦁 **BANG Leader 20000 Puffs**\n\n"
        "💰 **Kaina:** 15€ už 1 vnt\n"
        "⚡ Ilgas veikimo laikas • Sodrus skonis\n"
        "🔋 650mAh + Type-C įkrovimas\n"
        "🌬 DUAL MESH technologija\n\n"
        "Pasirinkite savo mėgstamą skonį 👇"
    )

    await message.answer_photo(
        photo="https://ibb.co/ycCP5PY8",
        caption=caption,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# ================== SKONIO PERŽIŪRA IR UŽSAKYMAS ==================
@dp.callback_query(F.data.startswith("flavor_"))
async def show_flavor(callback: types.CallbackQuery):
    code = callback.data.split("_")[1]
    name = flavors[code]
    qty = stock[code]
    
    builder = InlineKeyboardBuilder()
    builder.button(text="← Atgal", callback_data="back_to_menu")
    builder.button(text="🛒 Užsakyti šį skonį", callback_data=f"order_{code}")
    builder.adjust(1)

    text = f"🔥 <b>{name}</b>\n\n"
    text += f"💰 Kaina: <b>{PRICE}</b>\n"
    text += f"📦 Likutis: <b>{qty} vnt</b>\n\n"
    text += "Pasirinkite veiksmą:"

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Pasirinkite savo mėgstamą skonį 👇",
        reply_markup=main_menu()
    )
    await callback.answer()

# ================== UŽSAKYMO LOGIKA ==================
@dp.callback_query(F.data.startswith("order_"))
async def start_order(callback: types.CallbackQuery):
    code = callback.data.split("_")[1]
    name = flavors[code]
    
    builder = InlineKeyboardBuilder()
    for i in range(1, 11):
        builder.button(text=f"{i} vnt", callback_data=f"qty_{code}_{i}")
    builder.button(text="← Atgal", callback_data=f"flavor_{code}")
    builder.adjust(3)
    
    await callback.message.edit_text(
        f"🛒 Jūs pasirinkote: <b>{name}</b>\n\nKiek vienetų norite užsisakyti?",
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("qty_"))
async def process_quantity(callback: types.CallbackQuery):
    _, code, qty = callback.data.split("_")
    name = flavors[code]
    qty = int(qty)
    total = qty * 15
    
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Patvirtinti užsakymą", callback_data=f"confirm_{code}_{qty}")
    builder.button(text="← Keisti kiekį", callback_data=f"order_{code}")
    builder.adjust(1)

    await callback.message.edit_text(
        f"📋 **Užsakymo patvirtinimas**\n\n"
        f"Skonis: <b>{name}</b>\n"
        f"Kiekis: <b>{qty} vnt</b>\n"
        f"Viso: <b>{total}€</b>",
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_order(callback: types.CallbackQuery):
    _, code, qty = callback.data.split("_")
    name = flavors[code]
    qty = int(qty)
    
    user = callback.from_user
    username = f"@{user.username}" if user.username else "Nėra"

    order_text = f"🛒 **NAUJAS UŽSAKYMAS!**\n\n"
    order_text += f"Skonis: {name}\n"
    order_text += f"Kiekis: {qty} vnt\n"
    order_text += f"Suma: {qty*15}€\n"
    order_text += f"Vartotojas: {user.full_name}\n"
    order_text += f"Username: {username}\n"
    order_text += f"ID: {user.id}"

    await bot.send_message(ADMIN_ID, order_text)
    
    await callback.message.edit_text(
        "✅ **Užsakymas priimtas!**\n\nAčiū! Netrukus su jumis susisieks administratorius.",
        parse_mode="Markdown"
    )

# ================== ADMIN ==================
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = "🛠 **ADMIN PANELĖ**\n\n"
    for code, name in flavors.items():
        text += f"{name}: **{stock[code]}** vnt\n"
    await message.answer(text, parse_mode="Markdown")

async def main():
    print("✅ Cloudazz.lt Botas veikia!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())