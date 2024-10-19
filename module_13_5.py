from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
kb.row(button, button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью. "
                         "Что бы посчитать суточную норму калорий нажмите - Рассчитать", reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст (полных лет):')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    await message.answer(f'Введите свой пол (М или Ж):')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    if data["gender"] == "М":
        await message.answer(
            f'Ваша суточная норма калорий:'
            f'{int(data["weight"]) * 10 + int(data["growth"]) * 6.25 - int(data["age"]) * 5 + 5}(ккал)'
        )
    elif data["gender"] == "Ж":
        await message.answer(
            f'Ваша суточная норма калорий:'
            f'{int(data["weight"]) * 10 + int(data["growth"]) * 6.25 - int(data["age"]) * 5 - 161}(ккал)'
        )
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)