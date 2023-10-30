from aiogram import Bot
from aiogram.types import PollAnswer


async def is_answer_correct(quiz_answer: PollAnswer, correct_index: list, bot: Bot,
                            last_question=False, ) -> bool:
    if quiz_answer.option_ids == correct_index:
        if not last_question:
            await bot.send_message(quiz_answer.user.id, "Правильно! Идём дальше")
        else:
            await bot.send_message(quiz_answer.user.id, "Правильно!")
            await bot.send_message(quiz_answer.user.id, "Это был последний вопрос. Спасибо за участие!")
        return True
    else:
        if not last_question:
            await bot.send_message(
                quiz_answer.user.id,
                "Жаль, но это неправильный ответ. Двигаемся дальше - может потом повезёт"
            )
        else:
            await bot.send_message(quiz_answer.user.id, "Жаль, но это неправильный ответ.")
            await bot.send_message(quiz_answer.user.id, "Это был последний вопрос. Спасибо за участие!")
        return False
