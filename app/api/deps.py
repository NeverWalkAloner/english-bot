from sqlalchemy.orm import Session

from fastapi import Depends

from app.db.session import SessionLocal
from app.schemas.tg_updated import Update
from app.crud.crud_users import get_user_by_id


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(update: Update, db: Session = Depends(get_db)):
    return get_user_by_id(db, update.message.user.id)
