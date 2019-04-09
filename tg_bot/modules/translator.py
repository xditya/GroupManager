from typing import Optional, List

from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async

from tg_bot import dispatcher, LOGGER
from tg_bot.modules.disable import DisableAbleCommandHandler

from py_translator import Translator


@run_async
def do_translate(bot: Bot, update: Update, args: List[str]):
    short_name = "Created By @MidukkiBot 😬"
    msg = update.effective_message # type: Optional[Message]
    lan = " ".join(args)
    to_translate_text = msg.reply_to_message.text
    translator = Translator()
    try:
        translated = translator.translate(to_translate_text, dest=lan)
        src_lang = translated.src
        translated_text = translated.text
        msg.reply_text("Translated from {} to {}.\n {}".format(src_lang, lan, translated_text))
    except exc:
        msg.reply_text(str(exc))


__help__ = """- /tr (language code) as reply to a long message.
"""
__mod_name__ = "Google Translate"

dispatcher.add_handler(DisableAbleCommandHandler("tr", do_translate, pass_args=True))
