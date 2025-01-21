import requests
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, APIKEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_weather():
    base_url = 'http://api.weatherapi.com/v1/current.json'
    complete_url = f'{base_url}?q={'Москва'}&key={APIKEY}&lang=ru'
    response = requests.get(complete_url)
    return response.json()

@dp.message(Command('weather'))
async def weather(message: Message):
    weather = get_weather()
    temp_c = weather['current']['temp_c']  # Берём температуру в градусах Цельсия
    text = f"Температура в Москве сейчас: {temp_c}°C"
    await message.answer(text)

@dp.message(Command('photo'))
async def photo(message: Message):
    await message.answer_photo(photo='https://i.pinimg.com/originals/23/5e/59/235e59a85f3f5a4ee0377d48ec60a555.jpg', caption='Это такая вот фотка.')

@dp.message(F.photo)
async def photka(message: Message):
    await message.answer('Афигеть! Какая фотка!!!')

@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Это искусственный интеллект')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Available commands: /start, /help, /photo, /weather')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Hello! Im a bot.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
