from typing import Optional, List

from telegram import ParseMode
from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html

import tg_bot.modules.sql.connection_sql as sql
from tg_bot import dispatcher, LOGGER
from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_admin, is_user_admin, can_restrict
from tg_bot.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from tg_bot.modules.helper_funcs.string_handling import extract_time
#from tg_bot.modules.log_channel import loggable

@user_admin
@run_async
def allow_connections(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    if chat.type != chat.PRIVATE:
        if len(args) >= 1:
            var = args[0]
            print(var)
            if (var == "no"):
                sql.set_allow_connect_to_chat(chat.id, False)
                update.effective_message.reply_text("Disabled connections to this chat for users")
            elif(var == "yes"):
                sql.set_allow_connect_to_chat(chat.id, True)
                update.effective_message.reply_text("Enabled connections to this chat for users")
            else:
                update.effective_message.reply_text("Please enter yes or no!", parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text("Please enter yes or no!", parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Please enter yes or no in your group!", parse_mode=ParseMode.MARKDOWN)


@run_async
def connect_chat(bot, update, args):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    if update.effective_chat.type == 'private':
        if len(args) >= 1:
            try:
                connect_chat = int(args[0])
            except ValueError:
                update.effective_message.reply_text("Invalid Chat ID provided!")
            #if bot.get_chat_member(connect_chat, update.effective_message.from_user.id).status in ('administrator', 'creator', 'member'):
            if bot.get_chat_member(connect_chat, update.effective_message.from_user.id).status in ('administrator', 'creator'):
                #if sql.allow_connect_to_chat(chat.id) == True:
                connection_status = sql.connect(update.effective_message.from_user.id, connect_chat)
                if connection_status:
                    chat_name = dispatcher.bot.getChat(connected(chat, user.id)).title
                    update.effective_message.reply_text("Successfully connected to *{}*".format(chat_name), parse_mode=ParseMode.MARKDOWN)
                else:
                    update.effective_message.reply_text("Connection failed!")
                #else:
                    #update.effective_message.reply_text("Connections to this chat not allowed!")
            else:
                update.effective_message.reply_text("You are not a participant of the given chat, Go away!")
        else:
            update.effective_message.reply_text("Gimme a chat to connect to!")

    else:
        update.effective_message.reply_text("Usage limited to PMs only!")


def disconnect_chat(bot, update):
    if update.effective_chat.type == 'private':
        disconnection_status = sql.disconnect(update.effective_message.from_user.id)
        if disconnection_status:
           sql.disconnected_chat = update.effective_message.reply_text("Disconnected from chat!")
        else:
           update.effective_message.reply_text("Disconnection unsuccessfull!")
    else:
        update.effective_message.reply_text("Usage restricted to PMs only")


def connected(bot, update, chat, user_id, need_admin=True):
    if sql.get_connected_chat(user_id) and chat.type == chat.PRIVATE:
        conn_id = sql.get_connected_chat(user_id).chat_id
        if need_admin == True:
            if bot.get_chat_member(conn_id, update.effective_message.from_user.id).status in ('administrator', 'creator'): #or user_id in SUDO_USERS:
                return conn_id
            else:
                update.effective_message.reply_text("You need be a admin in connected group!")
                exit(1)
        else:
            return conn_id
    else:
        return False



__help__ = """
You can connect to remote chat for see and edit notes
Connections:
 - /connection <chatid>: Connect to remote chat for see and edit notes
 - /disconnect: Disconnect from chat
"""

__mod_name__ = "Connections"

CONNECT_CHAT_HANDLER = CommandHandler("connect", connect_chat, allow_edited=True, pass_args=True)
DISCONNECT_CHAT_HANDLER = CommandHandler("disconnect", disconnect_chat, allow_edited=True)
ALLOW_CONNECTIONS_HANDLER = CommandHandler("allowconnect", allow_connections, allow_edited=True, pass_args=True)

dispatcher.add_handler(CONNECT_CHAT_HANDLER)
dispatcher.add_handler(DISCONNECT_CHAT_HANDLER)
dispatcher.add_handler(ALLOW_CONNECTIONS_HANDLER)