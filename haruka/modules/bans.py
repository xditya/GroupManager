import html
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import run_async, CommandHandler, Filters
from telegram.utils.helpers import mention_html

from haruka import dispatcher, BAN_STICKER, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import bot_admin, user_admin, is_user_ban_protected, can_restrict, \
    is_user_admin, is_user_in_chat
from haruka.modules.helper_funcs.extraction import extract_user_and_text
from haruka.modules.helper_funcs.string_handling import extract_time
from haruka.modules.log_channel import loggable

from haruka.modules.translations.strings import tld


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

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

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "I'm not gonna BAN myself, are you crazy?"))
        return ""

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "Why would I ban an admin? That sounds like a pretty dumb idea."))
        return ""

    log = "<b>{}:</b>" \
          "\n#BANNED" \
          "\n<b>• Admin:</b> {}" \
          "\n<b>• User:</b> {}" \
          "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chat.title), mention_html(user.id, user.first_name), 
                                                  mention_html(member.user.id, member.user.first_name), user_id)

    reply = "{} has been banned!".format(mention_html(member.user.id, member.user.first_name))

    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id)
        #bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        message.reply_text(tld(chat.id, "Banned!"))
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            #bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
            message.reply_text(tld(chat.id, "Banned!"), quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text(tld(chat.id, "Well damn, I can't ban that user."))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

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

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "This user is ban protected, meaning that you cannot ban this user!"))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "I'm not gonna BAN myself, are you crazy?"))
        return ""

    if not reason:
        message.reply_text(tld(chat.id, "You haven't specified a time to ban this user for!"))
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    bantime = extract_time(message, time_val)

    if not bantime:
        return ""

    log = "<b>{}:</b>" \
          "\n#TEMP BANNED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {} (<code>{}</code>)" \
          "\n<b>Time:</b> {}".format(html.escape(chat.title),
                                     mention_html(user.id, user.first_name),
                                     mention_html(member.user.id, member.user.first_name),
                                     member.user.id,
                                     time_val)
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id, until_date=bantime)
        #bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        message.reply_text("Banned! User will be banned for {}.".format(time_val))
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            #bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
            message.reply_text(tld(chat.id, "Banned! User will be banned for {}.").format(time_val), quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text(tld(chat.id, "Well damn, I can't ban that user."))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def kick(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return ""
        else:
            raise

    if user_id == bot.id:
        message.reply_text("I'm not kicking myself!")
        return ""

    if is_user_ban_protected(chat, user_id):
        message.reply_text("Why would I kick an admin? That sounds like a pretty dumb idea.")
        return ""

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        #bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        message.reply_text("Kicked!")
        log = "<b>{}:</b>" \
              "\n#KICKED" \
              "\n<b>Admin:</b> {}" \
              "\n<b>User:</b> {} (<code>{}</code>)".format(html.escape(chat.title),
                                                           mention_html(user.id, user.first_name),
                                                           mention_html(member.user.id, member.user.first_name),
                                                           member.user.id)
        if reason:
            log += "\n<b>Reason:</b> {}".format(reason)

        return log

    else:
        message.reply_text("Well damn, I can't kick that user.")

    return ""


@run_async
@bot_admin
@can_restrict
def kickme(bot: Bot, update: Update):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("Why would I kick an admin? That sounds like a pretty dumb idea.")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("No problem.")
    else:
        update.effective_message.reply_text("Huh? I can't :/")


@run_async
@bot_admin
@can_restrict
@loggable
def banme(bot: Bot, update: Update):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("Why would I ban an admin? That sounds like a pretty dumb idea.")
        return

    res = update.effective_chat.kick_member(user_id)  
    if res:
        update.effective_message.reply_text("No problem, banned.")
        log = "<b>{}:</b>" \
              "\n#BANME" \
              "\n<b>User:</b> {}" \
              "\n<b>ID:</b> <code>{}</code>".format(html.escape(chat.title),
                                                    mention_html(user.id, user.first_name), user_id)
        return log

    else:
        update.effective_message.reply_text("Huh? I can't :/")


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def unban(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return ""
        else:
            raise

    if user_id == bot.id:
        message.reply_text("How would I unban myself if I wasn't here...?")
        return ""

    if is_user_in_chat(chat, user_id):
        message.reply_text("Why are you trying to unban someone that's already in the chat?")
        return ""

    chat.unban_member(user_id)
    message.reply_text("Yep, this user can join!")

    log = "<b>{}:</b>" \
          "\n#UNBANNED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {} (<code>{}</code>)".format(html.escape(chat.title),
                                                       mention_html(user.id, user.first_name),
                                                       mention_html(member.user.id, member.user.first_name),
                                                       member.user.id)
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    return log


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def sban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    update.effective_message.delete()

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            return ""
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        return ""

    if user_id == bot.id:
        return ""

    log = "<b>{}:</b>" \
          "\n# SILENTBAN" \
          "\n<b>• Admin:</b> {}" \
          "\n<b>• User:</b> {}" \
          "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chat.title), mention_html(user.id, user.first_name), 
                                                  mention_html(member.user.id, member.user.first_name), user_id)
    if reason:
        log += "\n<b>• Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id)
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id, excp.message)       
    return ""


__help__ = """
Some people need to be publicly banned; spammers, annoyances, or just trolls.

This module allows you to do that easily, by exposing some common actions, so everyone will see!

Available commands are:
 - /ban: bans a user from your chat.
 - /banme: ban yourself
 - /tban: temporarily bans a user from your chat. set time using int<d/h/m> (days hours minutes)
 - /unban: unbans a user from your chat.
 - /sban: silently bans a user. (via handle, or reply)
 - /mute: mute a user in your chat.
 - /tmute: temporarily mute a user in your chat. set time using int<d/h/m> (days hours minutes)
 - /unmute: unmutes a user from your chat.
 - /kick: kicks a user from your chat.
 - /kickme: users who use this, kick themselves!

 An example of temporarily muting someone:
/tmute @username 2h; this mutes a user for 2 hours.
"""

__mod_name__ = "Bans"

BAN_HANDLER = DisableAbleCommandHandler("ban", ban, pass_args=True, filters=Filters.group, admin_ok=True)
TEMPBAN_HANDLER = DisableAbleCommandHandler(["tban", "tempban"], temp_ban, pass_args=True, filters=Filters.group, admin_ok=True)
KICK_HANDLER = DisableAbleCommandHandler("kick", kick, pass_args=True, filters=Filters.group, admin_ok=True)
UNBAN_HANDLER = DisableAbleCommandHandler("unban", unban, pass_args=True, filters=Filters.group, admin_ok=True)
KICKME_HANDLER = DisableAbleCommandHandler("kickme", kickme, filters=Filters.group)
SBAN_HANDLER = DisableAbleCommandHandler("sban", sban, pass_args=True, filters=Filters.group, admin_ok=True)
BANME_HANDLER = DisableAbleCommandHandler("banme", banme, filters=Filters.group)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(BANME_HANDLER)
dispatcher.add_handler(SBAN_HANDLER)
