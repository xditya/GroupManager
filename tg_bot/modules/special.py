from io import BytesIO
from time import sleep
from typing import Optional, List
from telegram import TelegramError, Chat, Message
from telegram import Update, Bot, User
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown
from tg_bot.modules.helper_funcs.chat_status import is_user_ban_protected, user_admin, bot_admin
from tg_bot.modules.helper_funcs.extraction import extract_user_and_text


import random, re
import telegram
import tg_bot.modules.sql.users_sql as sql
from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, LOGGER
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.disable import DisableAbleCommandHandler

USERS_GROUP = 4

MESSAGES = (
    "Happy birthday ",
    "Heppi burfdey ",
    "Hep burf ",
    "Happy day of birthing ",
    "Sadn't deathn't-day ",
    "Oof, you were born today ",
)


@run_async
def spam(bot: Bot, update: Update):
    message = update.effective_message
    args = message.text.split(None, 1)[1]
    intval = str()
    args[0]+args[1]
    for x in args:
        if x.isdigit():
            intval = intval + x
        elif not x.isdigit():
            break
    spammsg = args.lstrip(intval)[1:]
    if intval.isdigit():
        if int(intval) <= 10:
            i = 0
            while i < int(intval):
                message.reply_text(spammsg)
                i += 1
        else:
            message.reply_text("Spam yourself")
    else:
        message.reply_text("Spam yourself")

@run_async
def snipe(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError as excp:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text("Couldn't send the message. Perhaps I'm not part of that group?")


@run_async
def getlink(bot: Bot, update: Update, args: List[int]):
    message = update.effective_message
    if args:
        pattern = re.compile(r'-\d+')
    else:
        message.reply_text("You don't seem to be referring to any chats.")
    links = "Invite link(s):\n"
    for chat_id in pattern.findall(message.text):
        try:
            chat = bot.getChat(chat_id)
            bot_member = chat.get_member(bot.id)
            if bot_member.can_invite_users:
                invitelink = bot.exportChatInviteLink(chat_id)
                links += str(chat_id) + ":\n" + invitelink + "\n"
            else:
                links += str(chat_id) + ":\nI don't have access to the invite link." + "\n"
        except BadRequest as excp:
                links += str(chat_id) + ":\n" + excp.message + "\n"
        except TelegramError as excp:
                links += str(chat_id) + ":\n" + excp.message + "\n"

    message.reply_text(links)


@run_async
def slist(bot: Bot, update: Update):
    message = update.effective_message
    text1 = "My sudo users are:"
    text2 = "My support users are:"
    for user_id in SUDO_USERS:
        try:
            user = bot.get_chat(user_id)
            name = "[{}](tg://user?id={})".format(user.first_name + (user.last_name or ""), user.id)
            if user.username:
                name = escape_markdown("@" + user.username)
            text1 += "\n - {}".format(name)
        except BadRequest as excp:
            if excp.message == 'Chat not found':
                text1 += "\n - ({}) - not found".format(user_id)
    for user_id in SUPPORT_USERS:
        try:
            user = bot.get_chat(user_id)
            name = "[{}](tg://user?id={})".format(user.first_name + (user.last_name or ""), user.id)
            if user.username:
                name = escape_markdown("@" + user.username)
            text2 += "\n - {}".format(name)
        except BadRequest as excp:
            if excp.message == 'Chat not found':
                text2 += "\n - ({}) - not found".format(user_id)
    message.reply_text(text1 + "\n", parse_mode=ParseMode.MARKDOWN)
    message.reply_text(text2 + "\n", parse_mode=ParseMode.MARKDOWN)


@run_async
@user_admin
def birthday(bot: Bot, update: Update, args: List[str]):
    if args:
        username = str(",".join(args))
    for i in range(5):
        bdaymessage = random.choice(MESSAGES)
        update.effective_message.reply_text(bdaymessage + username)


@run_async
def banall(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = str(args[0])
        all_mems = sql.get_chat_members(chat_id)
    else:
        chat_id = str(update.effective_chat.id)
        all_mems = sql.get_chat_members(chat_id)
    for mems in all_mems:
        try:
            bot.kick_chat_member(chat_id, mems.user)
            update.effective_message.reply_text("Tried banning " + str(mems.user))
            sleep(0.1)
        except BadRequest as excp:
            update.effective_message.reply_text(excp.message + " " + str(mems.user))
            continue

@bot_admin
def leavechat(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = int(args[0])
    else:
        update.effective_message.reply_text("You do not seem to be referring to a chat!")
    try:
        chat = bot.getChat(chat_id)
        titlechat = bot.get_chat(chat_id).title
        bot.sendMessage(chat_id, "`I Go Away!`")
        bot.leaveChat(chat_id)
        update.effective_message.reply_text("I left group {}".format(titlechat))

    except BadRequest as excp:
        if excp.message == "Chat not found":
            update.effective_message.reply_text("It looks like I've been kicked out of the group :p")
        else:
            return

__help__ = """
**Owner only:**
- /getlink **chatid**: Get the invite link for a specific chat.
- /banall : haha yes
- /leavechat : O GOD YES
**Sudo/owner only:**
- /quickscope **chatid** **userid**: Ban user from chat.
- /quickunban **chatid** **userid**: Unban user from chat.
- /snipe **chatid** **string**: Make me send a message to a specific chat.
- /rban **chatid** **userid** remotely ban a user from a chat
- /runban **chatid** **userid** remotely unban a user from a chat
- /Stats: check bot's stats
- /chatlist: get chatlist
- /gbanlist: get gbanned users list
- /gmutelist: get gmuted users list
- Chat bans via /restrict chat_id and /unrestrict chat_id commands
**Support user:**
- /gban : Global ban a user
- /ungban : Ungban a user
- /gmute : Gmute a user
- /ungmute : Ungmute a user
- /spam : Cus y not
Sudo/owner can use these commands too.
"""
__mod_name__ = "Special"

SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args=True, filters=Filters.user(OWNER_ID))
GETLINK_HANDLER = CommandHandler("getlink", getlink, pass_args=True, filters=Filters.user(OWNER_ID))
SLIST_HANDLER = CommandHandler("slist", slist, filters=Filters.user(OWNER_ID))
BIRTHDAY_HANDLER = CommandHandler("birthday", birthday, pass_args=True, filters=Filters.group)
SPAM_HANDLER = DisableAbleCommandHandler("spam", spam, filters=CustomFilters.sudo_filter)
LEAVECHAT_HANDLER = CommandHandler("leavechat", leavechat, pass_args=True, filters=Filters.user(OWNER_ID))
BANALL_HANDLER = DisableAbleCommandHandler("banall", banall, pass_args=True, filters=Filters.user(OWNER_ID))

dispatcher.add_handler(SPAM_HANDLER)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(GETLINK_HANDLER)
dispatcher.add_handler(SLIST_HANDLER)
dispatcher.add_handler(BIRTHDAY_HANDLER)
dispatcher.add_handler(LEAVECHAT_HANDLER)
dispatcher.add_handler(BANALL_HANDLER)
