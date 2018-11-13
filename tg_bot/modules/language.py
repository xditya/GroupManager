from tg_bot.modules.sql.translation import switch_to_locale, prev_locale
from tg_bot.modules.translations.strings import tld
from telegram.ext import CommandHandler
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot import dispatcher
from tg_bot.modules.translations.list_locale import list_locales
from tg_bot.modules.helper_funcs.chat_status import user_admin
from telegram.ext import CallbackQueryHandler
import re

@user_admin
def locale(bot, update, args):
    chat = update.effective_chat
    if len(args) > 0:
        locale = args[0].lower()
        if locale in list_locales:
            if locale in  ('en', 'de', 'nl', 'id', 'fi', 'pt-br', 'ru'):
                switch_to_locale(chat.id, locale)
                update.message.reply_text(tld(chat.id, 'Switched to {} successfully!').format(list_locales[locale]))
            else:
                update.message.reply_text("{} not supported yet!".format(list_locales[locale]))
        else:
            update.message.reply_text("Is that even a valid language code? Use an internationally accepted ISO code!")
    else:
        LANGUAGE = prev_locale(chat.id)
        if LANGUAGE:
            locale = LANGUAGE.locale_name
            native_lang = list_locales[locale]
            update.message.reply_text("Current locale for this chat is: *{}*".format(native_lang), parse_mode = ParseMode.MARKDOWN)
        else:
            update.message.reply_text("Current locale for this chat is: *English*", parse_mode = ParseMode.MARKDOWN)

@user_admin
def locale_button(bot, update):
    chat = update.effective_chat
    query = update.callback_query
    lang_match = re.findall(r"en|ru", query.data)
    if lang_match:
        if lang_match[0]:
            switch_to_locale(chat.id, lang_match[0])
            text = tld(chat.id, "*Language changed*")
        else:
            text = "Im sorry, error!"

        query.message.reply_text(text, parse_mode=ParseMode.MARKDOWN,
                                                reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))
                                                                           
    else:
        query.message.reply_text(tld(chat.id, "*Select language*"), parse_mode=ParseMode.MARKDOWN,
                                                reply_markup=InlineKeyboardMarkup(
                                            [[InlineKeyboardButton("English 🇺🇸", callback_data="set_lang_en"),
                                            InlineKeyboardButton("Russian 🇷🇺", callback_data="set_lang_ru")]] + [[
                                                InlineKeyboardButton("Back", callback_data="help_back")]]))

    print(lang_match)
    query.message.delete()
    bot.answer_callback_query(query.id)

LOCALE_HANDLER = CommandHandler(["set_locale", "locale", "lang", "setlang"], locale, pass_args=True)
locale_handler = CallbackQueryHandler(locale_button, pattern="chng_lang")
set_locale_handler = CallbackQueryHandler(locale_button, pattern=r"set_lang_")

dispatcher.add_handler(LOCALE_HANDLER)
dispatcher.add_handler(locale_handler)
dispatcher.add_handler(set_locale_handler)
