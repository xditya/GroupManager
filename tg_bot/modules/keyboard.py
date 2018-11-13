from math import ceil
from typing import List, Dict

from telegram import MAX_MESSAGE_LENGTH, InlineKeyboardButton, Bot, ParseMode
from telegram.error import TelegramError

from tg_bot import LOAD, NO_LOAD
from tg_bot.modules.translations.strings import tld
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler

@user_admin
def keyboard(bot, update):
    

KEYBOARD_HANDLER = CommandHandler(["keyboard"], keyboard, pass_args=True)
dispatcher.add_handler(KEYBOARD_HANDLER)