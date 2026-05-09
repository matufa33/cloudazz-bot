from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

TOKEN = "ČIA_ĮKLIJUOK_SAVO_TOKENĄ"   # ← Pakeisk!
ADMIN_ID = 123456789                  # ← Pakeisk

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
    caption = "🔥 **CLOUDAZZ.LT** — BANG Leader 20000 Puffs\n\n💰 15€ / vnt\n\nPasirinkite skonį 👇"
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
        await callback.message.edit_text(
            f"🔥 <b>{name}</b>\n\n💰 Kaina: <b>15€</b>\n\nNorite užsakyti? Rašykite @cloudazz_admin",
            parse_mode="HTML"
        )
    await callback.answer()

async def main():
    print("✅ Botas paleistas!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
