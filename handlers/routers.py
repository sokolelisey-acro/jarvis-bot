import os
import google.generativeai as genai # Убедись, что импортировал genai
from PIL import Image
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from handlers.gemai import model

router = Router()
user_chats = {}


def get_user_prefix(message: Message):
    user_username = message.from_user.username
    
    
    if user_username == "Puma_aa": 
        return "[УРОВЕНЬ ДОСТУПА: МИСС ИННА]\n"
    
    
    elif user_username == "elisey124": 
        return "[УРОВЕНЬ ДОСТУПА: СОЗДАТЕЛЬ]\n"
    
    
    else:
        return "[УРОВЕНЬ ДОСТУПА: ГОСТЬ]\n"

@router.message(Command("start"))
async def start(message: Message):
    print(f"ID: {message.from_user.id} | User: {message.from_user.username}") 
    await message.answer("Джарвис на связи. Чем могу помочь?")

@router.message(F.text)
async def text_ai_dialog(message: Message):
    user_id = message.from_user.id
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])
    
    chat = user_chats[user_id]
    wait_msg = await message.answer("🧠 Думаю...")

    try:
        prefix = get_user_prefix(message)
    
        response = await chat.send_message_async(f"{prefix}{message.text}")
        await wait_msg.edit_text(response.text)
    except Exception as e:
        await wait_msg.edit_text("Сенсоры барахлят... Попробуйте еще раз.")
        print(f"Ошибка текст: {e}")

@router.message(F.photo)
async def photo_ai_dialog(message: Message):
    user_id = message.from_user.id
    user_caption = message.caption if message.caption else "Что на фото?"
    
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])
    
    chat = user_chats[user_id]
    wait_msg = await message.answer("👁 Анализирую изображение...")

    try:
        photo_id = message.photo[-1].file_id
        file_path = f"temp_{user_id}.jpg" 
        await message.bot.download(photo_id, destination=file_path)

        img = Image.open(file_path)
        prefix = get_user_prefix(message)
        
        response = await chat.send_message_async([f"{prefix}{user_caption}", img])
        await wait_msg.edit_text(response.text)

        img.close()
        os.remove(file_path)
    except Exception as e:
        await wait_msg.edit_text("Не могу распознать изображение.")
        print(f"Ошибка фото: {e}")


@router.message(F.voice)
async def voice_ai_dialog(message: Message):
    user_id = message.from_user.id
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])
    
    chat = user_chats[user_id]
    wait_msg = await message.answer("👂 Слушаю...")

    try:
        voice_id = message.voice.file_id
        file_path = f"temp_{user_id}.ogg" 
        await message.bot.download(voice_id, destination=file_path)

       
        uploaded_file = genai.upload_file(path=file_path)
        
        prefix = get_user_prefix(message)
        response = await chat.send_message_async([prefix, uploaded_file])
        
        await wait_msg.edit_text(response.text)
        
        
        os.remove(file_path)
    
    except Exception as e:
        await wait_msg.edit_text("Аудио-датчики неисправны.")
        print(f"Ошибка голос: {e}")