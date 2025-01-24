import requests, asyncio, os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from aiogoogletrans import Translator
from config import TOKEN, APIKEY

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

def get_weather():
    base_url = 'http://api.weatherapi.com/v1/current.json'
    complete_url = f'{base_url}?q={'Москва'}&key={APIKEY}&lang=ru'
    response = requests.get(complete_url)
    return response.json()

@dp.message(Command('weather'))
async def weather(message: Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    weather = get_weather()
    temp_c = round(weather['current']['temp_c'])  # Берём температуру в градусах Цельсия и округляем
    text = f"Температура в Москве сейчас: {temp_c}°C" # Вся фраза текстом
    tts = gTTS(text=text, lang='ru') # Преобразуем в голосовое сообщение
    tts.save('weather.ogg') # Сохраняем голосовое сообщение
    audio = FSInputFile('weather.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove('weather.ogg') # Удаляем голосовое сообщение

@dp.message(F.photo)
async def photka(message: Message):
    await message.answer('Ухты, какая фотка! Сохраню себе.')
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Я бот, который сохраняет все фотки, которые ты мне отправишь. Ещё я могу сообщить тебе голосом текущую температуру в Москве (по команде /weather). И переведу на английский любой текст - просто напиши мне.')

@dp.message()
async def other(message: Message):
    translation_obj = await translator.translate(message.text, dest='en')
    translation = translation_obj.text
    await message.answer(f'{message.from_user.first_name}, по английски это будет:\n{translation}.')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
