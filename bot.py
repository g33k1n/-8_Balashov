import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import sqlite3


API_TOKEN = "7708065662:AAHBfsK0rD9AlgN6pjNYEQSv8DhFmap2wT0"

# Создание экземпляров бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Соединение с БД
conn = sqlite3.connect('messages.db')
c = conn.cursor()

# Создание таблицы сообщений
c.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user TEXT,
                message TEXT,
                command TEXT,
                timestamp TEXT
            )''')
conn.commit()

# Функция для сохранения сообщения в БД
def save_message(user, message, command, timestamp):
    c.execute('INSERT INTO messages (user, message, command, timestamp) VALUES (?, ?, ?, ?)',
              (user, message, command, timestamp))
    conn.commit()

# Создаем клавиатуру с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/music"), KeyboardButton(text="/messengers")]
    ],
    resize_keyboard=True
)

# Обработка команды /start
@router.message(Command("start"))
async def start_handler(message: Message):
    save_message(message.from_user.username, message.text, "start", message.date)
    await message.answer("Привет! Я бот, готов помочь!", reply_markup=keyboard)

# Обработка команды /help
@router.message(Command("help"))
async def help_handler(message: Message):
    save_message(message.from_user.username, message.text, "help", message.date)
    await message.answer("Напиши команду /start, чтобы начать работу.", reply_markup=keyboard)

# Обработка команды /music
@router.message(Command("music"))
async def music_handler(message: Message):
    save_message(message.from_user.username, message.text, "music", message.date)
    await message.answer("Вот ссылка на Яндекс.Музыку: https://music.yandex.ru/", reply_markup=keyboard)

# Обработка команды /messengers
@router.message(Command("messengers"))
async def messengers_handler(message: Message):
    save_message(message.from_user.username, message.text, "messengers", message.date)
    await message.answer("Вот ссылки на мессенджеры:\nTelegram: https://telegram.org/\nWhatsApp: https://www.whatsapp.com/\nSignal: https://signal.org/", reply_markup=keyboard)

# Обработка всех остальных сообщений
@router.message()
async def all_messages_handler(message: Message):
    save_message(message.from_user.username, message.text, "other", message.date)
    await message.answer("Ваше сообщение сохранено в базе данных!", reply_markup=keyboard)

# Регистрация маршрутов
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
