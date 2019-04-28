import html
from io import BytesIO
from typing import Optional, List

from telegram import Message, Update, Bot, User, Chat, ParseMode, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_html

import haruka.modules.sql.antispam_sql as sql
from haruka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, STRICT_ANTISPAM
from haruka.modules.helper_funcs.chat_status import user_admin, is_user_admin
from haruka.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from haruka.modules.helper_funcs.filters import CustomFilters
from haruka.modules.helper_funcs.misc import send_to_list
from haruka.modules.sql.users_sql import get_all_chats

from haruka.modules.translations.strings import tld

GBAN_ENFORCE_GROUP = 6

GBAN_ERRORS = {
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

UNGBAN_ERRORS = {
    "User is an administrator of the chat",
    "Chat not found",
    "Not enough rights to restrict/unrestrict chat member",
    "User_not_participant",
    "Method is available for supergroup and channel chats only",
    "Not in the chat",
    "Channel_private",
    "Chat_admin_required",
}


@run_async
def gban(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]
    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return

    if int(user_id) in SUDO_USERS:
        message.reply_text("I spy, with my little eye... a sudo user war! Why are you guys turning on each other?")
        return

    if int(user_id) in SUPPORT_USERS:
        message.reply_text("OOOH someone's trying to gban a support user! *grabs popcorn*")
        return

    if user_id == bot.id:
        message.reply_text("-_- So funny, lets gban myself why don't I? Nice try.")
        return

    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        message.reply_text(excp.message)
        return

    if user_chat.type != 'private':
        message.reply_text("That's not a user!")
        return

    if sql.is_user_gbanned(user_id):
        if not reason:
            message.reply_text("This user is already gbanned; I'd change the reason, but you haven't given me one...")
            return

        old_reason = sql.update_gban_reason(user_id, user_chat.username or user_chat.first_name, reason)
        user_id, new_reason = extract_user_and_text(message, args)
        if old_reason:
            banner = update.effective_user  # type: Optional[User]
            send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                     "<b>New Reason of Global Ban</b>" \
                     "\n<b>Sudo Admin:</b> {}" \
                     "\n<b>User:</b> {}" \
                     "\n<b>ID:</b> <code>{}</code>" \
                     "\n<b>Previous Reason:</b> {}" \
                     "\n<b>New Reason:</b> {}".format(mention_html(banner.id, banner.first_name),
                                              mention_html(user_chat.id, user_chat.first_name or "Deleted Account"), 
                                                           user_chat.id, old_reason, new_reason), 
                    html=True)

            message.reply_text("This user is already gbanned, for the following reason:\n"
                               "<code>{}</code>\n"
                               "I've gone and updated it with your new reason!".format(html.escape(old_reason)),
                               parse_mode=ParseMode.HTML)
        else:
            banner = update.effective_user  # type: Optional[User]
            send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                     "<b>New reason of Global Ban</b>" \
                     "\n<b>Sudo Admin:</b> {}" \
                     "\n<b>User:</b> {}" \
                     "\n<b>ID:</b> <code>{}</code>" \
                     "\n<b>New Reason:</b> {}".format(mention_html(banner.id, banner.first_name or "Deleted Account"),
                                              mention_html(user_chat.id, user_chat.first_name), 
                                                           user_chat.id, new_reason), 
                    html=True)
            message.reply_text("This user is already gbanned, but had no reason set; I've gone and updated it!")

        return

    message.reply_text("*Blows dust off of banhammer* 😉")

    banner = update.effective_user  # type: Optional[User]
    send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                 "{} is gbanning user {} "
                 "because:\n{}".format(mention_html(banner.id, banner.first_name),
                                       mention_html(user_chat.id, user_chat.first_name), reason or "No reason given"),
                 html=True)

    sql.gban_user(user_id, user_chat.username or user_chat.first_name, reason)

    chats = get_all_chats()
    for chat in chats:
        chat_id = chat.chat_id

        # Check if this group has disabled gbans
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            bot.kick_chat_member(chat_id, user_id)
        except BadRequest as excp:
            if excp.message in GBAN_ERRORS:
                pass
            else:
                message.reply_text("Could not gban due to: {}".format(excp.message))
                send_to_list(bot, SUDO_USERS + SUPPORT_USERS, "Could not gban due to: {}".format(excp.message))
                sql.ungban_user(user_id)
                return
        except TelegramError:
            pass

    send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                   "{} has been successfully gbanned!".format(mention_html(user_chat.id, user_chat.first_name)),
                   html=True)

@run_async
def ungban(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message  # type: Optional[Message]

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return

    user_chat = bot.get_chat(user_id)
    if user_chat.type != 'private':
        message.reply_text("That's not a user!")
        return

    if not sql.is_user_gbanned(user_id):
        message.reply_text("This user is not gbanned!")
        return

    banner = update.effective_user  # type: Optional[User]

    message.reply_text("I'll give {} a second chance, globally.".format(user_chat.first_name))

    send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                 "{} has ungbanned user {}".format(mention_html(banner.id, banner.first_name),
                                                   mention_html(user_chat.id, user_chat.first_name)),
                 html=True)

    chats = get_all_chats()
    for chat in chats:
        chat_id = chat.chat_id

        # Check if this group has disabled gbans
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status == 'kicked':
                bot.unban_chat_member(chat_id, user_id)

        except BadRequest as excp:
            if excp.message in UNGBAN_ERRORS:
                pass
            else:
                message.reply_text("Could not un-gban due to: {}".format(excp.message))
                bot.send_message(OWNER_ID, "Could not un-gban due to: {}".format(excp.message))
                return
        except TelegramError:
            pass

    sql.ungban_user(user_id)

    send_to_list(bot, SUDO_USERS + SUPPORT_USERS, "un-gban complete!")

    message.reply_text("Person has been un-gbanned.")


@run_async
def gbanlist(bot: Bot, update: Update):
    banned_users = sql.get_gban_list()

    if not banned_users:
        update.effective_message.reply_text("There aren't any gbanned users! You're kinder than I expected...")
        return

    banfile = 'Screw these guys.\n'
    for user in banned_users:
        banfile += "[x] {} - {}\n".format(user["name"], user["user_id"])
        if user["reason"]:
            banfile += "Reason: {}\n".format(user["reason"])

    with BytesIO(str.encode(banfile)) as output:
        output.name = "gbanlist.txt"
        update.effective_message.reply_document(document=output, filename="gbanlist.txt",
                                                caption="Here is the list of currently gbanned users.")


def check_and_ban(update, user_id, should_message=True):
    if sql.is_user_gbanned(user_id):
        update.effective_chat.kick_member(user_id)
        if should_message:
            update.effective_message.reply_text("This is a bad person, they shouldn't be here!")

#GMUTE

@run_async
def gmute(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return

    if int(user_id) in SUDO_USERS:
        message.reply_text("I spy, with my little eye... a sudo user war! Why are you guys turning on each other?")
        return

    if int(user_id) in SUPPORT_USERS:
        message.reply_text("OOOH someone's trying to gmute a support user! *grabs popcorn*")
        return

    if user_id == bot.id:
        message.reply_text("-_- So funny, lets gmute myself why don't I? Nice try.")
        return

    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        message.reply_text(excp.message)
        return

    if user_chat.type != 'private':
        message.reply_text("That's not a user!")
        return

    if sql.is_user_gmuted(user_id):
        if not reason:
            message.reply_text("This user is already gmuted; I'd change the reason, but you haven't given me one...")
            return

        success = sql.update_gmute_reason(user_id, user_chat.username or user_chat.first_name, reason)
        if success:
            message.reply_text("This user is already gmuted; I've gone and updated the gmute reason though!")
        else:
            message.reply_text("Do you mind trying again? I thought this person was gmuted, but then they weren't? "
                               "Am very confused")

        return

    message.reply_text("*Gets duct tape ready* 😉")

    muter = update.effective_user  # type: Optional[User]
    send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                 "{} is gmuting user {} "
                 "because:\n{}".format(mention_html(muter.id, muter.first_name),
                                       mention_html(user_chat.id, user_chat.first_name), reason or "No reason given"),
                 html=True)

    sql.gmute_user(user_id, user_chat.username or user_chat.first_name, reason)

    chats = get_all_chats()
    for chat in chats:
        chat_id = chat.chat_id

        # Check if this group has disabled gmutes
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)
        except BadRequest as excp:
            if excp.message == "User is an administrator of the chat":
                pass
            elif excp.message == "Chat not found":
                pass
            elif excp.message == "Not enough rights to restrict/unrestrict chat member":
                pass
            elif excp.message == "User_not_participant":
                pass
            elif excp.message == "Peer_id_invalid":  # Suspect this happens when a group is suspended by telegram.
                pass
            elif excp.message == "Group chat was deactivated":
                pass
            elif excp.message == "Need to be inviter of a user to kick it from a basic group":
                pass
            elif excp.message == "Chat_admin_required":
                pass
            elif excp.message == "Only the creator of a basic group can kick group administrators":
                pass
            elif excp.message == "Method is available only for supergroups":
                pass
            elif excp.message == "Can't demote chat creator":
                pass
            else:
                message.reply_text("Could not gmute due to: {}".format(excp.message))
                send_to_list(bot, SUDO_USERS + SUPPORT_USERS, "Could not gmute due to: {}".format(excp.message))
                sql.ungmute_user(user_id)
                return
        except TelegramError:
            pass

    send_to_list(bot, SUDO_USERS + SUPPORT_USERS, "gmute complete!")
    message.reply_text("Person has been gmuted.")


@run_async
def ungmute(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message  # type: Optional[Message]

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return

    user_chat = bot.get_chat(user_id)
    if user_chat.type != 'private':
        message.reply_text("That's not a user!")
        return

    if not sql.is_user_gmuted(user_id):
        message.reply_text("This user is not gmuted!")
        return

    muter = update.effective_user  # type: Optional[User]

    message.reply_text("I'll let {} speak again, globally.".format(user_chat.first_name))

    send_to_list(bot, SUDO_USERS + SUPPORT_USERS,
                 "{} has ungmuted user {}".format(mention_html(muter.id, muter.first_name),
                                                   mention_html(user_chat.id, user_chat.first_name)),
                 html=True)

    chats = get_all_chats()
    for chat in chats:
        chat_id = chat.chat_id

        # Check if this group has disabled gmutes
        if not sql.does_chat_gban(chat_id):
            continue

        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status == 'restricted':
                bot.restrict_chat_member(chat_id, int(user_id),
                                     can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_other_messages=True,
                                     can_add_web_page_previews=True)

        except BadRequest as excp:
            if excp.message == "User is an administrator of the chat":
                pass
            elif excp.message == "Chat not found":
                pass
            elif excp.message == "Not enough rights to restrict/unrestrict chat member":
                pass
            elif excp.message == "User_not_participant":
                pass
            elif excp.message == "Method is available for supergroup and channel chats only":
                pass
            elif excp.message == "Not in the chat":
                pass
            elif excp.message == "Channel_private":
                pass
            elif excp.message == "Chat_admin_required":
                pass
            else:
                message.reply_text("Could not un-gmute due to: {}".format(excp.message))
                bot.send_message(OWNER_ID, "Could not un-gmute due to: {}".format(excp.message))
                return
        except TelegramError:
            pass

    sql.ungmute_user(user_id)

    send_to_list(bot, SUDO_USERS + SUPPORT_USERS, "un-gmute complete!")

    message.reply_text("Person has been un-gmuted.")


@run_async
def gmutelist(bot: Bot, update: Update):
    muted_users = sql.get_gmute_list()

    if not muted_users:
        update.effective_message.reply_text("There aren't any gmuted users! You're kinder than I expected...")
        return

    mutefile = 'Screw these guys.\n'
    for user in muted_users:
        mutefile += "[x] {} - {}\n".format(user["name"], user["user_id"])
        if user["reason"]:
            mutefile += "Reason: {}\n".format(user["reason"])

    with BytesIO(str.encode(mutefile)) as output:
        output.name = "gmutelist.txt"
        update.effective_message.reply_document(document=output, filename="gmutelist.txt",
                                                caption="Here is the list of currently gmuted users.")


def check_and_mute(bot, update, user_id, should_message=True):
    if sql.is_user_gmuted(user_id):
        bot.restrict_chat_member(update.effective_chat.id, user_id, can_send_messages=False)
        if should_message:
            update.effective_message.reply_text("This is a bad person, I'll silence them for you!")


@run_async
def enforce_gmute(bot: Bot, update: Update):
    # Not using @restrict handler to avoid spamming - just ignore if cant gmute.
    if sql.does_chat_gban(update.effective_chat.id) and update.effective_chat.get_member(bot.id).can_restrict_members:
        user = update.effective_user  # type: Optional[User]
        chat = update.effective_chat  # type: Optional[Chat]
        msg = update.effective_message  # type: Optional[Message]

        if user and not is_user_admin(chat, user.id):
            check_and_mute(bot, update, user.id, should_message=True)
        if msg.new_chat_members:
            new_members = update.effective_message.new_chat_members
            for mem in new_members:
                check_and_mute(bot, update, mem.id, should_message=True)
        if msg.reply_to_message:
            user = msg.reply_to_message.from_user  # type: Optional[User]
            if user and not is_user_admin(chat, user.id):
                check_and_mute(bot, update, user.id, should_message=True)


@run_async
def enforce_gban(bot: Bot, update: Update):
    # Not using @restrict handler to avoid spamming - just ignore if cant gban.
    if sql.does_chat_gban(update.effective_chat.id) and update.effective_chat.get_member(bot.id).can_restrict_members:
        user = update.effective_user  # type: Optional[User]
        chat = update.effective_chat  # type: Optional[Chat]
        msg = update.effective_message  # type: Optional[Message]

        if user and not is_user_admin(chat, user.id):
            check_and_ban(update, user.id)

        if msg.new_chat_members:
            new_members = update.effective_message.new_chat_members
            for mem in new_members:
                check_and_ban(update, mem.id)

        if msg.reply_to_message:
            user = msg.reply_to_message.from_user  # type: Optional[User]
            if user and not is_user_admin(chat, user.id):
                check_and_ban(update, user.id, should_message=False)


@run_async
@user_admin
def antispam(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    if len(args) > 0:
        if args[0].lower() in ["on", "yes"]:
            sql.enable_antispam(chat.id)
            update.effective_message.reply_text(tld(chat.id, "I've enabled antispam security in this group. This will help protect you "
                                                "from spammers, unsavoury characters, and the biggest trolls."))
        elif args[0].lower() in ["off", "no"]:
            sql.disable_antispam(chat.id)
            update.effective_message.reply_text(tld(chat.id, "I've disabled antispam security in this group. GBans wont affect your users "
                                                "anymore. You'll be less protected from any trolls and spammers "
                                                "though!"))
    else:
        update.effective_message.reply_text(tld(chat.id, "Give me some arguments to choose a setting! on/off, yes/no!\n\n"
                                            "Your current setting is: {}\n"
                                            "When True, any gbans that happen will also happen in your group. "
                                            "When False, they won't, leaving you at the possible mercy of "
                                            "spammers.").format(sql.does_chat_gban(chat.id)))

#Gkick

GKICK_ERRORS = {
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
    "Not in the chat",
    "Method is available for supergroup and channel chats only",
    "Reply message not found"
}

@run_async
def gkick(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id = extract_user(message, args)
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        if excp.message in GKICK_ERRORS:
            pass
        else:
            message.reply_text("User cannot be Globally kicked because: {}".format(excp.message))
            return
    except TelegramError:
            pass

    if not user_id:
        message.reply_text("You do not seems to be referring to a user")
        return
    if int(user_id) in SUDO_USERS or int(user_id) in SUPPORT_USERS:
        message.reply_text("OHHH! Someone's trying to gkick a sudo/support user! *Grabs popcorn*")
        return
    if int(user_id) == OWNER_ID:
        message.reply_text("Wow! Some's trying to gkick my owner! *Grabs Potato Chips*")
        return
        
    if user_id == bot.id:
        message.reply_text("Welp, I'm not gonna gkick myself!")
        return

    if int(user_id) in SUDO_USERS:
        message.reply_text("")
        return

    chats = get_all_chats()
    message.reply_text("Globally kicking user @{}".format(user_chat.username))
    for chat in chats:
        try:
            bot.unban_chat_member(chat.chat_id, user_id)  # Unban_member = kick (and not ban)
        except BadRequest as excp:
            if excp.message in GKICK_ERRORS:
                pass
            else:
                message.reply_text("User cannot be Globally kicked because: {}".format(excp.message))
                return
        except TelegramError:
            pass


def __stats__():
    return "{} gbanned users.\n{} gmuted users.".format(sql.num_gbanned_users(), sql.num_gmuted_users())
    


def __user_info__(user_id, chat_id):
    is_gbanned = sql.is_user_gbanned(user_id)
    is_gmuted = sql.is_user_gmuted(user_id)

    if not user_id in SUDO_USERS:

        text = tld(chat_id, "Globally banned: <b>{}</b>")
        if is_gbanned:
            text = text.format(tld(chat_id, "Yes"))
            user = sql.get_gbanned_user(user_id)
            if user.reason:
                text += tld(chat_id, "\nReason: {}").format(html.escape(user.reason))
        else:
            text = text.format(tld(chat_id, "No"))
        
        text += tld(chat_id, "\nGlobally muted: <b>{}</b>")
        if is_gmuted:
            text = text.format(tld(chat_id, "Yes"))
            user = sql.get_gmuted_user(user_id)
            if user.reason:
                text += tld(chat_id, "\nReason: {}").format(html.escape(user.reason))
        else:
            text = text.format(tld(chat_id, "No"))

        return text
    else:
        return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(bot, update, chat, chatP, user):
    chat_id = chat.id
    return "This chat is enforcing *gbans*: `{}`.".format(sql.does_chat_gban(chat_id))


__help__ = """
*Admin only:*
 - /antispam <on/off/yes/no>: Will disable antispam security in group, or return your current settings.

Antispam are used by the bot owners to ban spammers across all groups. This helps protect \
you and your groups by removing spam flooders as quickly as possible. They can be disabled for you group by calling \
/antispam
"""

__mod_name__ = "Antispam security"

ANTISPAM_STATUS = CommandHandler("antispam", antispam, pass_args=True, filters=Filters.group)

GBAN_HANDLER = CommandHandler("gban", gban, pass_args=True,
                              filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
UNGBAN_HANDLER = CommandHandler("ungban", ungban, pass_args=True,
                                filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
GBAN_LIST = CommandHandler("gbanlist", gbanlist,
                           filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
GBAN_ENFORCER = MessageHandler(Filters.all & Filters.group, enforce_gban)


GMUTE_HANDLER = CommandHandler("gmute", gmute, pass_args=True,
                              filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
UNGMUTE_HANDLER = CommandHandler("ungmute", ungmute, pass_args=True,
                                filters=CustomFilters.sudo_filter | CustomFilters.support_filter)
GMUTE_LIST = CommandHandler("gmutelist", gmutelist,
                           filters=CustomFilters.sudo_filter | CustomFilters.support_filter)


GKICK_HANDLER = CommandHandler("gkick", gkick, pass_args=True,
                              filters=CustomFilters.sudo_filter | CustomFilters.support_filter)

dispatcher.add_handler(ANTISPAM_STATUS)

dispatcher.add_handler(GBAN_HANDLER)
dispatcher.add_handler(UNGBAN_HANDLER)
dispatcher.add_handler(GBAN_LIST)

dispatcher.add_handler(GMUTE_HANDLER)
dispatcher.add_handler(UNGMUTE_HANDLER)
dispatcher.add_handler(GMUTE_LIST)

dispatcher.add_handler(GKICK_HANDLER)


if STRICT_ANTISPAM:  # enforce GBANS if this is set
    dispatcher.add_handler(GBAN_ENFORCER, GBAN_ENFORCE_GROUP)
