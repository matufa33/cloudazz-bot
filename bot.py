from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import json

TOKEN = "8644750183:AAFCk_oXv4v_r1kwIpgxqMztNEfNQwYmBdw"
ADMIN_ID = 7406366737
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
        default = {"watermelon": 9, "strawberry": 10, "blueberry": 10, "grape": 10, "mix": 10}
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

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.delete()
    caption = "🔥 **CLOUDAZZ.LT** — Premium Vape Parduotuvė\n\n🦁 BANG Leader 20000 Puffs\n\n💰 Kaina: 15€ / vnt\n\nPasirinkite skonį 👇"
    await message.answer_photo(
        photo="https://ibb.co/ycCP5PY8",
        caption=caption,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data.startswith("flavor_"))
async def show_flavor(callback: types.CallbackQuery):
    code = callback.data.split("_")[1]
    name = flavors[code]
    qty = stock.get(code, 0)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="← Atgal", callback_data="back")
    builder.button(text="🛒 Užsakyti", callback_data=f"order_{code}")
    builder.adjust(1)

    await callback.message.edit_text(
        f"🔥 <b>{name}</b>\n\n💰 Kaina: <b>{PRICE}</b>\n📦 Likutis: <b>{qty} vnt</b>",
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text("Pasirinkite skonį 👇", reply_markup=main_menu())
    await callback.answer()

async def main():
    print("✅ Botas veikia!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
