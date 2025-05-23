import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from utils.pdf_generator import generar_pdf

TOKEN = "7263876989:AAH9rz1WwTN0Cpu28Y-0-AYW1jhE8pP6lJE"
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    fullname = State()
    loan_amount = State()
    loan_term = State()
    first_payment_day = State()
    commission = State()
    currency = State()

@dp.message(F.text.lower() == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Нужное Ф.И.О:")
    await state.set_state(Form.fullname)

@dp.message(Form.fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text.strip())
    await message.answer("Сумма кредита:")
    await state.set_state(Form.loan_amount)

@dp.message(Form.loan_amount)
async def get_loan_amount(message: types.Message, state: FSMContext):
    await state.update_data(loan_amount=message.text)
    await message.answer("Срок кредита в месяцах:")
    await state.set_state(Form.loan_term)

@dp.message(Form.loan_term)
async def get_loan_term(message: types.Message, state: FSMContext):
    await state.update_data(loan_term=message.text)
    await message.answer("День первого платежа (1-31):")
    await state.set_state(Form.first_payment_day)

@dp.message(Form.first_payment_day)
async def get_first_payment_day(message: types.Message, state: FSMContext):
    await state.update_data(first_payment_day=message.text)
    await message.answer("Размер комиссии (в процентах):")
    await state.set_state(Form.commission)

@dp.message(Form.commission)
async def get_commission(message: types.Message, state: FSMContext):
    await state.update_data(commission=message.text)
    await message.answer("Валюта(USD, EUR, RUB):")
    await state.set_state(Form.currency)

@dp.message(Form.currency)
async def get_currency(message: types.Message, state: FSMContext):
    await state.update_data(currency=message.text)
    data = await state.get_data()

    filename = f"{data['fullname'].replace(' ', '_')}.pdf"
    filepath = generar_pdf(data, filename)

    pdf = FSInputFile(filepath)
    await message.answer_document(pdf)

    await message.answer("Нужное Ф.И.О:")
    await state.clear()
    await state.set_state(Form.fullname)

if __name__ == "__main__":
    dp.run_polling(bot)