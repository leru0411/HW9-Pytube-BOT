from pytube import YouTube, exceptions
from aiogram import *

import os


bot = Bot('5657870732:AAGmtzw5hI-Uyrp62k6k6GviUCXa68-MTxU')
dp = Dispatcher(bot)

print('server is working')

@dp.message_handler(commands=['start'])
async def start_command(message:types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, f"Привет, {message.from_user.username}! Я помогу тебе скачать видео с YouTube.\n"
                                    "Отправь сюда ссылку на нужное видео.")

@dp.message_handler()
async def text_message(message:types.Message):
    chat_id = message.chat.id
    url = message.text    
    try:
        yt = YouTube(url)
        await bot.send_message(chat_id, f'Скачиваю видео {yt.title} с канала {yt.author}')
        await download_video(url, message, bot)
    except exceptions.VideoUnavailable:
        await bot.send_message(chat_id, f'Ссылка не корректная. Нужна ссылка на существующее видео с YouTube.')
    except exceptions.RegexMatchError:
        await bot.send_message(chat_id, f'Ссылка не корректная. Нужна ссылка на существующее видео с YouTube.')

async def download_video(url, message, bot):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}_{yt.title}')
    with open(f'{message.chat.id}/{message.chat.id}_{yt.title}', 'rb') as video:
        await bot.send_video(message.chat.id, video, caption='Не благодари.')
        os.remove(f'{message.chat.id}/{message.chat.id}_{yt.title}')

if __name__ == '__main__':
    executor.start_polling(dp)