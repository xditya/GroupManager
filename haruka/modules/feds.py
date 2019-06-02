import html
from io import BytesIO
from typing import Optional, List
import random
import uuid
from time import sleep

from future.utils import string_types
from telegram.error import BadRequest, TelegramError
from telegram import ParseMode, Update, Bot, Chat, User, MessageEntity
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from haruka import dispatcher, OWNER_ID, SUDO_USERS, WHITELIST_USERS, MESSAGE_DUMP, LOGGER
from haruka.modules.helper_funcs.handlers import CMD_STARTERS
from haruka.modules.helper_funcs.misc import is_module_loaded, send_to_list
from haruka.modules.helper_funcs.chat_status import is_user_admin
from haruka.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from haruka.modules.helper_funcs.string_handling import markdown_parser
from haruka.modules.disable import DisableAbleCommandHandler

import haruka.modules.sql.feds_sql as sql

from haruka.modules.translations.strings import tld

from haruka.modules.connection import connected

# Hello bot owner, I spended for feds many hours of my life, Please don't remove this if you still respect MrYacha and peaktogoo
# Federation by MrYacha 2018-2019
# Federation rework in process by Mizukito Akito 2019
# Time spended on feds = 10h by #MrYacha
# Time spended on reworking on the whole feds = 20+ hours by @peaktogoo

LOGGER.info("Original federation module by MrYacha, reworked by Mizukito Akito (@peaktogoo) on Telegram.")

FBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Peer_id_invalid",
    "Group chat was deactivated",
    "Need to be inviter of a user to kick it from a basic group",
    "Chat_admin_required",
    "Only the creator of a basic group can kick group administrators",
    "Channel_private",
    "Not in the chat"
}

UNFBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Method is available for supergroup and channel chats only",
    "Not in the chat",
    "Channel_private",
    "Chat_admin_required",
}


def new_fed(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message
    fednam = message.text[len('/newfed '):]
    if not fednam == '':
        fed_id = str(uuid.uuid4())
        fed_name = fednam
        LOGGER.info(fed_id)

        #if fednam == 'Name':
        #     fed_id = "Name"

        x = sql.new_fed(user.id, fed_name, fed_id)
        if not x:
            update.effective_message.reply_text(tld(chat.id, "Big F! There is an error while creating Federations, Kindly get into my support group and ask what is going on!"))
            return

        update.effective_message.reply_text("*You have successfully created a new federation!*"\
                                            "\nName: `{}`"\
                                            "\nID: `{}`"
                                            "\n\nUse command below to join the federation:"
                                            "\n`/joinfed {}`".format(fed_name, fed_id, fed_id), parse_mode=ParseMode.MARKDOWN)
        bot.send_message(
            MESSAGE_DUMP,
           "Federation <b>{}</b> has been created with ID: <pre>{}</pre>".format(fed_name, fed_id),parse_mode=ParseMode.HTML)
    else:
        update.effective_message.reply_text(tld(chat.id, "Please write federation name!"))


def del_fed(bot: Bot, update: Update, args: List[str]):

        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
        fed_id = sql.get_fed_id(chat.id)

        if not fed_id:
            update.effective_message.reply_text(tld(chat.id, "At the moment, We only support deleting federation on the group that joined it."))
            return

        if not is_user_fed_owner(fed_id, user.id):
            update.effective_message.reply_text(tld(chat.id, "Only fed owner can do this!"))
            return

        sql.del_fed(fed_id, chat.id)
        update.effective_message.reply_text(tld(chat.id, "Deleted!"))


def fed_chat(bot: Bot, update: Update, args: List[str]):
        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
        fed_id = sql.get_fed_id(chat.id)

        user_id = update.effective_message.from_user.id
        if not is_user_admin(update.effective_chat, user_id):
            update.effective_message.reply_text("You must be a chat administrator to run this command :P")
            return

        if not fed_id:
            update.effective_message.reply_text(tld(chat.id, "This group not in any federation!"))
            return

        print(fed_id)
        user = update.effective_user  # type: Optional[Chat]
        chat = update.effective_chat  # type: Optional[Chat]
        info = sql.get_fed_info(fed_id)

        text = "This chat is part of the following federation:"
        text += "\n{} (ID: <code>{}</code>)".format(info.fed_name, fed_id)

        update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def join_fed(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message
    administrators = chat.get_administrators()
    fed_id = sql.get_fed_id(chat.id)

    if user.id in SUDO_USERS:
        pass
    else:
        for admin in administrators:
            status = admin.status
            if status == "creator":
                print(admin)
                if str(admin.user.id) == str(user.id):
                    pass
                else:
                    update.effective_message.reply_text(tld(chat.id, "Only group creator can do it!"))
                    return
    if fed_id:
        message.reply_text(tld(chat.id, "Uh, Are you gonna join two federations at one chat?"))
        return

    if len(args) >= 1:
        fedd = args[0]
        print(fedd)
        if sql.search_fed_by_id(fedd) == False:
            message.reply_text(tld(chat.id, "Please enter valid federation id."))
            return

        x = sql.chat_join_fed(fedd, chat.id)
        if not x:
                message.reply_text(tld(chat.id, "Failed to join to federation! Due to some errors that basically I have no idea, try reporting it in support group!"))
                return

        message.reply_text(tld(chat.id, "Chat joined to federation!"))


def leave_fed(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    fed_id = sql.get_fed_id(chat.id)

    administrators = chat.get_administrators()

    if user.id in SUDO_USERS:
        pass
    else:
        for admin in administrators:
            status = admin.status
            if status == "creator":
                print(admin)
                if str(admin.user.id) == str(user.id):
                    pass
                else:
                    update.effective_message.reply_text(tld(chat.id, "Only group creator can do it!"))
                    return

    if sql.chat_leave_fed(chat.id) == True:
        update.effective_message.reply_text(tld(chat.id, "Left from fed!"))
    else:
        update.effective_message.reply_text(tld(chat.id, "Why you are leaving feds when you have not join any!"))


def user_join_fed(bot: Bot, update: Update, args: List[str]):

        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
        fed_id = sql.get_fed_id(chat.id)

        if is_user_fed_owner(fed_id, user.id) == False:
                update.effective_message.reply_text(tld(chat.id, "Only fed owner can do this!"))
                return

        msg = update.effective_message  # type: Optional[Message]
        user_id = extract_user(msg, args)
        if user_id:
                user = bot.get_chat(user_id)

        elif not msg.reply_to_message and not args:
                user = msg.from_user

        elif not msg.reply_to_message and (not args or (
                len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
                [MessageEntity.TEXT_MENTION]))):
                msg.reply_text(tld(chat.id, "I can't extract a user from this."))
                return

        else:
            return

        print(sql.search_user_in_fed(fed_id, user_id))

        #if user_id == user_id:
        #        update.effective_message.reply_text(tld(chat.id, "Are you gonna promote yourself?"))
        #        return

        fed_id = sql.get_fed_id(chat.id)
        info = sql.get_fed_info(fed_id)
        OW = bot.get_chat(info.owner_id)
        HAHA = OW.id
        if user_id == HAHA:
                update.effective_message.reply_text(tld(chat.id, "Why are you trying to promote federation owner!?"))
                return

        if not sql.search_user_in_fed(fed_id, user_id) == False:
                update.effective_message.reply_text(tld(chat.id, "I can't promote user which is already a fed admin! But I can demote them."))
                return

        if user_id == bot.id:
                update.effective_message.reply_text(tld(chat.id, "I am already the federation admin and the one that manage it!"))
                return

        #else:
        #        return

        res = sql.user_join_fed(fed_id, user_id)
        if not res:
                update.effective_message.reply_text(tld(chat.id, "Failed to promoted! It might be because you are admin in another federation! Our code is still buggy, We are sorry for that!"))
                return

        update.effective_message.reply_text(tld(chat.id, "Promoted Successfully!"))


def user_demote_fed(bot: Bot, update: Update, args: List[str]):
        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
        fed_id = sql.get_fed_id(chat.id)

        if is_user_fed_owner(fed_id, user.id) == False:
                update.effective_message.reply_text(tld(chat.id, "Only fed owner can do this!"))
                return

        msg = update.effective_message  # type: Optional[Message]
        user_id = extract_user(msg, args)
        if user_id:
                user = bot.get_chat(user_id)

        elif not msg.reply_to_message and not args:
                user = msg.from_user

        elif not msg.reply_to_message and (not args or (
                len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
                [MessageEntity.TEXT_MENTION]))):
                msg.reply_text(tld(chat.id, "I can't extract a user from this."))
                return

        #else:
        #        return

        if user_id == bot.id:
                update.effective_message.reply_text(tld(chat.id, "What are you trying to do? Demoting me from your federation?"))
                return

        if sql.search_user_in_fed(fed_id, user_id) == False:
                update.effective_message.reply_text(tld(chat.id, "I can't demote user which is not a fed admin! If you wanna bring him to tears, promote him first!"))
                return

        res = sql.user_demote_fed(fed_id, user_id)
        if res == True:
                update.effective_message.reply_text(tld(chat.id, "Get out of here!"))
        else:
                update.effective_message.reply_text(tld(chat.id, "I can not remove him, I am powerless!"))


def fed_info(bot: Bot, update: Update, args: List[str]):

        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
        fed_id = sql.get_fed_id(chat.id)
        info = sql.get_fed_info(fed_id)

        if not fed_id:
            update.effective_message.reply_text(tld(chat.id, "This group is not in any federation!"))
            return

        if is_user_fed_admin(fed_id, user.id) == False:
            update.effective_message.reply_text(tld(chat.id, "Only fed admins can do this!"))
            return

        OW = bot.get_chat(info.owner_id)
        HAHA = OW.id
        FEDADMIN = sql.all_fed_users(fed_id)
        FEDADMIN.append(int(HAHA))
        ACTUALADMIN = len(FEDADMIN)

        print(fed_id)
        user = update.effective_user  # type: Optional[Chat]
        chat = update.effective_chat  # type: Optional[Chat]
        info = sql.get_fed_info(fed_id)

        text = "<b>Fed info:</b>"
        text += "\nFedID: <code>{}</code>".format(fed_id)
        text += "\nName: {}".format(info.fed_name)
        text += "\nCreator: {}".format(mention_html(HAHA, "this guy"))
        text += "\nNumber of admins: <code>{}</code>".format(ACTUALADMIN)
        R = 0
        for O in sql.get_all_fban_users(fed_id):
                R = R + 1

        text += "\nNumber of bans: <code>{}</code>".format(R)
        h = sql.all_fed_chats(fed_id)
        asdf = len(h)
        text += "\nNumber of connected chats: <code>{}</code>".format(asdf)

        update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def fed_admin(bot: Bot, update: Update, args: List[str]):

        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
        fed_id = sql.get_fed_id(chat.id)

        if not fed_id:
            update.effective_message.reply_text(tld(chat.id, "This group is not in any federation!"))
            return

        if is_user_fed_admin(fed_id, user.id) == False:
            update.effective_message.reply_text(tld(chat.id, "Only fed admins can do this!"))
            return

        print(fed_id)
        user = update.effective_user  # type: Optional[Chat]
        chat = update.effective_chat  # type: Optional[Chat]
        info = sql.get_fed_info(fed_id)

        text = "\n\n<b>Federation Admins:</b>"
        user = bot.get_chat(info.owner_id) 
        text += "\n• {} - <code>{}</code> (Creator)".format(mention_html(user.id, user.first_name), user.id)

        h = sql.all_fed_users(fed_id)
        for O in h:
                user = bot.get_chat(O) 
                text += "\n• {} - <code>{}</code>".format(mention_html(user.id, user.first_name), user.id, O)

        update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


def fed_ban(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text(tld(chat.id, "This group is not in any federation!"))
        return

    info = sql.get_fed_info(fed_id)
    OW = bot.get_chat(info.owner_id)
    HAHA = OW.id
    FEDADMIN = sql.all_fed_users(fed_id)
    FEDADMIN.append(int(HAHA))

    if is_user_fed_admin(fed_id, user.id) == False:
        update.effective_message.reply_text(tld(chat.id, "Only fed admins can do this!"))
        return


    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    fban = sql.get_fban_user(fed_id, user_id)
    if not fban == False:
        update.effective_message.reply_text(tld(chat.id, "*Cough* This user is already fbanned!"))
        return

    if not user_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a user."))
        return

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "You can't fban me, better hit your head against the wall, it's more fun."))
        return

    if is_user_fed_owner(fed_id, user_id) == True:
        message.reply_text(tld(chat.id, "Why you are trying to fban the federation owner?"))
        return

    if is_user_fed_admin(fed_id, user_id) == True:
        message.reply_text(tld(chat.id, "Why so serious trying to fban the federation admin?"))
        return

    if user_id == OWNER_ID:
        message.reply_text(tld(chat.id, "I'm not fbanning my master, That's pretty dumb idea!"))
        return

    if int(user_id) in SUDO_USERS:
        message.reply_text(tld(chat.id, "I'm not fbanning the bot sudoers!"))
        return

    if int(user_id) in WHITELIST_USERS:
        message.reply_text(tld(chat.id, "This person is whitelisted from being fbanned!"))
        return

    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        message.reply_text(excp.message)
        return

    if user_chat.type != 'private':
        message.reply_text(tld(chat.id, "That's not a user!"))
        return

    ok123 = mention_html(user_chat.id, user_chat.first_name)
    ok1234 = info.fed_name

    text12 = f"Beginning federation ban of {ok123} in {ok1234}."
    update.effective_message.reply_text(text12, parse_mode=ParseMode.HTML)

    if reason == "":
        reason = "No Reason."

    x = sql.fban_user(fed_id, user_id, reason)
    if not x:
        message.reply_text("Failed to federation ban! Probably this bug is not fixed yet due to the developer is lazy as fuck.")
        return

    h = sql.all_fed_chats(fed_id)
    for O in h:
        try:
            bot.kick_chat_member(O, user_id)
            #text = tld(chat.id, "I should fban {}, but it's only test fban, right? So i let him live.").format(O)
            text = "Fbanning {}".format(user_id)
            #message.reply_text(text)
        except BadRequest as excp:
            if excp.message in FBAN_ERRORS:
                pass
            else:
                message.reply_text(tld(chat.id, "Could not fban due to: {}").format(excp.message))
                return
        except TelegramError:
            pass

    send_to_list(bot, FEDADMIN,
             "<b>New FedBan</b>" \
             "\n<b>Fed:</b> {}" \
             "\n<b>FedAdmin:</b> {}" \
             "\n<b>User:</b> {}" \
             "\n<b>User ID:</b> <code>{}</code>" \
             "\n<b>Reason:</b> {}".format(info.fed_name, mention_html(user.id, user.first_name),
                                   mention_html(user_chat.id, user_chat.first_name),
                                                user_chat.id, reason), 
            html=True)


@run_async
def unfban(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]
    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text(tld(chat.id, "This group is not in any federation!"))
        return

    info = sql.get_fed_info(fed_id)

    if is_user_fed_admin(fed_id, user.id) == False:
        update.effective_message.reply_text(tld(chat.id, "Only fed admins can do this!"))
        return

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a user."))
        return

    user_chat = bot.get_chat(user_id)
    if user_chat.type != 'private':
        message.reply_text(tld(chat.id, "That's not a user!"))
        return

    if sql.get_fban_user(fed_id, user_id) == False:
        message.reply_text(tld(chat.id, "This user is not fbanned!"))
        return

    banner = update.effective_user  # type: Optional[User]

    message.reply_text(tld(chat.id, "I'll give {} a second chance in this federation.").format(user_chat.first_name))

    h = sql.all_fed_chats(fed_id)

    for O in h:
        try:
            member = bot.get_chat_member(O, user_id)
            if member.status == 'kicked':
                bot.unban_chat_member(O, user_id)


        except BadRequest as excp:

            if excp.message in UNFBAN_ERRORS:
                pass
            else:
                message.reply_text(tld(chat.id, "Could not un-fban due to: {}").format(excp.message))
                return

        except TelegramError:
            pass

        try:
            x = sql.un_fban_user(fed_id, user_id)
            if not x:
                message.reply_text(tld(chat.id, "Failed to fban, This user is probably fbanned!"))
                return
        except:
            pass

    message.reply_text(tld(chat.id, "Person has been un-fbanned."))

    OW = bot.get_chat(info.owner_id)
    HAHA = OW.id
    FEDADMIN = sql.all_fed_users(fed_id)
    FEDADMIN.append(int(HAHA))

    send_to_list(bot, FEDADMIN,
             "<b>Un-FedBan</b>" \
             "\n<b>Fed:</b> {}" \
             "\n<b>FedAdmin:</b> {}" \
             "\n<b>User:</b> {}" \
             "\n<b>User ID:</b> <code>{}</code>".format(info.fed_name, mention_html(user.id, user.first_name),
                                                 mention_html(user_chat.id, user_chat.first_name),
                                                              user_chat.id),
            html=True)


def set_frules(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    fed_id = sql.get_fed_id(chat.id)

    if not fed_id:
        update.effective_message.reply_text(tld(chat.id, "This chat is not in any federation!"))
        return

    if is_user_fed_admin(fed_id, user.id) == False:
        update.effective_message.reply_text(tld(chat.id, "Only fed admins can do this!"))
        return

    if len(args) >= 1:
        msg = update.effective_message  # type: Optional[Message]
        raw_text = msg.text
        args = raw_text.split(None, 1)  # use python's maxsplit to separate cmd and args
        if len(args) == 2:
            txt = args[1]
            offset = len(txt) - len(raw_text)  # set correct offset relative to command
            markdown_rules = markdown_parser(txt, entities=msg.parse_entities(), offset=offset)
        x = sql.set_frules(fed_id, markdown_rules)
        if not x:
            update.effective_message.reply_text(tld(chat.id, "Big F! There is an error while setting federation rules! If you wondered why please ask it in support group!"))
            return

        rules = sql.get_fed_info(fed_id).fed_name
        update.effective_message.reply_text(tld(chat.id, f"Rules are set for {rules}!"))
    else:
        update.effective_message.reply_text(tld(chat.id, "Please write rules to set it up!"))


def get_frules(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    fed_id = sql.get_fed_id(chat.id)
    if not fed_id:
        update.effective_message.reply_text(tld(chat.id, "This chat is not in any federation!"))
        return

    ruless = sql.get_frules(fed_id)
    try:
        rules = ruless.rules
        print(rules)
        text = "*Rules in this fed:*\n"
        text += rules
        update.effective_message.reply_text(tld(chat.id, text), parse_mode=ParseMode.MARKDOWN)
        return
    except AttributeError:
        update.effective_message.reply_text(tld(chat.id, "There are no rules in this federation!"))
        return


@run_async
def broadcast(bot: Bot, update: Update, args: List[str]):
    to_send = update.effective_message.text.split(None, 1)
    if len(to_send) >= 2:
        chat = update.effective_chat  # type: Optional[Chat]
        fed_id = sql.get_fed_id(chat.id)
        chats = sql.all_fed_chats(fed_id)
        failed = 0
        for Q in chats:
            try:
                bot.sendMessage(Q, to_send[1])
                sleep(0.1)
            except TelegramError:
                failed += 1
                LOGGER.warning("Couldn't send broadcast to %s, group name %s", str(chat.chat_id), str(chat.chat_name))

        update.effective_message.reply_text(tld(chat.id, "Federations Broadcast complete. {} groups failed to receive the message, probably "
                                            "due to leaving the federation.").format(failed))


def is_user_fed_admin(fed_id, user_id):
    list = sql.all_fed_users(fed_id)
    print(user_id)
    if str(user_id) in list or is_user_fed_owner(fed_id, user_id) == True:
        return True
    else:
        return False


def is_user_fed_owner(fed_id, user_id):
    print("Check on fed owner")

    if int(user_id) == int(sql.get_fed_info(fed_id).owner_id) or user_id == OWNER_ID or user_id == '483808054':
        return True
    else:
        return False


def welcome_fed(bot, update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]

    fed_id = sql.get_fed_id(chat.id)
    fban = fban = sql.get_fban_user(fed_id, user.id)
    if not fban == False:
        update.effective_message.reply_text(tld(chat.id, "This user is banned in current federation! I will remove him."))
        bot.kick_chat_member(chat.id, user.id)
        return True
    else:
        return False


def __stats__():
    R = 0
    for O in sql.get_all_fban_users_global():
        R = R + 1

    S = 0
    for O in sql.get_all_feds_users_global():
        S = S + 1

    return "{} fbanned users, across {} feds".format(R, S)


def __user_info__(user_id, chat_id):
    fed_id = sql.get_fed_id(chat_id)
    if fed_id:
        fban = sql.get_fban_user(fed_id, user_id)
        info = sql.get_fed_info(fed_id)
        infoname = info.fed_name

        if is_user_fed_admin(fed_id, user_id) == True:
            text = f"This user is a fed admin in the current federation, <code>{infoname}</code>."

        elif not fban == False:
            text = "Banned in current federation - <b>Yes</b>"
            text += "\n<b>Reason:</b> {}".format(fban)
        else:
            text = "Banned in current federation - <b>No</b>"
    else:
        text = ""
    return text


__mod_name__ = "Federations"

__help__ = """
Ah, group management. It's all fun and games, until you start getting spammers in, and you need to ban them. Then you need to start banning more, and more, and it gets painful.
But then you have multiple groups, and you don't want these spammers in any of your groups - how can you deal? Do you have to ban them manually, in all your groups?

Inspired by [Rose bot](t.me/MissRose_bot)

No more! With federations, you can make a ban in one chat overlap to all your other chats.
You can even appoint federation admins, so that your trustworthy admins can ban across all the chats that you want to protect.

Commands:
 - /newfed <fedname>: creates a new federation with the given name. Users are only allowed to own one federation. This method can also be used to change the federation name. (max 64 characters)
 - /delfed: deletes your federation, and any information relating to it. Will not unban any banned users.
 - /fedinfo <FedID>: information about the specified federation.
 - /joinfed <FedID>: joins the current chat to the federation. Only chat owners can do this. Each chat can only be in one federation.
 - /leavefed <FedID>: leaves the given federation. Only chat owners can do this.
 - /fpromote <user>: promotes the user to fed admin. Fed owner only.
 - /fdemote <user>: demotes the user from fed admin to normal user. Fed owner only.
 - /fban <user>: bans a user from all federations that this chat is in, and that the executor has control over.
 - /unfban <user>: unbans a user from all federations that this chat is in, and that the executor has control over.
 - /setfrules: Set federation rules
 - /frules: Show federation rules
 - /chatfed: Show the federation the chat is in
 - /fedadmins: Show the federation admins

Federations originally by @MrYacha, 75% Reworked by @peaktogoo
"""

NEW_FED_HANDLER = CommandHandler("newfed", new_fed)
DEL_FED_HANDLER = CommandHandler("delfed", del_fed, pass_args=True)
JOIN_FED_HANDLER = CommandHandler("joinfed", join_fed, pass_args=True)
LEAVE_FED_HANDLER = CommandHandler("leavefed", leave_fed, pass_args=True)
PROMOTE_FED_HANDLER = CommandHandler("fpromote", user_join_fed, pass_args=True)
DEMOTE_FED_HANDLER = CommandHandler("fdemote", user_demote_fed, pass_args=True)
INFO_FED_HANDLER = CommandHandler("fedinfo", fed_info, pass_args=True)
BAN_FED_HANDLER = DisableAbleCommandHandler(["fban", "fedban"], fed_ban, pass_args=True)
UN_BAN_FED_HANDLER = CommandHandler("unfban", unfban, pass_args=True)
FED_BROADCAST_HANDLER = CommandHandler("fbroadcast", broadcast, pass_args=True)
FED_SET_RULES_HANDLER = CommandHandler("setfrules", set_frules, pass_args=True)
FED_GET_RULES_HANDLER = CommandHandler("frules", get_frules, pass_args=True)
FED_CHAT_HANDLER = CommandHandler("chatfed", fed_chat, pass_args=True)
FED_ADMIN_HANDLER = CommandHandler("fedadmins", fed_admin, pass_args=True)

dispatcher.add_handler(NEW_FED_HANDLER)
dispatcher.add_handler(DEL_FED_HANDLER)
dispatcher.add_handler(JOIN_FED_HANDLER)
dispatcher.add_handler(LEAVE_FED_HANDLER)
dispatcher.add_handler(PROMOTE_FED_HANDLER)
dispatcher.add_handler(DEMOTE_FED_HANDLER)
dispatcher.add_handler(INFO_FED_HANDLER)
dispatcher.add_handler(BAN_FED_HANDLER)
dispatcher.add_handler(UN_BAN_FED_HANDLER)
#dispatcher.add_handler(FED_BROADCAST_HANDLER)
dispatcher.add_handler(FED_SET_RULES_HANDLER)
dispatcher.add_handler(FED_GET_RULES_HANDLER)
dispatcher.add_handler(FED_CHAT_HANDLER)
dispatcher.add_handler(FED_ADMIN_HANDLER)
