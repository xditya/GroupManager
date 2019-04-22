import threading

from sqlalchemy import Column, UnicodeText, Integer, String, Boolean

from tg_bot.modules.sql import BASE, SESSION
from tg_bot import SUPPORT_USERS

class SupportUsers(BASE):
    __tablename__ = "supportusers"
    user_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    reason = Column(UnicodeText)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return "<Support User {} ({})>".format(self.name, self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id,
                "name": self.name}

SupportUsers.__table__.create(checkfirst=True)

SUPPORT_USERS_LOCK = threading.RLock()
SUPPORT_SETTING_LOCK = threading.RLock()
SUPPORT_LIST = set()
SUPPORTSTAT_LIST = set()

def gsupport_user(user_id, name):
    with SUPPORT_USERS_LOCK:
        user = SESSION.query(SupportUsers).get(user_id)
        if not user:
            user = SupportUsers(user_id, name)
        else:
            user.name = name

        SESSION.merge(user)
        SESSION.commit()
        __load_support_userid_list()

def ungsupport_user(user_id):
    with SUPPORT_USERS_LOCK:
        user = SESSION.query(SupportUsers).get(user_id)
        if user:
            SESSION.delete(user)

        SESSION.commit()
        __load_support_userid_list()

def get_support_list():
    try:
        return [x.to_dict() for x in SESSION.query(SupportUsers).all()]
    finally:
        SESSION.close()

def __load_support_userid_list():
    global SUPPORT_LIST
    try:
        SUPPORT_LIST = {x.user_id for x in SESSION.query(SupportUsers).all()}
    finally:
        SESSION.close()
