from sqlalchemy.orm import Session

from app.models.dictionary import Dictionary
from app.models.users import User, UsageMode, UserWords
from app.schemas import tg_updated as user_schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one_or_none()


def create_user(db: Session, user: user_schemas.User):
    db_user = User(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_usage_mode(db: Session, user: User, usage_mode: UsageMode):
    user.usage_mode = usage_mode
    db.add(user)
    db.commit()


def create_word_in_progress(db: Session, user: User, word: Dictionary):
    db_word = UserWords(
        user=user,
        word=word,
        in_progress=True,
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def delete_in_progress_word(db: Session, user: User):
    db.delete(user.word_in_progress)
    db.commit()


def update_in_progress_word(db: Session, user: User):
    user.word_in_progress.in_progress = False
    db.add(user.word_in_progress)
    db.commit()
