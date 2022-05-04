from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from telebot import types

from app.schemas.tg_updated import Update, User
from app.core.config import bot, settings
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
        user = await create_user(update=update, db=db)
    elif update.message.text == "/new_words":
        crud_users.set_usage_mode(db, user, user_models.UsageMode.new_words)
    elif update.message.text == "/repeat_words":
        crud_users.set_usage_mode(db, user, user_models.UsageMode.repeat_words)
    elif update.message.text == "Пропустить слово":
        if user.usage_mode == user_models.UsageMode.new_words:
            crud_users.delete_in_progress_word(db, user)
        else:
            crud_users.update_progress_word(db, user.word_in_progress)
    elif update.message.text == "Показать слово":
        return await current_word(update=update, db=db, user=user)
    elif update.message.text.lower() == settings.EASTER_EGG_TEXT.lower():
        bot.send_message(update.message.chat.id, settings.EASTER_EGG_RESPONSE)
    elif user.word_in_progress:
        return await guess_word(update=update, db=db, user=user)
    return await random_word(update=update, db=db, user=user)


@router.post("/random-word/")
async def random_word(
        update: Update,
        db: Session = Depends(get_db),
        user: user_models.User = Depends(get_current_user)
):
    if user.word_in_progress:
        user_word = user.word_in_progress
    elif user.usage_mode == user_models.UsageMode.new_words:
        word = crud_dictionary.get_random_new_word(db)
        user_word = crud_users.create_word_in_progress(db, user, word)
    else:
        user_word = crud_dictionary.get_random_repeated_word(db, user)
        if user_word:
            crud_users.update_progress_word(db, user_word, in_progress=True)
    if not user_word:
        markup = types.ReplyKeyboardRemove()
        await bot.send_message(
            update.message.chat.id,
            "Нет доступных слов",
            reply_markup=markup,
        )
        return {"status": "NOK"}
    markup = types.ReplyKeyboardMarkup()
    skip = types.KeyboardButton("Пропустить слово")
    show = types.KeyboardButton("Показать слово")
    markup.add(skip, show)
    await bot.send_message(
        update.message.chat.id,
        user_word.word.russian,
        reply_markup=markup,
    )
    return {"status": "OK"}


@router.post("/guess-word/")
async def guess_word(
        update: Update,
        db: Session = Depends(get_db),
        user: user_models.User = Depends(get_current_user)
):
    if not user.word_in_progress:
        return {"status": "NOK"}
    word_in_progress = user.word_in_progress.word.english
    if word_in_progress.lower() == update.message.text.lower():
        crud_users.update_progress_word(db, user.word_in_progress)
        next_word = types.KeyboardButton("следующее слово")
        markup = types.ReplyKeyboardMarkup()
        markup.add(next_word)
        await bot.send_message(
            update.message.chat.id,
            "Правильно!",
            reply_markup=markup,
        )
        return {"status": "OK"}
    else:
        await bot.send_message(
            update.message.chat.id,
            "Неверно, попробуйте еще раз.",
        )
        return {"status": "NOK"}


@router.post("/sign-up/", response_model=User)
async def create_user(update: Update, db: Session = Depends(get_db)):
    user = crud_users.get_user_by_id(db, user_id=update.message.user.id)
    if user:
        return user
    return crud_users.create_user(db=db, user=update.message.user)


@router.post("/current-word/")
async def current_word(
        update: Update,
        db: Session = Depends(get_db),
        user: user_models.User = Depends(get_current_user),
):
    if not user.word_in_progress:
        return {"status": "NOK"}
    next_word = types.KeyboardButton("следующее слово")
    markup = types.ReplyKeyboardMarkup()
    markup.add(next_word)
    await bot.send_message(
        update.message.chat.id,
        user.word_in_progress.word.english,
        reply_markup=markup,
    )
    if user.usage_mode == user_models.UsageMode.new_words:
        crud_users.delete_in_progress_word(db, user)
    else:
        crud_users.update_progress_word(db, user.word_in_progress)
    return {"status": "OK"}
