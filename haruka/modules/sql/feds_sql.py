import threading

from sqlalchemy import Column, String, UnicodeText, func, distinct

from haruka.modules.sql import SESSION, BASE


class Federations(BASE):
    __tablename__ = "feds"
    owner_id = Column(String(14))
    fed_name = Column(UnicodeText)
    fed_id = Column(UnicodeText, primary_key=True)

    def __init__(self, owner_id, fed_name, fed_id):
        self.owner_id = owner_id
        self.fed_name = fed_name
        self.fed_id = fed_id

class ChatF(BASE):
    __tablename__ = "chat_feds"
    chat_id = Column(String(14), primary_key=True)
    fed_id = Column(UnicodeText)

    def __init__(self, chat_id, fed_id):
        self.chat_id = chat_id
        self.fed_id = fed_id

class UserF(BASE):
    __tablename__ = "user_feds"
    user_id = Column(String(14), primary_key=True)
    fed_id = Column(UnicodeText)

    def __init__(self, user_id, fed_id):
        self.user_id = user_id
        self.fed_id = fed_id

class RulesF(BASE):
    __tablename__ = "rules_feds"
    fed_id = Column(String(), primary_key=True)
    rules = Column(UnicodeText, default="")

    def __init__(self, fed_id, rules):
        self.fed_id = fed_id
        self.rules = rules

class BansF(BASE):
    __tablename__ = "bans_feds"
    fed_id = Column(String(), primary_key=True)
    user_id = Column(String(14), primary_key=True)
    reason = Column(UnicodeText, default="")

    def __init__(self, fed_id, user_id, reason):
        self.fed_id = fed_id
        self.user_id = user_id
        self.reason = reason


Federations.__table__.create(checkfirst=True)
ChatF.__table__.create(checkfirst=True)
UserF.__table__.create(checkfirst=True)
RulesF.__table__.create(checkfirst=True)
BansF.__table__.create(checkfirst=True)

FEDS_LOCK = threading.RLock()
CHAT_FEDS_LOCK = threading.RLock()


def get_fed_info(fed_id):
    q = SESSION.query(Federations).get(str(fed_id))
    SESSION.close()
    return q


def get_fed_id(chat_id):
        curr = SESSION.query(ChatF).get(str(chat_id))
        if curr:
                h = curr.fed_id
        else:
                h = False
        SESSION.close()
        return h


def new_fed(owner_id, fed_id, fed_name):
    with FEDS_LOCK:
        r = Federations(str(owner_id), fed_id, fed_name)
        SESSION.add(r)
        try:
            SESSION.commit()
            return r
        except:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()

def del_fed(fed_id, chat_id):
    with FEDS_LOCK:
        curr = SESSION.query(Federations).get(fed_id)
        print(curr)
        if curr:
                SESSION.delete(curr)
                SESSION.commit()

        curr = SESSION.query(ChatF).get(str(chat_id))
        if curr:
                SESSION.delete(curr)
                SESSION.commit()

        curr = SESSION.query(UserF).all()
        for I in curr:
                if I.fed_id == fed_id:
                        SESSION.delete(I)
                        SESSION.commit()

        curr = SESSION.query(RulesF).get(fed_id)
        if curr:
                SESSION.delete(curr)
                SESSION.commit()

        return

def search_fed_by_name(fed_name):
        curr = SESSION.query(Federations).all()
        result = False
        for Q in curr:
                if Q.fed_name == fed_name:
                        result = Q.fed_id

        return result

def search_user_in_fed(fed_id, user_id):
        curr = SESSION.query(UserF).all()
        result = False
        for Q in curr:
                print(Q.fed_id, fed_id)
                if Q.fed_id == fed_id:
                        print("2", Q.user_id, user_id)
                        if int(Q.user_id) == int(user_id):
                                print("3")
                                result = Q.user_id

        SESSION.close()
        return result

def chat_join_fed(fed_id, chat_id):
    with FEDS_LOCK:
        r = ChatF(chat_id, fed_id)
        SESSION.add(r)
        try:
            SESSION.commit()
            return r
        except:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()


def user_demote_fed(fed_id, user_id):
    with FEDS_LOCK:
        curr = SESSION.query(UserF).all()
        result = False
        for r in curr:
                print(r.user_id, user_id, r.fed_id, fed_id)
                if int(r.user_id) == int(user_id):
                        print("yes1 - ", r.user_id, user_id)
                        if r.fed_id == fed_id:
                                print("yes2 - ", r.fed_id, fed_id)
                                SESSION.delete(r)
                                SESSION.commit()
                                result = True

        SESSION.close()
        return result


def user_join_fed(fed_id, user_id):
    with FEDS_LOCK:
        r = UserF(user_id, fed_id)
        SESSION.add(r)
        try:
            SESSION.commit()
            return r
        except:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()


def chat_leave_fed(chat_id):
	with FEDS_LOCK:
		H = False
		curr = SESSION.query(ChatF).all()
		for U in curr:
			if int(U.chat_id) == int(chat_id):
				H = True
				SESSION.delete(U)
				SESSION.commit()
		return H

def all_fed_chats(fed_id):
    with FEDS_LOCK:
        r = SESSION.query(ChatF).all()
        h = []

        for n in r:
            if n.fed_id == fed_id:
                print(n.chat_id)
                h.append(n.chat_id)

        SESSION.close()
        return h

def all_fed_users(fed_id):
    with FEDS_LOCK:
        r = SESSION.query(UserF).all()
        h = []

        for n in r:
            if n.fed_id == fed_id:
                print(n.user_id)
                h.append(n.user_id)

        SESSION.close()
        return h


def set_frules(fed_id, rules):
    with FEDS_LOCK:
        r = SESSION.query(RulesF).get(fed_id)
        if r:
                print("fund prev")
                SESSION.delete(r)
        r = RulesF(str(fed_id), rules)

        SESSION.add(r)
        try:
            SESSION.commit()
            return r
        except:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()


def get_frules(fed_id):
    with FEDS_LOCK:
        r = SESSION.query(RulesF).get(str(fed_id))

        SESSION.close()
        return r


def fban_user(fed_id, user_id, reason):
    with FEDS_LOCK:
        r = SESSION.query(BansF).all()
        for I in r:
                print("1")
                if I.fed_id == fed_id:
                        print("2")
                        print(I.user_id, user_id)
                        if int(I.user_id) == int(user_id):
                                print("fund prev")
                                SESSION.delete(I)

        r = BansF(str(fed_id), user_id, reason)

        SESSION.add(r)
        try:
            SESSION.commit()
            return r
        except:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()


def un_fban_user(fed_id, user_id):
    with FEDS_LOCK:
        r = SESSION.query(BansF).all()
        for I in r:
                print("1")
                if I.fed_id == fed_id:
                        print("2")
                        print(I.user_id, user_id)
                        if int(I.user_id) == int(user_id):
                                print("fund prev")
                                SESSION.delete(I)
        try:
            SESSION.commit()
            return I
        except:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()

def get_fban_user(fed_id, user_id):
        r = SESSION.query(BansF).all()
        h = False
        for I in r:
                if I.fed_id == fed_id:
                        if int(I.user_id) == int(user_id):
                                h = I.reason

        SESSION.close()
        return h


def get_all_fban_users(fed_id):
        r = SESSION.query(BansF).all()
        h = []
        for I in r:
                if I.fed_id == fed_id:
                        h.append(I.user_id)

        SESSION.close()
        return h

def get_all_fban_users_global():
        r = SESSION.query(BansF).all()
        h = []
        for I in r:
                h.append(I.user_id)

        SESSION.close()
        return h

def get_all_feds_users_global():
        r = SESSION.query(Federations).all()
        h = []
        for I in r:
                h.append(I.fed_id)

        SESSION.close()
        return h

def search_fed_by_id(fed_id):
        curr = SESSION.query(Federations).all()
        result = False
        for Q in curr:
                if Q.fed_id == fed_id:
                        result = Q.fed_id

        return result
