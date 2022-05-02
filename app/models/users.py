import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UsageMode(enum.Enum):
    repeat_words = 'repeat_words'
    new_words = 'new_words'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    usage_mode = Column(
        Enum(UsageMode),
        nullable=False,
        default=UsageMode.new_words.value,
        server_default=UsageMode.new_words.value,
    )

    words = relationship("UserWords", back_populates="user", lazy='dynamic')

    @property
    def word_in_progress(self):
        return self.words.filter(UserWords.in_progress == True).first()


class UserWords(Base):
    __tablename__ = "userwords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("dictionary.id"))
    in_progress = Column(Boolean, default=False)

    user = relationship("User", back_populates="words")
    word = relationship("Dictionary")
