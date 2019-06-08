import re, ast
from io import BytesIO
from typing import Optional, List

from telegram import MAX_MESSAGE_LENGTH, ParseMode, InlineKeyboardMarkup
from telegram import Message, Update, Bot
from telegram.error import BadRequest
from telegram.ext import CommandHandler, RegexHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown

import haruka.modules.sql.notes_sql as sql
from haruka import dispatcher, MESSAGE_DUMP, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import user_admin
from haruka.modules.helper_funcs.misc import build_keyboard, revert_buttons
from haruka.modules.helper_funcs.msg_types import get_note_type

from haruka.modules.connection import connected

FILE_MATCHER = re.compile(r"^###file_id(!photo)?###:(.*?)(?:\s|$)")
STICKER_MATCHER = re.compile(r"^###sticker(!photo)?###:")
BUTTON_MATCHER = re.compile(r"^###button(!photo)?###:(.*?)(?:\s|$)")
MYFILE_MATCHER = re.compile(r"^###file(!photo)?###:")
MYPHOTO_MATCHER = re.compile(r"^###photo(!photo)?###:")
MYAUDIO_MATCHER = re.compile(r"^###audio(!photo)?###:")
MYVOICE_MATCHER = re.compile(r"^###voice(!photo)?###:")
MYVIDEO_MATCHER = re.compile(r"^###video(!photo)?###:")
MYVIDEONOTE_MATCHER = re.compile(r"^###video_note(!photo)?###:")

ENUM_FUNC_MAP = {
	sql.Types.TEXT.value: dispatcher.bot.send_message,
	sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
	sql.Types.STICKER.value: dispatcher.bot.send_sticker,
	sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
	sql.Types.PHOTO.value: dispatcher.bot.send_photo,
	sql.Types.AUDIO.value: dispatcher.bot.send_audio,
	sql.Types.VOICE.value: dispatcher.bot.send_voice,
	sql.Types.VIDEO.value: dispatcher.bot.send_video,
	sql.Types.VIDEO_NOTE.value: dispatcher.bot.send_video_note
}


# Do not async
def get(bot, update, notename, show_none=True, no_format=False):
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	conn = connected(bot, update, chat, user.id, need_admin=False)
	if conn:
		chat_id = conn
		send_id = user.id
	else:
		chat_id = update.effective_chat.id
		send_id = chat_id

	note = sql.get_note(chat_id, notename)
	message = update.effective_message  # type: Optional[Message]

	if note:
		# If we're replying to a message, reply to that message (unless it's an error)
		if message.reply_to_message:
			reply_id = message.reply_to_message.message_id
		else:
			reply_id = message.message_id

		if note.is_reply:
			if MESSAGE_DUMP:
				try:
					bot.forward_message(chat_id=chat_id, from_chat_id=MESSAGE_DUMP, message_id=note.value)
				except BadRequest as excp:
					if excp.message == "Message to forward not found":
                                                message.reply_text("This message seems to have been lost - I'll remove it "
                                                                                   "from your notes list.")
                                                sql.rm_note(chat_id, notename)
					else:
						raise
			else:
				try:
					bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=note.value)

				except BadRequest as excp:
					if excp.message == "Message to forward not found":
						message.reply_text("Looks like the original sender of this note has deleted "
										   "their message - sorry! Get your bot admin to start using a "
										   "message dump to avoid this. I'll remove this note from "
										   "your saved notes.")
					sql.rm_note(chat_id, notename)

				else:
					raise
		else:
			text = note.value
			keyb = []
			parseMode = ParseMode.MARKDOWN
			buttons = sql.get_buttons(chat_id, notename)
			if no_format:
				parseMode = None
				text += revert_buttons(buttons)
			else:
				keyb = build_keyboard(buttons)

			keyboard = InlineKeyboardMarkup(keyb)

			try:
				if note.msgtype in (sql.Types.BUTTON_TEXT, sql.Types.TEXT):
					try:
						bot.send_message(send_id, text, reply_to_message_id=reply_id,
										 parse_mode=parseMode, disable_web_page_preview=True,
										 reply_markup=keyboard)
					except BadRequest as excp:
						if excp.message == "Wrong http url":
							failtext = "The URL on the button is invalid! Please update this note!"
							failtext += "\n\n```\n{}```".format(note.value + revert_buttons(buttons))
							message.reply_text(failtext, parse_mode="markdown")
						print("Gagal mengirim catatan: " + excp.message)
						pass
				else:
					ENUM_FUNC_MAP[note.msgtype](send_id, note.file, caption=text, reply_to_message_id=reply_id,
												parse_mode=parseMode, disable_web_page_preview=True,
												reply_markup=keyboard)

			except BadRequest as excp:
				if excp.message == "Entity_mention_user_invalid":
					message.reply_text("Looks like you tried to mention someone I've never seen before. If you really "
									   "want to mention them, forward one of their messages to me, and I'll be able "
									   "to tag them!")

				elif FILE_MATCHER.match(note.value):
					message.reply_text("This note was an incorrectly imported file from another bot - I can't use "
									   "it. If you really need it, you'll have to save it again. In "
									   "the meantime, I'll remove it from your notes list.")
					sql.rm_note(chat_id, notename)
				else:
					message.reply_text("This note could not be sent, as it is incorrectly formatted, Please ask in @HarukaAyaGroup if you can't figure out why!")
					LOGGER.exception("Could not parse message #%s in chat %s", notename, str(chat_id))
					LOGGER.warning("Message was: %s", str(note.value))

		return
	elif show_none:
		message.reply_text("This note doesn't exist")


@run_async
def cmd_get(bot: Bot, update: Update, args: List[str]):
	if len(args) >= 2 and args[1].lower() == "noformat":
		get(bot, update, args[0], show_none=True, no_format=True)
	elif len(args) >= 1:
		get(bot, update, args[0], show_none=True)
	else:
		update.effective_message.reply_text("Get rekt")


@run_async
def hash_get(bot: Bot, update: Update):
	message = update.effective_message.text
	fst_word = message.split()[0]
	no_hash = fst_word[1:]
	get(bot, update, no_hash, show_none=False)


# TODO: FIX THIS
@run_async
@user_admin
def save(bot: Bot, update: Update):
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	conn = connected(bot, update, chat, user.id)
	if conn:
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		chat_id = update.effective_chat.id
		if chat.type == "private":
			chat_name = "local notes"
		else:
			chat_name = chat.title

	msg = update.effective_message  # type: Optional[Message]

	note_name, text, data_type, content, buttons = get_note_type(msg)

	if data_type is None:
		msg.reply_text("Dude, there's no note!")
		return

	if len(text.strip()) == 0:
		text = note_name

	if not sql.get_note(chat_id, note_name):
		sql.add_note_to_db(chat_id, note_name, text, data_type, buttons=buttons, file=content)
		msg.reply_text("Ok, added `{note_name}` note in *{chat_name}*.\nGet it with `/get {note_name}`, or `#{note_name}`".format(note_name=note_name, chat_name=chat_name), parse_mode=ParseMode.MARKDOWN)
	else:
		sql.add_note_to_db(chat_id, note_name, text, data_type, buttons=buttons, file=content)
		msg.reply_text("Ok, Note `{note_name}` in *{chat_name}* have been updated!.\nGet it with `/get {note_name}`, or `#{note_name}`".format(note_name=note_name, chat_name=chat_name), parse_mode=ParseMode.MARKDOWN)


@run_async
@user_admin
def clear(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
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

    if len(args) >= 1:
        notename = args[0]

        if sql.rm_note(chat_id, notename):
            update.effective_message.reply_text("Note succesfully removed from *{}*.".format(chat_name), parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text("That's not a note in my database!")


@run_async
def list_notes(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    conn = connected(bot, update, chat, user.id, need_admin=False)
    if not conn == False:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
        msg = "*Notes in {}:*\n"
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = ""
            msg = "*Local Notes:*\n"
        else:
            chat_name = chat.title
            msg = "*Notes in {}:*\n"

    note_list = sql.get_all_chat_notes(chat_id)

    for note in note_list:
        note_name = " • `#{}`\n".format(note.name)
        if len(msg) + len(note_name) > MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
            msg = ""
        msg += note_name

    if not note_list:
        update.effective_message.reply_text("No notes in *{}*!".format(chat_name), parse_mode=ParseMode.MARKDOWN)

    elif len(msg) != 0:
        msg += "\nYou can retrieve these notes by using `/get notename`, or `#notename`"
        update.effective_message.reply_text(msg.format(chat_name), parse_mode=ParseMode.MARKDOWN)


def __import_data__(chat_id, data):
	failures = []
	for notename, notedata in data.get('extra', {}).items():
		match = FILE_MATCHER.match(notedata)
		matchsticker = STICKER_MATCHER.match(notedata)
		matchbtn = BUTTON_MATCHER.match(notedata)
		matchfile = MYFILE_MATCHER.match(notedata)
		matchphoto = MYPHOTO_MATCHER.match(notedata)
		matchaudio = MYAUDIO_MATCHER.match(notedata)
		matchvoice = MYVOICE_MATCHER.match(notedata)
		matchvideo = MYVIDEO_MATCHER.match(notedata)
		matchvn = MYVIDEONOTE_MATCHER.match(notedata)

		if match:
			failures.append(notename)
			notedata = notedata[match.end():].strip()
			if notedata:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.TEXT)
		elif matchsticker:
			content = notedata[matchsticker.end():].strip()
			if content:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.STICKER, file=content)
		elif matchbtn:
			parse = notedata[matchbtn.end():].strip()
			notedata = parse.split("<###button###>")[0]
			buttons = parse.split("<###button###>")[1]
			buttons = ast.literal_eval(buttons)
			if buttons:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.BUTTON_TEXT, buttons=buttons)
		elif matchfile:
			file = notedata[matchfile.end():].strip()
			file = file.split("<###TYPESPLIT###>")
			notedata = file[1]
			content = file[0]
			if content:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.DOCUMENT, file=content)
		elif matchphoto:
			photo = notedata[matchphoto.end():].strip()
			photo = photo.split("<###TYPESPLIT###>")
			notedata = photo[1]
			content = photo[0]
			if content:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.PHOTO, file=content)
		elif matchaudio:
			audio = notedata[matchaudio.end():].strip()
			audio = audio.split("<###TYPESPLIT###>")
			notedata = audio[1]
			content = audio[0]
			if content:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.AUDIO, file=content)
		elif matchvoice:
			voice = notedata[matchvoice.end():].strip()
			voice = voice.split("<###TYPESPLIT###>")
			notedata = voice[1]
			content = voice[0]
			if content:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.VOICE, file=content)
		elif matchvideo:
			video = notedata[matchvideo.end():].strip()
			video = video.split("<###TYPESPLIT###>")
			notedata = video[1]
			content = video[0]
			if content:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.VIDEO, file=content)
		elif matchvn:
			video_note = notedata[matchvn.end():].strip()
			video_note = video_note.split("<###TYPESPLIT###>")
			notedata = video_note[1]
			content = video_note[0]
			if content:
				sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.VIDEO_NOTE, file=content)
		else:
			sql.add_note_to_db(chat_id, notename[1:], notedata, sql.Types.TEXT)

	if failures:
		with BytesIO(str.encode("\n".join(failures))) as output:
			output.name = "failed_imports.txt"
			dispatcher.bot.send_document(chat_id, document=output, filename="failed_imports.txt",
										 caption="These files/photos failed to import due to originating "
												 "from another bot. This is a telegram API restriction, and can't "
												 "be avoided. Sorry for the inconvenience!")


def __stats__():
	return "{} notes, accross {} chats.".format(sql.num_notes(), sql.num_chats())


def __migrate__(old_chat_id, new_chat_id):
	sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
	notes = sql.get_all_chat_notes(chat_id)
	return "Ada catatan `{}` dalam obrolan ini.".format(len(notes))


__help__ = """
Save data for future users with notes!
Notes are great to save random tidbits of information; a phone number, a nice gif, a funny picture - anything!
Available commands are:
 - /save <word> <sentence>: Save that sentence to the note called "word". Replying to a message will save that message. Even works on media!
 - /get <word>: get the note registered to that word.
 - #<word>: same as /get word
 - /clear <word>: delete the note called "word"
 - /notes: List all notes in the current chat
 - /saved: same as /notes
An example of how to save a note would be via:
/save data This is some data!
Now, anyone using "/get data", or "#data" will be replied to with "This is some data!".
If you want to save an image, gif, or sticker, or any other data, do the following:
/save word while replying to a sticker or whatever data you'd like. Now, the note at "#word" contains a sticker which will be sent as a reply.
Tip: to retrieve a note without the formatting, use /get <notename> noformat
This will retrieve the note and send it without formatting it; getting you the raw markdown, allowing you to make easy edits
"""

__mod_name__ = "Notes"

GET_HANDLER = CommandHandler("get", cmd_get, pass_args=True)
HASH_GET_HANDLER = RegexHandler(r"^#[^\s]+", hash_get)

SAVE_HANDLER = CommandHandler("save", save)
DELETE_HANDLER = CommandHandler("clear", clear, pass_args=True)

LIST_HANDLER = DisableAbleCommandHandler(["notes", "saved"], list_notes, admin_ok=True)

dispatcher.add_handler(GET_HANDLER)
dispatcher.add_handler(SAVE_HANDLER)
dispatcher.add_handler(LIST_HANDLER)
dispatcher.add_handler(DELETE_HANDLER)
dispatcher.add_handler(HASH_GET_HANDLER)
