from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import random

TOKEN = "ВАШ_ТОКЕН_БОТА"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команды
commands = [
    ("start", "Начать работу"),
    ("help", "Помощь"),
    ("advice", "Совет по безопасности"),
    ("joke", "Шутка про IT")
]

# Данные для бота
advices = [
    "🔐 Всегда обновляйте ПО",
    "🛡️ Используйте менеджер паролей",
    "🌐 VPN защищает в публичных сетях"
]

jokes = [
    "Почему программист всегда холодный? Потому что у него Windows открыты!",
    "Как называют программиста на пляже? Безтолочь!",
]

# Обработчики
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text=cmd[0]) for cmd in commands]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Выберите команду:", reply_markup=keyboard)

@dp.message(Command("advice"))
async def give_advice(message: types.Message):
    await message.answer(random.choice(advices))

@dp.message(Command("joke"))
async def tell_joke(message: types.Message):
    await message.answer(random.choice(jokes))

@dp.message(F.text == "help")
async def help_cmd(message: types.Message):
    await message.answer("Доступные команды:\n" + "\n".join(f"/{cmd[0]} - {cmd[1]}" for cmd in commands))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())