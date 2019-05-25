import html

from telegram import Bot, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, MessageHandler, run_async

import tldextract
from haruka import LOGGER, dispatcher
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import user_admin, user_not_admin
from haruka.modules.sql import urlblacklist_sql as sql


@run_async
@user_admin
def add_blacklist_url(bot: Bot, update: Update):
    chat = update.effective_chat
    message = update.effective_message
    urls = message.text.split(None, 1)
    if len(urls) > 1:
        urls = urls[1]
        to_blacklist = list(set(uri.strip()
                                for uri in urls.split("\n") if uri.strip()))
        blacklisted = []

        for uri in to_blacklist:
            extract_url = tldextract.extract(uri)
            if extract_url.domain and extract_url.suffix:
                blacklisted.append(extract_url.domain + "." + extract_url.suffix)
                sql.blacklist_url(chat.id, extract_url.domain + "." + extract_url.suffix)

        if len(to_blacklist) == 1:
            extract_url = tldextract.extract(to_blacklist[0])
            if extract_url.domain and extract_url.suffix:
                message.reply_text(
                    "Added <code>{}</code> domain to the blacklist!".format(
                        html.escape(
                            extract_url.domain + "." + extract_url.suffix)),
                    parse_mode=ParseMode.HTML)
            else:
                message.reply_text(
                    "You are trying to blacklist an invalid url")
        else:
            message.reply_text(
                "Added <code>{}</code> domains to the blacklist.".format(
                    len(blacklisted)), parse_mode=ParseMode.HTML)
    else:
        message.reply_text(
            "Tell me which urls you would like to add to the blacklist.")


@run_async
@user_admin
def rm_blacklist_url(bot: Bot, update: Update):
    chat = update.effective_chat
    message = update.effective_message
    urls = message.text.split(None, 1)

    if len(urls) > 1:
        urls = urls[1]
        to_unblacklist = list(set(uri.strip()
                                  for uri in urls.split("\n") if uri.strip()))
        unblacklisted = 0
        for uri in to_unblacklist:
            extract_url = tldextract.extract(uri)
            success = sql.rm_url_from_blacklist(chat.id, extract_url.domain + "." + extract_url.suffix)
            if success:
                unblacklisted += 1

        if len(to_unblacklist) == 1:
            if unblacklisted:
                message.reply_text(
                    "Removed <code>{}</code> from the blacklist!".format(
                        html.escape(
                            to_unblacklist[0])),
                    parse_mode=ParseMode.HTML)
            else:
                message.reply_text("This isn't a blacklisted domain...!")
        elif unblacklisted == len(to_unblacklist):
            message.reply_text(
                "Removed <code>{}</code> domains from the blacklist.".format(
                    unblacklisted), parse_mode=ParseMode.HTML)
        elif not unblacklisted:
            message.reply_text(
                "None of these domains exist, so they weren't removed.",
                parse_mode=ParseMode.HTML)
        else:
            message.reply_text(
                "Removed <code>{}</code> domains from the blacklist. {} did not exist, "
                "so were not removed.".format(
                    unblacklisted,
                    len(to_unblacklist) - unblacklisted),
                parse_mode=ParseMode.HTML)
    else:
        message.reply_text(
            "Tell me which domains you would like to remove from the blacklist.")


@run_async
@user_not_admin
def del_blacklist_url(bot: Bot, update: Update):
    chat = update.effective_chat
    message = update.effective_message
    parsed_entities = message.parse_entities(types=["url"])
    extracted_domains = []
    for obj, url in parsed_entities.items():
        extract_url = tldextract.extract(url)
        extracted_domains.append(extract_url.domain + "." + extract_url.suffix)
    for url in sql.get_blacklisted_urls(chat.id):
        if url in extracted_domains:
            try:
                message.delete()
            except BadRequest as excp:
                if excp.message == "Message to delete not found":
                    pass
                else:
                    LOGGER.exception("Error while deleting blacklist message.")
            break


@run_async
def get_blacklisted_urls(bot: Bot, update: Update):
    chat = update.effective_chat
    message = update.effective_message

    base_string = "Current <b>blacklisted</b> domains:\n"
    blacklisted = sql.get_blacklisted_urls(chat.id)

    if not blacklisted:
        message.reply_text("There are no blacklisted domains here!")
        return
    for domain in blacklisted:
        base_string += "- <code>{}</code>\n".format(domain)

    message.reply_text(base_string, parse_mode=ParseMode.HTML)


URL_BLACKLIST_HANDLER = DisableAbleCommandHandler(
    "blacklist",
    add_blacklist_url,
    filters=Filters.group,
    pass_args=True,
    admin_ok=True)
ADD_URL_BLACKLIST_HANDLER = CommandHandler(
    "addurl", add_blacklist_url, filters=Filters.group)

RM_BLACKLIST_URL_HANDLER = CommandHandler(
    "delurl", rm_blacklist_url, filters=Filters.group)

GET_BLACKLISTED_URLS = CommandHandler(
    "geturl",
    get_blacklisted_urls,
    filters=Filters.group)

URL_DELETE_HANDLER = MessageHandler(
    Filters.entity("url"),
    del_blacklist_url,
    edited_updates=True)


__mod_name__ = "Domain Blacklists"

__help__ = """
Domain blacklisting is used to stop certain domains from being mentioned in a group, Any time an url on that domain is mentioned, /
the message will immediately be deleted.

*NOTE:* domain blacklisting do not affect group admins.

- /geturl: View the current blacklisted urls

*Admin only:*

- /addurl <urls>: Add a domain to the blacklist. The bot will automatically parse the url.
- /delurl <urls>: Remove urls from the blacklist

"""

dispatcher.add_handler(URL_BLACKLIST_HANDLER)
dispatcher.add_handler(ADD_URL_BLACKLIST_HANDLER)
dispatcher.add_handler(RM_BLACKLIST_URL_HANDLER)
dispatcher.add_handler(GET_BLACKLISTED_URLS)
dispatcher.add_handler(URL_DELETE_HANDLER)
