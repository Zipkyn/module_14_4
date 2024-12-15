from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from crud_functions import initiate_db, get_all_products

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

initiate_db()

main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ]
)

buying_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ]
)

@dp.message(F.text.lower() == 'привет')
async def greet(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=main_keyboard)

@dp.message(F.text == 'Купить')
async def get_buying_list(message: types.Message):
    products = get_all_products()
    if not products:
        await message.answer("Нет доступных продуктов для покупки.")
        return

    for product in products:
        product_id, title, description, price = product
        product_info = f"Название: {title} | Описание: {description} | Цена: {price}"
        photo_path = f'images/product{product_id}.jpg'  # Путь к фото продукта
        try:
            photo = FSInputFile(photo_path)
            await message.answer_photo(photo=photo, caption=product_info)
        except Exception as e:
            await message.answer(f"{product_info}\n[Изображение не найдено]")

    await message.answer("Выберите продукт для покупки:", reply_markup=buying_inline_keyboard)

@dp.callback_query(F.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


