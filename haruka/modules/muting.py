import html
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, User, CallbackQuery

from haruka import dispatcher, LOGGER, SUDO_USERS
from haruka.modules.helper_funcs.chat_status import bot_admin, user_admin, is_user_admin, can_restrict
from haruka.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from haruka.modules.helper_funcs.string_handling import extract_time
from haruka.modules.log_channel import loggable

from haruka.modules.translations.strings import tld
from haruka.modules.connection import connected
from haruka.modules.disable import DisableAbleCommandHandler


@run_async
@bot_admin
@user_admin
@loggable
def mute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            exit(1)
        else:
            chatD = chat

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "You'll need to either give me a username to mute, or reply to someone to be muted."))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "I'm not muting myself!"))
        return ""

    member = chatD.get_member(int(user_id))

    if member:

        if user_id in SUDO_USERS:
            message.reply_text(tld(chat.id, "No! I'm not muting bot sudoers! That would be a pretty dumb idea."))

        elif is_user_admin(chatD, user_id, member=member):
            message.reply_text(tld(chat.id, "No! I'm not muting chat administrator! That would be a pretty dumb idea."))

        elif member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chatD.id, user_id, can_send_messages=False)
            keyboard = []
            reply = tld(chat.id, "{} is muted in {}!").format(mention_html(member.user.id, member.user.first_name), chatD.title)
            message.reply_text(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#MUTE" \
                   "\n<b>Admin:</b> {}" \
                   "\n<b>User:</b> {}".format(html.escape(chatD.title),
                                              mention_html(user.id, user.first_name),
                                              mention_html(member.user.id, member.user.first_name))

        else:
            message.reply_text(tld(chat.id, "This user is already muted in {}!").format(chatD.title))
    else:
        message.reply_text(tld(chat.id, "This user isn't in the {}!").format(chatD.title))

    return ""


@run_async
@bot_admin
@user_admin
@loggable
def unmute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            exit(1)
        else:
            chatD = chat


    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "You'll need to either give me a username to unmute, or reply to someone to be unmuted."))
        return ""

    member = chatD.get_member(int(user_id))

    if member.status != 'kicked' and member.status != 'left':
        if member.can_send_messages and member.can_send_media_messages \
                and member.can_send_other_messages and member.can_add_web_page_previews:
            message.reply_text(tld(chat.id, "This user already has the right to speak in {}.").format(chatD.title))
        else:
            bot.restrict_chat_member(chatD.id, int(user_id),
                                     can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_other_messages=True,
                                     can_add_web_page_previews=True)
            keyboard = []
            reply = tld(chat.id, "Yep, {} can start talking again in {}!").format(mention_html(member.user.id, member.user.first_name), chatD.title)
            message.reply_text(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#UNMUTE" \
                   "\n<b>• Admin:</b> {}" \
                   "\n<b>• User:</b> {}" \
                   "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chatD.title),
                                                           mention_html(user.id, user.first_name),
                                                           mention_html(member.user.id, member.user.first_name), user_id)
    else:
        message.reply_text(tld(chat.id, "This user isn't even in the chat, unmuting them won't make them talk more than they "
                           "already do!"))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_mute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            exit(1)
        else:
            chatD = chat

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a user."))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "I can't seem to find this user"))
            return ""
        else:
            raise

    if is_user_admin(chat, user_id, member):
        message.reply_text(tld(chat.id, "I really wish I could mute admins..."))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "I'm not gonna MUTE myself, are you crazy?"))
        return ""

    if not reason:
        message.reply_text(tld(chat.id, "You haven't specified a time to mute this user for!"))
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = "<b>{}:</b>" \
          "\n#TEMP MUTED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {}" \
          "\n<b>Time:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name),
                                     mention_html(member.user.id, member.user.first_name), time_val)
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        if member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chat.id, user_id, until_date=mutetime, can_send_messages=False)
            message.reply_text(tld(chat.id, "Muted for {} in {}!").format(time_val, chatD.title))
            return log
        else:
            message.reply_text(tld(chat.id, "This user is already muted in {}!").format(chatD.title))

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(tld(chat.id, "Muted for {} in {}!").format(time_val, chatD.title), quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR muting user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text(tld(chat.id, "Well damn, I can't mute that user."))

    return ""


@run_async
@bot_admin
@user_admin
@loggable
def nomedia(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            exit(1)
        else:
            chatD = chat

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "You'll need to either give me a username to restrict, or reply to someone to be restricted."))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "I'm not restricting myself!"))
        return ""

    member = chatD.get_member(int(user_id))

    if member:
        if is_user_admin(chatD, user_id, member=member):
            message.reply_text(tld(chat.id, "Afraid I can't restrict admins!"))

        elif member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chatD.id, user_id, can_send_messages=True,
                                     can_send_media_messages=False,
                                     can_send_other_messages=False,
                                     can_add_web_page_previews=False)
            keyboard = []
            reply = tld(chat.id, "{} is restricted from sending media in {}!").format(mention_html(member.user.id, member.user.first_name), chatD.title)
            message.reply_text(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#RESTRICTED" \
                   "\n<b>• Admin:</b> {}" \
                   "\n<b>• User:</b> {}" \
                   "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chatD.title),
                                              mention_html(user.id, user.first_name),
                                              mention_html(member.user.id, member.user.first_name), user_id)

        else:
            message.reply_text(tld(chat.id, "This user is already restricted in {}!"))
    else:
        message.reply_text(tld(chat.id, "This user isn't in the {}!").format(chatD.title))

    return ""


@run_async
@bot_admin
@user_admin
@loggable
def media(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            exit(1)
        else:
            chatD = chat

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "You'll need to either give me a username to unrestrict, or reply to someone to be unrestricted."))
        return ""

    member = chatD.get_member(int(user_id))

    if member.status != 'kicked' and member.status != 'left':
        if member.can_send_messages and member.can_send_media_messages \
                and member.can_send_other_messages and member.can_add_web_page_previews:
            message.reply_text(tld(chat.id, "This user already has the rights to send anything in {}.").format(chatD.title))
        else:
            bot.restrict_chat_member(chatD.id, int(user_id),
                                     can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_other_messages=True,
                                     can_add_web_page_previews=True)
            keyboard = []
            reply = tld(chat.id, "Yep, {} can send media again in {}!").format(mention_html(member.user.id, member.user.first_name), chatD.title)
            message.reply_text(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#UNRESTRICTED" \
                   "\n<b>• Admin:</b> {}" \
                   "\n<b>• User:</b> {}" \
                   "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chatD.title),
                                                           mention_html(user.id, user.first_name),
                                                           mention_html(member.user.id, member.user.first_name), user_id)
    else:
        message.reply_text(tld(chat.id, "This user isn't even in the chat, unrestricting them won't make them send anything than they "
                           "already do!"))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_nomedia(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            exit(1)
        else:
            chatD = chat

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "You don't seem to be referring to a user."))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "I can't seem to find this user"))
            return ""
        else:
            raise

    if is_user_admin(chat, user_id, member):
        message.reply_text(tld(chat.id, "I really wish I could restrict admins..."))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "I'm not gonna RESTRICT myself, are you crazy?"))
        return ""

    if not reason:
        message.reply_text(tld(chat.id, "You haven't specified a time to restrict this user for!"))
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = "<b>{}:</b>" \
          "\n#TEMP RESTRICTED" \
          "\n<b>• Admin:</b> {}" \
          "\n<b>• User:</b> {}" \
          "\n<b>• ID:</b> <code>{}</code>" \
          "\n<b>• Time:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name),
                                       mention_html(member.user.id, member.user.first_name), user_id, time_val)
    if reason:
        log += "\n<b>• Reason:</b> {}".format(reason)

    try:
        if member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chat.id, user_id, until_date=mutetime, can_send_messages=True,
                                     can_send_media_messages=False,
                                     can_send_other_messages=False,
                                     can_add_web_page_previews=False)
            message.reply_text(tld(chat.id, "Restricted from sending media for {} in {}!").format(time_val, chatD.title))
            return log
        else:
            message.reply_text(tld(chat.id, "This user is already restricted in {}.").format(chatD.title))

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(tld(chat.id, "Restricted for {} in {}!").format(time_val, chatD.title), quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR muting user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text(tld(chat.id, "Well damn, I can't restrict that user."))

    return ""


@run_async
@bot_admin
@can_restrict
def muteme(bot: Bot, update: Update, args: List[str]) -> str:
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("I wish I could... but you're an admin.")
        return

    res = bot.restrict_chat_member(chat.id, user_id, can_send_messages=False)
    if res:
        update.effective_message.reply_text("No problem, Muted!")
        log = "<b>{}:</b>" \
              "\n#MUTEME" \
              "\n<b>User:</b> {}" \
              "\n<b>ID:</b> <code>{}</code>".format(html.escape(chat.title),
                                                    mention_html(user.id, user.first_name), user_id)
        return log

    else:
        update.effective_message.reply_text("Huh? I can't :/")


MUTE_HANDLER = DisableAbleCommandHandler("mute", mute, pass_args=True, admin_ok=True)
UNMUTE_HANDLER = DisableAbleCommandHandler("unmute", unmute, pass_args=True, admin_ok=True)
TEMPMUTE_HANDLER = DisableAbleCommandHandler(["tmute", "tempmute"], temp_mute, pass_args=True, admin_ok=True)
TEMP_NOMEDIA_HANDLER = DisableAbleCommandHandler(["trestrict", "temprestrict"], temp_nomedia, pass_args=True, admin_ok=True)
NOMEDIA_HANDLER = DisableAbleCommandHandler(["restrict", "nomedia"], nomedia, pass_args=True, admin_ok=True)
MEDIA_HANDLER = DisableAbleCommandHandler("unrestrict", media, pass_args=True, admin_ok=True)
MUTEME_HANDLER = DisableAbleCommandHandler("muteme", muteme, pass_args=True, filters=Filters.group, admin_ok=True)

dispatcher.add_handler(MUTE_HANDLER)
dispatcher.add_handler(UNMUTE_HANDLER)
dispatcher.add_handler(TEMPMUTE_HANDLER)
dispatcher.add_handler(TEMP_NOMEDIA_HANDLER)
dispatcher.add_handler(NOMEDIA_HANDLER)
dispatcher.add_handler(MEDIA_HANDLER)
dispatcher.add_handler(MUTEME_HANDLER)
