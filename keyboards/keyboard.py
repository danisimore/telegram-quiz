from aiogram import types

kb = [
    [
        types.KeyboardButton(text="Сыграем!"),
    ],
]

keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Нажми на кнопку снизу!",
    one_time_keyboard=True
)
