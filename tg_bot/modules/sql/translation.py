import threading
from sqlalchemy import Column, String, UnicodeText
from tg_bot.modules.sql import SESSION, BASE

class Locales(BASE):
    __tablename__ = "Locales"
    chat_id = Column(String(14), primary_key=True)
    locale_name = Column(UnicodeText)

    def __init__(self, chat_id, locale_name):
        self.chat_id = str(chat_id) # ensure string
        self.locale_name = locale_name

Locales.__table__.create(checkfirst=True)
LOCALES_INSERTION_LOCK = threading.RLock()

def switch_to_locale(chat_id, locale_name):
    with LOCALES_INSERTION_LOCK:
        prev = SESSION.query(Locales).get((str(chat_id)))
        if prev:
            SESSION.delete(prev)
        switch_locale = Locales(str(chat_id), locale_name)
        SESSION.add(switch_locale)
        SESSION.commit()

def prev_locale(chat_id):
    try:
        return SESSION.query(Locales).get((str(chat_id)))
    finally :
        SESSION.close()
