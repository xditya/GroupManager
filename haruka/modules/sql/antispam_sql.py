import threading

from sqlalchemy import Column, UnicodeText, Integer, String, Boolean

from haruka.modules.sql import BASE, SESSION


class GloballyBannedUsers(BASE):
    __tablename__ = "gbans"
    user_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    reason = Column(UnicodeText)

    def __init__(self, user_id, name, reason=None):
        self.user_id = user_id
        self.name = name
        self.reason = reason

    def __repr__(self):
        return "<GBanned User {} ({})>".format(self.name, self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id,
                "name": self.name,
                "reason": self.reason}


class GloballyMutedUsers(BASE):
    __tablename__ = "gmutes"
    user_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    reason = Column(UnicodeText)

    def __init__(self, user_id, name, reason=None):
        self.user_id = user_id
        self.name = name
        self.reason = reason

    def __repr__(self):
        return "<GMuted User {} ({})>".format(self.name, self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id,
                "name": self.name,
                "reason": self.reason}


class AntispamSettings(BASE):
    __tablename__ = "antispam_settings"
    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=True, nullable=False)

    def __init__(self, chat_id, enabled):
        self.chat_id = str(chat_id)
        self.setting = enabled

    def __repr__(self):
        return "<Gban setting {} ({})>".format(self.chat_id, self.setting)


GloballyBannedUsers.__table__.create(checkfirst=True)
GloballyMutedUsers.__table__.create(checkfirst=True)
AntispamSettings.__table__.create(checkfirst=True)

GBANNED_USERS_LOCK = threading.RLock()
ASPAM_SETTING_LOCK = threading.RLock()
GBANNED_LIST = set()
GBANSTAT_LIST = set()
ANTISPAMSETTING = set()

GMUTED_USERS_LOCK = threading.RLock()
GMUTE_SETTING_LOCK = threading.RLock()
GMUTED_LIST = set()
GMUTESTAT_LIST = set()


def gban_user(user_id, name, reason=None):
    with GBANNED_USERS_LOCK:
        user = SESSION.query(GloballyBannedUsers).get(user_id)
        if not user:
            user = GloballyBannedUsers(user_id, name, reason)
        else:
            user.name = name
            user.reason = reason

        SESSION.merge(user)
        SESSION.commit()
        __load_gbanned_userid_list()


def update_gban_reason(user_id, name, reason=None):
    with GBANNED_USERS_LOCK:
        user = SESSION.query(GloballyBannedUsers).get(user_id)
        if not user:
            return None
        old_reason = user.reason
        user.name = name
        user.reason = reason

        SESSION.merge(user)
        SESSION.commit()
        return old_reason


def ungban_user(user_id):
    with GBANNED_USERS_LOCK:
        user = SESSION.query(GloballyBannedUsers).get(user_id)
        if user:
            SESSION.delete(user)

        SESSION.commit()
        __load_gbanned_userid_list()


def is_user_gbanned(user_id):
    return user_id in GBANNED_LIST


def get_gbanned_user(user_id):
    try:
        return SESSION.query(GloballyBannedUsers).get(user_id)
    finally:
        SESSION.close()


def get_gban_list():
    try:
        return [x.to_dict() for x in SESSION.query(GloballyBannedUsers).all()]
    finally:
        SESSION.close()


def enable_antispam(chat_id):
    with ASPAM_SETTING_LOCK:
        chat = SESSION.query(AntispamSettings).get(str(chat_id))
        if not chat:
            chat = AntispamSettings(chat_id, True)

        chat.setting = True
        SESSION.add(chat)
        SESSION.commit()
        if str(chat_id) in GBANSTAT_LIST:
            GBANSTAT_LIST.remove(str(chat_id))


def disable_antispam(chat_id):
    with ASPAM_SETTING_LOCK:
        chat = SESSION.query(AntispamSettings).get(str(chat_id))
        if not chat:
            chat = AntispamSettings(chat_id, False)

        chat.setting = False
        SESSION.add(chat)
        SESSION.commit()
        GBANSTAT_LIST.add(str(chat_id))


def does_chat_gban(chat_id):
    return str(chat_id) not in GBANSTAT_LIST


def num_gbanned_users():
    return len(GBANNED_LIST)


def __load_gbanned_userid_list():
    global GBANNED_LIST
    try:
        GBANNED_LIST = {x.user_id for x in SESSION.query(GloballyBannedUsers).all()}
    finally:
        SESSION.close()


def __load_gban_stat_list():
    global GBANSTAT_LIST
    try:
        GBANSTAT_LIST = {x.chat_id for x in SESSION.query(AntispamSettings).all() if not x.setting}
    finally:
        SESSION.close()

#Gmute

def gmute_user(user_id, name, reason=None):
    with GMUTED_USERS_LOCK:
        user = SESSION.query(GloballyMutedUsers).get(user_id)
        if not user:
            user = GloballyMutedUsers(user_id, name, reason)
        else:
            user.name = name
            user.reason = reason

        SESSION.merge(user)
        SESSION.commit()
        __load_gmuted_userid_list()


def update_gmute_reason(user_id, name, reason=None):
    with GMUTED_USERS_LOCK:
        user = SESSION.query(GloballyMutedUsers).get(user_id)
        if not user:
            return False
        user.name = name
        user.reason = reason

        SESSION.merge(user)
        SESSION.commit()
        return True


def ungmute_user(user_id):
    with GMUTED_USERS_LOCK:
        user = SESSION.query(GloballyMutedUsers).get(user_id)
        if user:
            SESSION.delete(user)

        SESSION.commit()
        __load_gmuted_userid_list()


def is_user_gmuted(user_id):
    return user_id in GMUTED_LIST


def get_gmuted_user(user_id):
    try:
        return SESSION.query(GloballyMutedUsers).get(user_id)
    finally:
        SESSION.close()


def get_gmute_list():
    try:
        return [x.to_dict() for x in SESSION.query(GloballyMutedUsers).all()]
    finally:
        SESSION.close()


def does_chat_gmute(chat_id):
    return str(chat_id) not in GMUTESTAT_LIST


def num_gmuted_users():
    return len(GMUTED_LIST)


def __load_gmuted_userid_list():
    global GMUTED_LIST
    try:
        GMUTED_LIST = {x.user_id for x in SESSION.query(GloballyMutedUsers).all()}
    finally:
        SESSION.close()


def __load_gmute_stat_list():
    global GMUTESTAT_LIST
    try:
        GMUTESTAT_LIST = {x.chat_id for x in SESSION.query(AntispamSettings).all() if not x.setting}
    finally:
        SESSION.close()



def migrate_chat(old_chat_id, new_chat_id):
    with ASPAM_SETTING_LOCK:
        gban = SESSION.query(AntispamSettings).get(str(old_chat_id))
        if gban:
            gban.chat_id = new_chat_id
            SESSION.add(gban)

        gmute = SESSION.query(AntispamSettings).get(str(old_chat_id))
        if gmute:
            gmute.chat_id = new_chat_id
            SESSION.add(gmute)

        SESSION.commit()


# Create in memory userid to avoid disk access
__load_gbanned_userid_list()
__load_gban_stat_list()

__load_gmuted_userid_list()
__load_gmute_stat_list()
