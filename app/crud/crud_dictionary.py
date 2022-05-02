from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from app.models.dictionary import Dictionary
from app.models.users import User


def get_random_new_word(db: Session):
    return db.query(Dictionary).order_by(func.random()).first()


def get_random_repeated_word(db: Session, user: User):
    return user.words.order_by(func.random()).first()
