from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Обычная клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.add(button).add(button_2)

# Инлайн-клавиатура
kb_inl = InlineKeyboardMarkup(row_width=2)
button_inl = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_inl_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_inl.add(button_inl, button_inl_2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Я бот, помогающий твоему здоровью! Нажмите "Рассчитать", чтобы получить рекомендации.\n',
                         reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=kb_inl)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        " Упрощенный вариант формулы Миффлина-Сан Жеора: "
        "\n-для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 "
        "\n-для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161"
    )
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(text='Информация')
async def information(message: types.Message):
    await message.answer('Это тестовый бот для подсчёта калорий')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(grow=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weig=message.text)
    data = await state.get_data()
    BMR = int(10 * int(data['weig']) + 6.25 * int(data['grow']) - 5 * int(data['ag']) + 5)
    await message.answer(f'Норма калорий составляет примерно {BMR} ккал/день.')
    await state.finish()


@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer("Здравствуйте! Введите команду /start, чтобы продолжить.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)