from typing import Optional, List

from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.ext import Filters, MessageHandler, run_async

from haruka import dispatcher, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler

from googletrans import Translator


@run_async
def do_translate(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message # type: Optional[Message]
    lan = " ".join(args)
    try:
        to_translate_text = msg.reply_to_message.text
    except:
        return
    translator = Translator()
    try:
        translated = translator.translate(to_translate_text, dest=lan)
        src_lang = translated.src
        translated_text = translated.text
        msg.reply_text("Translated from {} to {}.\n {}".format(src_lang, lan, translated_text))
    except :
        msg.reply_text("Error")


__help__ = """- /tr (language code) as reply to a long message.
"""
__mod_name__ = "Translator"

dispatcher.add_handler(DisableAbleCommandHandler("tr", do_translate, pass_args=True))
