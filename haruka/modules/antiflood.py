import html
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler, CommandHandler, run_async
from telegram.utils.helpers import mention_html

from haruka import dispatcher
from haruka.modules.helper_funcs.chat_status import is_user_admin, user_admin, can_restrict
from haruka.modules.log_channel import loggable
from haruka.modules.sql import antiflood_sql as sql

from haruka.modules.translations.strings import tld

FLOOD_GROUP = 3


@run_async
@loggable
def check_flood(bot: Bot, update: Update) -> str:
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    if not user:  # ignore channels
        return ""

    # ignore admins
    if is_user_admin(chat, user.id):
        sql.update_flood(chat.id, None)
        return ""

    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return ""

    try:
        bot.restrict_chat_member(chat.id, user.id, can_send_messages=False)
        msg.reply_text(tld(chat.id, "I like to leave the flooding to natural disasters. But you, you were just a "
                       "disappointment. *Muted*!"))

        return "<b>{}:</b>" \
               "\n#MUTED" \
               "\n<b>User:</b> {}" \
               "\nFlooded the group.".format(html.escape(chat.title),
                                             mention_html(user.id, user.first_name))

    except BadRequest:
        msg.reply_text(tld(chat.id, "I can't mute people here, give me permissions first! Until then, I'll disable antiflood."))
        sql.set_flood(chat.id, 0)
        return "<b>{}:</b>" \
               "\n#INFO" \
               "\nDon't have mute permissions, so automatically disabled antiflood.".format(chat.title)


@run_async
@user_admin
@can_restrict
@loggable
def set_flood(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    if len(args) >= 1:
        val = args[0].lower()
        if val == "off" or val == "no" or val == "0":
            sql.set_flood(chat.id, 0)
            message.reply_text(tld(chat.id, "Antiflood has been disabled."))

        elif val.isdigit():
            amount = int(val)
            if amount <= 0:
                sql.set_flood(chat.id, 0)
                message.reply_text(tld(chat.id,  "Antiflood has been disabled."))
                return "<b>{}:</b>" \
                       "\n#SETFLOOD" \
                       "\n<b>Admin:</b> {}" \
                       "\nDisabled antiflood.".format(html.escape(chat.title), mention_html(user.id, user.first_name))

            elif amount < 3:
                message.reply_text(tld(chat.id, "Antiflood has to be either 0 (disabled), or a number bigger than 3 (enabled)!"))
                return ""

            else:
                sql.set_flood(chat.id, amount)
                message.reply_text(tld(chat.id, "Antiflood has been updated and set to {}").format(amount))
                return "<b>{}:</b>" \
                       "\n#SETFLOOD" \
                       "\n<b>Admin:</b> {}" \
                       "\nSet antiflood to <code>{}</code>.".format(html.escape(chat.title),
                                                                    mention_html(user.id, user.first_name), amount)

        else:
            message.reply_text(tld(chat.id, "Unrecognized argument - please use a number, 'off', or 'no'."))

    return ""


@run_async
def flood(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]

    limit = sql.get_flood_limit(chat.id)
    if limit == 0:
        update.effective_message.reply_text(tld(chat.id, "I'm not currently enforcing flood control!"))
    else:
        update.effective_message.reply_text(tld(chat.id,
            "I'm currently muting users if they send more than {} consecutive messages.").format(limit))


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(bot, update, chat, chatP, user):
    chat_id = chat.id
    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        return "*Not* currently enforcing flood control."
    else:
        return "Antiflood is set to `{}` messages.".format(limit)


__help__ = """
 You know how sometimes, people join, send 100 messages, and ruin your chat? With antiflood, that happens no more!

Antiflood allows you to take action on users that send more than x messages in a row. Actions are: ban/kick/mute/tban/tmute

Available commands are:
 - /flood: gets the current antiflood settings.
 - /setflood <number/off>: sets the number of messages at which to take action on a user.
"""

__mod_name__ = "AntiFlood"

FLOOD_BAN_HANDLER = MessageHandler(Filters.all & ~Filters.status_update & Filters.group, check_flood)
SET_FLOOD_HANDLER = CommandHandler("setflood", set_flood, pass_args=True, filters=Filters.group)
FLOOD_HANDLER = CommandHandler("flood", flood, filters=Filters.group)

dispatcher.add_handler(FLOOD_BAN_HANDLER, FLOOD_GROUP)
dispatcher.add_handler(SET_FLOOD_HANDLER)
dispatcher.add_handler(FLOOD_HANDLER)
