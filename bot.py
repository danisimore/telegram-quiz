import asyncio
import os

from aiogram.enums import ParseMode
from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.types import PollAnswer

from dotenv import load_dotenv

from keyboards.keyboard import keyboard
from filters.message_text_filter import MessageTextFilter

from services.check_answer import is_answer_correct

load_dotenv(dotenv_path=".env")

TOKEN = os.environ.get("TOKEN")

storage = MemoryStorage()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()

quiz_counter = 0


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer("Привет!", reply_markup=keyboard)


@dp.message(MessageTextFilter("Сыграем!"))
async def lets_play(message: types.Message) -> None:
    await bot.send_poll(
        message.chat.id,
        'Первый вопрос: Как назывался особый головной убор, который носили фараоны в Древнем Египте?',
        ['Картуз', 'Немес', 'Корона', 'Убрус'],
        type='quiz',
        correct_option_id=1,
        is_anonymous=False,
    )


@dp.poll_answer()
async def handle_poll_answer(quiz_answer: PollAnswer):
    global quiz_counter

    if quiz_counter == 0:
        await is_answer_correct(quiz_answer=quiz_answer, correct_index=[1], bot=bot)

        quiz_counter += 1

        await bot.send_poll(
            quiz_answer.user.id,
            'У какого животного самые большие глаза относительно тела?',
            ['У лемура', 'У летучей мыши', 'У долгопята', 'У тупайи'],
            type='quiz',
            correct_option_id=2,
            is_anonymous=False
        )

    elif quiz_counter == 1:
        await is_answer_correct(quiz_answer=quiz_answer, correct_index=[2], bot=bot)

        quiz_counter += 1

        await bot.send_poll(
            quiz_answer.user.id,
            'Детинцем на Руси называли...',
            ['Кремль', 'Школу', 'Княжеский терем', 'Монастырь'],
            type='quiz',
            correct_option_id=0,
            is_anonymous=False
        )

    elif quiz_counter == 2:
        await is_answer_correct(quiz_answer=quiz_answer, correct_index=[0], bot=bot)

        quiz_counter += 1

        await bot.send_poll(
            quiz_answer.user.id,
            'Продолжите пословицу: «Знает кошка…»',
            ['«Да мыши не знают»', '«Почем фунт лиха»', '«Где собака зарыта»', '«Чье мясо съела»'],
            type='quiz',
            correct_option_id=3,
            is_anonymous=False
        )

    elif quiz_counter == 3:
        await is_answer_correct(quiz_answer=quiz_answer, correct_index=[2], bot=bot)

        quiz_counter += 1

        await bot.send_poll(
            quiz_answer.user.id,
            'Сколько лет проходит между ситцевой и золотой свадьбой?',
            ['11', '19', '25', '49'],
            type='quiz',
            correct_option_id=3,
            is_anonymous=False
        )

    elif quiz_counter == 4:
        await is_answer_correct(quiz_answer=quiz_answer, correct_index=[3], bot=bot, last_question=True)
        quiz_counter = 0


async def main():
    await dp.start_polling(bot)


# router.message.register(cmd_start, Command("start"))

if __name__ == "__main__":
    asyncio.run(main())
