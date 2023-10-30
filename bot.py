import asyncio
import os
import json

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
from services.write_data import write_json


load_dotenv(dotenv_path=".env")

TOKEN = os.environ.get("TOKEN")

storage = MemoryStorage()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()

with open("./data/users_statistic.json") as data_file:
    user_data = json.load(data_file)

current_user_quiz_statistic = {}

quiz_counter = 0


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer("Привет!", reply_markup=keyboard)


@dp.message(MessageTextFilter("Сыграем!"))
async def lets_play(message: types.Message) -> None:
    global user_data
    global current_user_quiz_statistic

    if message.chat.username in user_data:
        await message.answer("Вы уже проходили опрос!")
    else:
        current_user_quiz_statistic[message.chat.username] = {
            "correct_answers": 0,
            "incorrect_answers": 0
        }

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
    global user_data

    if quiz_counter == 0:
        is_correct = await is_answer_correct(quiz_answer=quiz_answer, correct_index=[1], bot=bot)

        if is_correct:
            current_user_quiz_statistic[quiz_answer.user.username]["correct_answers"] += 1
        else:
            current_user_quiz_statistic[quiz_answer.user.username]["incorrect_answers"] += 1

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
        is_correct = await is_answer_correct(quiz_answer=quiz_answer, correct_index=[2], bot=bot)

        if is_correct:
            current_user_quiz_statistic[quiz_answer.user.username]["correct_answers"] += 1
        else:
            current_user_quiz_statistic[quiz_answer.user.username]["incorrect_answers"] += 1

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
        is_correct = await is_answer_correct(quiz_answer=quiz_answer, correct_index=[0], bot=bot)

        if is_correct:
            current_user_quiz_statistic[quiz_answer.user.username]["correct_answers"] += 1
        else:
            current_user_quiz_statistic[quiz_answer.user.username]["incorrect_answers"] += 1

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
        is_correct = await is_answer_correct(quiz_answer=quiz_answer, correct_index=[3], bot=bot)

        if is_correct:
            current_user_quiz_statistic[quiz_answer.user.username]["correct_answers"] += 1
        else:
            current_user_quiz_statistic[quiz_answer.user.username]["incorrect_answers"] += 1

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
        is_correct = await is_answer_correct(
            quiz_answer=quiz_answer,
            correct_index=[3],
            bot=bot,
            last_question=True,
        )

        if is_correct:
            current_user_quiz_statistic[quiz_answer.user.username]["correct_answers"] += 1
        else:
            current_user_quiz_statistic[quiz_answer.user.username]["incorrect_answers"] += 1

        quiz_counter = 0

        write_json(user_data=current_user_quiz_statistic, username=quiz_answer.user.username)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
