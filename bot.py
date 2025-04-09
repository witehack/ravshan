from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import logging
from openai import AsyncOpenAI

# Настройка
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7742435607:AAEE7EaoNzdy6pE6a8rdpuXBB_MFX3p1L0Q"
OPENAI_API_KEY = "sk-lT7U7U3zRLhzNg_PoVw0h11gbD63FjUTCCPttkDYVCAhhOg_-NaayzJsXQ1r_ZM3vyTX4cXQqKg51-BEN6T_SA"
OPENAI_BASE_URL = "https://api.langdock.com/openai/eu/v1"

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

# Режимы работы
MODES = {
    'default': {
        'prompt': "Ты Ravshan — дружелюбный помощник из Узбекистана. Отвечай с юмором, используй слова 'дружок', 'брат'.",
        'temperature': 0.7
    },
    'solver': {
        'prompt': "Ты опытный репетитор. Решай задачи строго по шагам:\n1. Анализ условия\n2. Формулы/теория\n3. Пошаговое решение\n4. Ответ",
        'temperature': 0.1
    }
}


@dp.message(Command("start"))
async def start(message: types.Message):
    text = (
        "👋 Привет! Я Ravshan — твой помощник в учебе!\n\n"
        "🔹 <b>Обычный режим</b>: общение с юмором\n"
        "🔹 <b>Режим решателя</b>: /solve - для точных решений задач\n\n"
        "Примеры запросов:\n"
        "<code>/solve Решите уравнение: 2x + 5 = 15</code>\n"
        "<code>/solve Какой объем водорода выделится при реакции HCl с Zn?</code>"
    )
    await message.answer(text, parse_mode="HTML")


@dp.message(Command("solve"))
async def solve_mode(message: types.Message):
    task = message.text.split('/solve')[-1].strip()
    if not task:
        return await message.answer("Напишите задачу после /solve")

    try:
        await bot.send_chat_action(message.chat.id, "typing")
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": MODES['solver']['prompt']},
                {"role": "user", "content": task}
            ],
            temperature=MODES['solver']['temperature']
        )

        answer = response.choices[0].message.content
        await message.answer(f"🔍 <b>Решение:</b>\n\n{answer}", parse_mode="HTML")

    except Exception as e:
        logger.error(f"Solve error: {e}")
        await message.answer("⚠️ Ошибка при решении задачи")


@dp.message()
async def default_mode(message: types.Message):
    try:
        await bot.send_chat_action(message.chat.id, "typing")
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": MODES['default']['prompt']},
                {"role": "user", "content": message.text}
            ],
            temperature=MODES['default']['temperature']
        )
        await message.answer(response.choices[0].message.content)

    except Exception as e:
        logger.error(f"Chat error: {e}")
        await message.answer("⚠️ Ошибка обработки запроса")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())