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

bot = Bot(token=TOKEN)
dp = Dispatcher()

def main_menu():
    builder = InlineKeyboardBuilder()
    for code, name in flavors.items():
        builder.button(text=name, callback_data=code)
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.delete()
    caption = (
        "🔥 **CLOUDAZZ.LT** — Premium Vape Parduotuvė\n\n"
        "🦁 BANG Leader 20000 Puffs\n"
        "💰 Kaina: 15€ / vnt\n\n"
        "Pasirinkite skonį 👇"
    )
    await message.answer_photo(
        photo="https://ibb.co/ycCP5PY8",
        caption=caption,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    code = callback.data
    if code in flavors:
        name = flavors[code]
        new_caption = f"🔥 **{name}**\n\n💰 Kaina: **{PRICE}**\n\nNorite užsakyti? Rašykite administratoriui."
        
        await callback.message.edit_caption(
            caption=new_caption,
            parse_mode="Markdown"
        )
    await callback.answer()

async def main():
    print("✅ Cloudazz Botas veikia!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
