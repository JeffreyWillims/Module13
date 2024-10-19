import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
api = ""
bot = Bot(token=api)
dp = Dispatcher(storage=MemoryStorage())

# Обычная клавиатура
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')]
    ],
    resize_keyboard=True
)

# Инлайн-клавиатура с использованием InlineKeyboardBuilder
builder = InlineKeyboardBuilder()
button_inl = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_inl_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
builder.add(button_inl, button_inl_2)
kb_inl = builder.as_markup()

# FSM Состояния
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer(
        'Я бот, помогающий твоему здоровью! Нажмите "Рассчитать", чтобы получить рекомендации.',
        reply_markup=kb
    )

# Обработчик кнопки "Рассчитать"
@dp.message(F.text == "Рассчитать")
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=kb_inl)

# Обработчик инлайн-кнопки "Формулы расчёта"
@dp.callback_query(F.data == "formulas")
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        " Упрощенный вариант формулы Миффлина-Сан Жеора: "
        "\n-для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 "
        "\n-для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161"
    )
    await call.answer()

# Обработчик инлайн-кнопки "Рассчитать норму калорий"
@dp.callback_query(F.data == "calories")
async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой возраст: ')
    await state.set_state(UserState.age)
    await call.answer()

# Обработчик ввода возраста
@dp.message(UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await state.set_state(UserState.growth)

# Обработчик ввода роста
@dp.message(UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await state.set_state(UserState.weight)



# Обработчик ввода веса и подсчёт калорий
@dp.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    weight = int(message.text)
    growth = int(user_data['growth'])
    age = int(user_data['age'])
    BMR = int(10 * weight + 6.25 * growth - 5 * age + 5)
    await message.answer(f'Норма калорий составляет примерно {BMR} ккал/день.')
    await state.clear()

# Обработчик кнопки "Информация"
@dp.message(F.text == "Информация")
async def information(message: types.Message):
    await message.answer('Это тестовый бот для подсчёта калорий')

# Универсальный обработчик для всех остальных сообщений
@dp.message()
async def all_message(message: types.Message):
    await message.answer("Здравствуйте! Введите команду /start, чтобы продолжить.")

if __name__ == '__main__':
    dp.run_polling(bot)
