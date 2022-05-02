from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from telebot import types

from app.schemas.tg_updated import Update, User
from app.schemas.dictionary import Dictionary
from app.core.config import bot
from app.crud import crud_dictionary
from app.crud import crud_users
from app.models import users as user_models

from .deps import get_db, get_current_user

router = APIRouter()


@router.post("/")
async def root(
        update: Update,
        db: Session = Depends(get_db),
        user: user_models.User = Depends(get_current_user)
):
    if update.message.text == "/start":
        return await create_user(update=update, db=db)
    elif update.message.text == "/new_words":
        crud_users.set_usage_mode(db, user, user_models.UsageMode.new_words)
    elif update.message.text == "/repeat_words":
        crud_users.set_usage_mode(db, user, user_models.UsageMode.repeat_words)
    elif update.message.text == "Пропустить слово":
        crud_users.delete_in_progress_word(db, user)
    elif user.word_in_progress:
        word_in_progress = user.word_in_progress.word.english
        if word_in_progress.lower() == update.message.text.lower():
            crud_users.update_in_progress_word(db, user)
            next_word = types.KeyboardButton("следующее слово")
            markup = types.ReplyKeyboardMarkup()
            markup.add(next_word)
            await bot.send_message(
                update.message.chat.id,
                "Правильно!",
                reply_markup=markup,
            )
            return {"status": "OK"}
    user_word = await random_word(db=db, user=user)
    if not user_word:
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            update.message.chat.id,
            "Нет доступных слов",
            reply_markup=markup,
        )
        return {"status": "OK"}
    markup = types.ReplyKeyboardMarkup()
    skip = types.KeyboardButton("Пропустить слово")
    markup.add(skip)
    await bot.send_message(
        update.message.chat.id,
        user_word.word.russian,
        reply_markup=markup,
    )
    return {"status": "OK"}


@router.get("/random_word/", response_model=Dictionary)
async def random_word(
        db: Session = Depends(get_db),
        user: user_models.User = Depends(get_current_user)
):
    if user.word_in_progress:
        return user.word_in_progress
    if user.usage_mode == user_models.UsageMode.new_words:
        word = crud_dictionary.get_random_new_word(db)
    else:
        word = crud_dictionary.get_random_repeated_word(db, user)
    if word:
        return crud_users.create_word_in_progress(db, user, word)


@router.post("/sign-up/", response_model=User)
async def create_user(update: Update, db: Session = Depends(get_db)):
    user = crud_users.get_user_by_id(db, user_id=update.message.user.id)
    if user:
        return user
    return crud_users.create_user(db=db, user=update.message.user)
