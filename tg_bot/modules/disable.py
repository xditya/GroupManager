from typing import Union, List, Optional

from future.utils import string_types
from telegram import ParseMode, Update, Bot, Chat, User
from telegram.ext import CommandHandler, RegexHandler, Filters
from telegram.utils.helpers import escape_markdown

from tg_bot import dispatcher
from tg_bot.modules.helper_funcs.handlers import CMD_STARTERS
from tg_bot.modules.helper_funcs.misc import is_module_loaded

from tg_bot.modules.translations.strings import tld

from tg_bot.modules.connection import connected

FILENAME = __name__.rsplit(".", 1)[-1]

# If module is due to be loaded, then setup all the magical handlers
if is_module_loaded(FILENAME):
    from tg_bot.modules.helper_funcs.chat_status import user_admin, is_user_admin
    from telegram.ext.dispatcher import run_async

    from tg_bot.modules.sql import disable_sql as sql

    DISABLE_CMDS = []
    DISABLE_OTHER = []
    ADMIN_CMDS = []

    class DisableAbleCommandHandler(CommandHandler):
        def __init__(self, command, callback, admin_ok=False, **kwargs):
            super().__init__(command, callback, **kwargs)
            self.admin_ok = admin_ok
            if isinstance(command, string_types):
                DISABLE_CMDS.append(command)
                if admin_ok:
                    ADMIN_CMDS.append(command)
            else:
                DISABLE_CMDS.extend(command)
                if admin_ok:
                    ADMIN_CMDS.extend(command)

        def check_update(self, update):
            chat = update.effective_chat  # type: Optional[Chat]
            user = update.effective_user  # type: Optional[User]
            if super().check_update(update):
                # Should be safe since check_update passed.
                command = update.effective_message.text_html.split(None, 1)[0][1:].split('@')[0]

                # disabled, admincmd, user admin
                if sql.is_command_disabled(chat.id, command):
                    return command in ADMIN_CMDS and is_user_admin(chat, user.id)

                # not disabled
                else:
                    return True

            return False


    class DisableAbleRegexHandler(RegexHandler):
        def __init__(self, pattern, callback, friendly="", **kwargs):
            super().__init__(pattern, callback, **kwargs)
            DISABLE_OTHER.append(friendly or pattern)
            self.friendly = friendly or pattern

        def check_update(self, update):
            chat = update.effective_chat
            return super().check_update(update) and not sql.is_command_disabled(chat.id, self.friendly)


    @run_async
    @user_admin
    def disable(bot: Bot, update: Update, args: List[str]):
        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
    
        conn = connected(bot, update, chat, user.id)
        if not conn == False:
            chatD = dispatcher.bot.getChat(conn)
        else:
            if chat.type == "private":
                exit(1)
            else:
                chatD = update.effective_chat


        if len(args) >= 1:
            disable_cmd = args[0]
            if disable_cmd.startswith(CMD_STARTERS):
                disable_cmd = disable_cmd[1:]

            if disable_cmd in set(DISABLE_CMDS + DISABLE_OTHER):
                sql.disable_command(chatD.id, disable_cmd)
                update.effective_message.reply_text(tld(chat.id, "Disabled the use of `{}` in *{}*").format(disable_cmd, chatD.title),
                                                    parse_mode=ParseMode.MARKDOWN)
            else:
                update.effective_message.reply_text(tld(chat.id, "That command can't be disabled"))

        else:
            update.effective_message.reply_text(tld(chat.id, "What should I disable?"))


    @run_async
    @user_admin
    def enable(bot: Bot, update: Update, args: List[str]):
        chat = update.effective_chat  # type: Optional[Chat]
        user = update.effective_user  # type: Optional[User]
    
        conn = connected(bot, update, chat, user.id)
        if not conn == False:
            chatD = dispatcher.bot.getChat(conn)
        else:
            if chat.type == "private":
                exit(1)
            else:
                chatD = update.effective_chat


        if len(args) >= 1:
            enable_cmd = args[0]
            if enable_cmd.startswith(CMD_STARTERS):
                enable_cmd = enable_cmd[1:]

            if sql.enable_command(chatD.id, enable_cmd):
                update.effective_message.reply_text(tld(chat.id, "Enabled the use of `{}` in *{}*").format(enable_cmd, chatD.title),
                                                    parse_mode=ParseMode.MARKDOWN)
            else:
                update.effective_message.reply_text(tld(chat.id, "Is that even disabled?"))

        else:
            update.effective_message.reply_text(tld(chat.id, "What should I enable?"))


    @run_async
    @user_admin
    def list_cmds(bot: Bot, update: Update):
        chat = update.effective_chat  # type: Optional[Chat]
        if DISABLE_CMDS + DISABLE_OTHER:
            result = ""
            for cmd in set(DISABLE_CMDS + DISABLE_OTHER):
                result += " • `{}`\n".format(escape_markdown(cmd))
            update.effective_message.reply_text(tld(chat.id, "The following commands are toggleable:\n{}").format(result),
                                                parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text(tld(chat.id, "No commands can be disabled."))


    # do not async
    def build_curr_disabled(chatD_id, chat_id):

        disabled = sql.get_all_disabled(chatD_id)

        result = ""
        for cmd in disabled:
            result += " • `{}`\n".format(escape_markdown(cmd))

        if result == "":
            return tld(chat_id, "No commands are disabled!")
        else:
            return result


    @run_async
    def commands(bot: Bot, update: Update):
        chat = update.effective_chat
        user = update.effective_user  # type: Optional[User]
    
        conn = connected(bot, update, chat, user.id, need_admin=False)
        if not conn == False:
            chatD = dispatcher.bot.getChat(conn)
        else:
            if chat.type == "private":
                exit(1)
            else:
                chatD = update.effective_chat

        disabled = sql.get_all_disabled(chatD.id)
        if not disabled:
            update.effective_message.reply_text(tld(chat.id, "No commands are disabled! in *{}*!").format(chatD.title))

        text = build_curr_disabled(chatD.id, chat.id)

        update.effective_message.reply_text(tld(chat.id, "The following commands are currently restricted in *{}*:\n{}").format(chatD.title, text), parse_mode=ParseMode.MARKDOWN)


    def __stats__():
        return "{} disabled items, across {} chats.".format(sql.num_disabled(), sql.num_chats())


    def __migrate__(old_chat_id, new_chat_id):
        sql.migrate_chat(old_chat_id, new_chat_id)


    def __chat_settings__(bot, update, chat, chatP, user):
        return build_curr_disabled(chat.id, chat.id)


    __mod_name__ = "Command disabling"

    __help__ = """
Not everyone wants every feature that rose offers. Some commands are best left unused; to avoid spam and abuse.

This allows you to disable some commonly used commands, so noone can use them. It'll also allow you to autodelete them, stopping people from

Available commands are:
 - /disable <commandname>: stop users from using the "commandname" command in this group.
 - /enable <commandname>: allow users to use the "commandname" command in this group again.
 - /listcmds: list all disableable commands.
 - /disabled: list the disabled commands in this chat.

Note:
When disabling a command, the command only gets disabled for non-admins. All admins can still use those commands.
Disabled commands are still accessible through the /connect feature. If you would be interested to see this disabled too, let me know in the support chat.
    """

    DISABLE_HANDLER = CommandHandler("disable", disable, pass_args=True)
    ENABLE_HANDLER = CommandHandler("enable", enable, pass_args=True)
    COMMANDS_HANDLER = CommandHandler(["cmds", "disabled"], commands)
    TOGGLE_HANDLER = CommandHandler("listcmds", list_cmds)

    dispatcher.add_handler(DISABLE_HANDLER)
    dispatcher.add_handler(ENABLE_HANDLER)
    dispatcher.add_handler(COMMANDS_HANDLER)
    dispatcher.add_handler(TOGGLE_HANDLER)

else:
    DisableAbleCommandHandler = CommandHandler
    DisableAbleRegexHandler = RegexHandler
