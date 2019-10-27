import re
from typing import Optional

import telegram
from telegram import ParseMode, InlineKeyboardMarkup, Message, Chat
from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import CommandHandler, MessageHandler, DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown

from haruka import dispatcher, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import user_admin
from haruka.modules.helper_funcs.extraction import extract_text
from haruka.modules.helper_funcs.filters import CustomFilters
from haruka.modules.helper_funcs.misc import build_keyboard
from haruka.modules.helper_funcs.string_handling import split_quotes, button_markdown_parser
from haruka.modules.sql import cust_filters_sql as sql

from haruka.modules.translations.strings import tld

from haruka.modules.connection import connected

HANDLER_GROUP = 10


@run_async
def list_handlers(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    
    conn = connected(bot, update, chat, user.id, need_admin=False)
    if not conn == False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
        filter_list = tld(chat.id, "*List of filters in {}:*\n")
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = tld(chat.id, "local filters")
            filter_list = tld(chat.id, "*local filters:*\n")
        else:
            chat_name = chat.title
            filter_list = tld(chat.id, "*Filters in {}*:\n")

    all_handlers = sql.get_chat_triggers(chat_id)

    if not all_handlers:
        update.effective_message.reply_text(tld(chat.id, "No filters in {}!").format(chat_name))
        return

    for keyword in all_handlers:
        entry = " • `{}`\n".format(escape_markdown(keyword))
        if len(entry) + len(filter_list) > telegram.MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(filter_list.format(chat_name), parse_mode=telegram.ParseMode.MARKDOWN)
            filter_list = entry
        else:
            filter_list += entry

    update.effective_message.reply_text(filter_list.format(chat_name), parse_mode=telegram.ParseMode.MARKDOWN)

# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@user_admin
def filters(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    args = msg.text.split(None, 1)  # use python's maxsplit to separate Cmd, keyword, and reply_text

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "local notes"
        else:
            chat_name = chat.title

    if len(args) < 2:
        return

    extracted = split_quotes(args[1])
    if len(extracted) < 1:
        return
    # set trigger -> lower, so as to avoid adding duplicate filters with different cases
    keyword = extracted[0].lower()

    is_sticker = False
    is_document = False
    is_image = False
    is_voice = False
    is_audio = False
    is_video = False
    buttons = []

    # determine what the contents of the filter are - text, image, sticker, etc
    if len(extracted) >= 2:
        offset = len(extracted[1]) - len(msg.text)  # set correct offset relative to command + notename
        content, buttons = button_markdown_parser(extracted[1], entities=msg.parse_entities(), offset=offset)
        content = content.strip()
        if not content:
            msg.reply_text(tld(chat.id, "There is no note message - You can't JUST have buttons, you need a message to go with it!"))
            return

    elif msg.reply_to_message and msg.reply_to_message.sticker:
        content = msg.reply_to_message.sticker.file_id
        is_sticker = True

    elif msg.reply_to_message and msg.reply_to_message.document:
        content = msg.reply_to_message.document.file_id
        is_document = True

    elif msg.reply_to_message and msg.reply_to_message.photo:
        content = msg.reply_to_message.photo[-1].file_id  # last elem = best quality
        is_image = True

    elif msg.reply_to_message and msg.reply_to_message.audio:
        content = msg.reply_to_message.audio.file_id
        is_audio = True

    elif msg.reply_to_message and msg.reply_to_message.voice:
        content = msg.reply_to_message.voice.file_id
        is_voice = True

    elif msg.reply_to_message and msg.reply_to_message.video:
        content = msg.reply_to_message.video.file_id
        is_video = True

    else:
        msg.reply_text(tld(chat.id, "You didn't specify what to reply with!"))
        return

    # Add the filter
    # Note: perhaps handlers can be removed somehow using sql.get_chat_filters
    for handler in dispatcher.handlers.get(HANDLER_GROUP, []):
        if handler.filters == (keyword, chat_id):
            dispatcher.remove_handler(handler, HANDLER_GROUP)

    sql.add_filter(chat_id, keyword, content, is_sticker, is_document, is_image, is_audio, is_voice, is_video,
                   buttons)

    msg.reply_text(tld(chat.id, "Handler '{}' added in *{}*!").format(keyword, chat_name), parse_mode=telegram.ParseMode.MARKDOWN)
    raise DispatcherHandlerStop


# NOT ASYNC BECAUSE DISPATCHER HANDLER RAISED
@user_admin
def stop_filter(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    args = update.effective_message.text.split(None, 1)

    conn = connected(bot, update, chat, user.id)
    if not conn == False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = "local notes"
        else:
            chat_name = chat.title

    if len(args) < 2:
        return

    chat_filters = sql.get_chat_triggers(chat_id)

    if not chat_filters:
        update.effective_message.reply_text(tld(chat.id, "No filters are active in {}!").format(chat_name))
        return

    for keyword in chat_filters:
        if keyword == args[1]:
            sql.remove_filter(chat_id, args[1])
            update.effective_message.reply_text(tld(chat.id, "Yep, I'll stop replying to that in *{}*.").format(chat_name), parse_mode=telegram.ParseMode.MARKDOWN)
            raise DispatcherHandlerStop

    update.effective_message.reply_text(tld(chat.id, "That's not a current filter - run /filters for all active filters."))


@run_async
def reply_filter(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]
    to_match = extract_text(message)
    if not to_match:
        return

    chat_filters = sql.get_chat_triggers(chat.id)
    for keyword in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            filt = sql.get_filter(chat.id, keyword)
            if filt.is_sticker:
                message.reply_sticker(filt.reply)
            elif filt.is_document:
                try:
                    message.reply_document(filt.reply)
                except:
                    print("L")
            elif filt.is_image:
                message.reply_photo(filt.reply)
            elif filt.is_audio:
                message.reply_audio(filt.reply)
            elif filt.is_voice:
                message.reply_voice(filt.reply)
            elif filt.is_video:
                try:
                    message.reply_video(filt.reply)
                except:
                    print("Nut")
            elif filt.has_markdown:
                buttons = sql.get_buttons(chat.id, filt.keyword)
                keyb = build_keyboard(buttons)
                keyboard = InlineKeyboardMarkup(keyb)

                try:
                    message.reply_text(filt.reply, parse_mode=ParseMode.MARKDOWN,
                                       disable_web_page_preview=True,
                                       reply_markup=keyboard)
                except BadRequest as excp:
                    if excp.message == "Unsupported url protocol":
                        message.reply_text("You seem to be trying to use an unsupported url protocol. Telegram "
                                           "doesn't support buttons for some protocols, such as tg://. Please try "
                                           "again, or ask in @HarukaAyaGroup for help.")
                    elif excp.message == "Reply message not found":
                        bot.send_message(chat.id, filt.reply, parse_mode=ParseMode.MARKDOWN,
                                         disable_web_page_preview=True,
                                         reply_markup=keyboard)
                    else:
                        try:
                            message.reply_text("This note could not be sent, as it is incorrectly formatted. Ask in @HarukaAyaGroup if you can't figure out why!")
                            LOGGER.warning("Message %s could not be parsed", str(filt.reply))
                            LOGGER.exception("Could not parse filter %s in chat %s", str(filt.keyword), str(chat.id))
                        except:
                            print("Nut")

            else:
                # LEGACY - all new filters will have has_markdown set to True.
                message.reply_text(filt.reply)
            break


def __stats__():
    return "{} filters, across {} chats.".format(sql.num_filters(), sql.num_chats())


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(bot, update, chat, chatP, user):
    cust_filters = sql.get_chat_triggers(chat.id)
    return "There are `{}` custom filters here.".format(len(cust_filters))


def __import_data__(chat_id, data):
    # set chat filters
    filters = data.get('filters', {})
    for trigger in filters:
        sql.add_to_blacklist(chat_id, trigger)


__help__ = """
Make your chat more lively with filters; The bot will reply to certain words!
Filters are case insensitive; every time someone says your trigger words, {} will reply something else! can be used to create your own commands, if desired.
 - /filters: list all active filters in this chat.
*Admin only:*
 - /filter <keyword> <reply message>: Every time someone says "word", the bot will reply with "sentence". For multiple word filters, quote the first word.
 - /stop <filter keyword>: stop that filter.
 
 An example of how to set a filter would be via:
`/filter hello Hello there! How are you?`
A multiword filter could be set via:
`/filter "hello friend" Hello back! Long time no see!`
If you want to save an image, gif, or sticker, or any other data, do the following:
`/filter word while replying to a sticker or whatever data you'd like. Now, every time someone mentions "word", that sticker will be sent as a reply.`
Now, anyone saying "hello" will be replied to with "Hello there! How are you?".
"""

__mod_name__ = "Filters"

FILTER_HANDLER = DisableAbleCommandHandler("filter", filters)
STOP_HANDLER = DisableAbleCommandHandler("stop", stop_filter)
LIST_HANDLER = DisableAbleCommandHandler("filters", list_handlers, admin_ok=True)
CUST_FILTER_HANDLER = MessageHandler(CustomFilters.has_text, reply_filter)

dispatcher.add_handler(FILTER_HANDLER)
dispatcher.add_handler(STOP_HANDLER)
dispatcher.add_handler(LIST_HANDLER)
dispatcher.add_handler(CUST_FILTER_HANDLER, HANDLER_GROUP)
