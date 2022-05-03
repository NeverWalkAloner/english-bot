import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base, Dictionary, User, UserWords
from app.api.deps import get_db
from app.core.config import settings


@pytest.fixture(scope="session")
def db_engine():
    create_database(settings.TEST_SQLALCHEMY_DATABASE_URL)
    engine = create_engine(settings.TEST_SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    drop_database(settings.TEST_SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
    )
    db = TestingSessionLocal()

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def user(db):
    db_user = User(
        id=42,
        username="prefect",
        first_name="Ford",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    yield db_user
    db.delete(db_user)
    db.commit()


@pytest.fixture
def dictionary(db):
    db_dictionary = Dictionary(
        english="hello",
        russian="привет",
    )
    db.add(db_dictionary)
    db.commit()
    db.refresh(db_dictionary)
    yield db_dictionary
    db.delete(db_dictionary)
    db.commit()


@pytest.fixture
def current_word(db, user, dictionary):
    user_word = UserWords(user=user, word=dictionary, in_progress=True)
    db.add(user_word)
    db.commit()
    db.refresh(user_word)
    yield user_word
    db.delete(user_word)
    db.commit()
