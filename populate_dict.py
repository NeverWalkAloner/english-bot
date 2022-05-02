import json

from app.db.session import SessionLocal

from app.models.dictionary import Dictionary

with open('dict_db', mode='r') as f:
    db = SessionLocal()
    words = json.loads(f.read())
    for word in words:
        db_dic = Dictionary(english=word['eng'], russian=word['rus'])
        db.add(db_dic)
    db.commit()
