import json, time, os
from io import BytesIO
from typing import Optional

from telegram import MAX_MESSAGE_LENGTH, ParseMode, InlineKeyboardMarkup
from telegram import Message, Chat, Update, Bot
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async, Filters

import haruka.modules.sql.notes_sql as sql
from haruka import dispatcher, LOGGER, OWNER_ID, SUDO_USERS, MESSAGE_DUMP
from haruka.__main__ import DATA_IMPORT
from haruka.modules.helper_funcs.chat_status import user_admin
from haruka.modules.helper_funcs.misc import build_keyboard, revert_buttons
from haruka.modules.helper_funcs.msg_types import get_note_type
from haruka.modules.rules import get_rules
import haruka.modules.sql.rules_sql as rulessql
from haruka.modules.sql import warns_sql as warnssql
import haruka.modules.sql.blacklist_sql as blacklistsql
from haruka.modules.sql import disable_sql as disabledsql
from haruka.modules.sql import cust_filters_sql as filtersql
import haruka.modules.sql.welcome_sql as welcsql
import haruka.modules.sql.locks_sql as locksql
from haruka.modules.connection import connected

@run_async
@user_admin
def import_data(bot: Bot, update):
	msg = update.effective_message  # type: Optional[Message]
	chat = update.effective_chat  # type: Optional[Chat]
	user = update.effective_user  # type: Optional[User]
	# TODO: allow uploading doc with command, not just as reply
	# only work with a doc

	conn = connected(bot, update, chat, user.id, need_admin=True)
	if conn:
		chat = dispatcher.bot.getChat(conn)
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		if update.effective_message.chat.type == "private":
			update.effective_message.reply_text("This command can only be runned on group, not PM.")
			return ""

		chat = update.effective_chat
		chat_id = update.effective_chat.id
		chat_name = update.effective_message.chat.title

	if msg.reply_to_message and msg.reply_to_message.document:
		try:
			file_info = bot.get_file(msg.reply_to_message.document.file_id)
		except BadRequest:
			msg.reply_text("Try downloading and uploading the file yourself again, This one seem broken!")
			return

		with BytesIO() as file:
			file_info.download(out=file)
			file.seek(0)
			data = json.load(file)

		# only import one group
		if len(data) > 1 and str(chat.id) not in data:
			msg.reply_text("There are more than one group in this file and the chat.id is not same! How am i supposed to import it?")
			return

		# Check if backup is this chat
		try:
			if data.get(str(chat.id)) == None:
				if conn:
					text = "Backup comes from another chat, I can't return another chat to chat *{}*".format(chat_name)
				else:
					text = "Backup comes from another chat, I can't return another chat to this chat"
				return msg.reply_text(text, parse_mode="markdown")
		except:
			return msg.reply_text("There is problem while importing the data! Please ask in @HarukaAyaGroup about why this happened.")
		# Check if backup is from self
		try:
			if str(bot.id) != str(data[str(chat.id)]['bot']):
				return msg.reply_text("Backup from another bot that is not suggested might cause the problem, documents, photos, videos, audios, records might not work as it should be. However, You can still request a feature regarding this in @HarukaAyaGroup !")
		except:
			pass
		# Select data source
		if str(chat.id) in data:
			data = data[str(chat.id)]['hashes']
		else:
			data = data[list(data.keys())[0]]['hashes']

		try:
			for mod in DATA_IMPORT:
				mod.__import_data__(str(chat.id), data)
		except Exception:
			msg.reply_text("An error occurred while recovering your data. The process failed. If you experience a problem with this, please ask in @HarukaAyaGroup . My owner and community will be happy to help. Also, bugs report makes me even better!\nThank you!")

			LOGGER.exception("Imprt for the chat %s with the name %s failed.", str(chat.id), str(chat.title))
			return

		# TODO: some of that link logic
		# NOTE: consider default permissions stuff?
		if conn:


			text = "Backup fully restored on *{}*.".format(chat_name)
		else:
			text = "Backup fully restored"
		msg.reply_text(text, parse_mode="markdown")


@run_async
@user_admin
def export_data(bot: Bot, update: Update, chat_data):
	msg = update.effective_message  # type: Optional[Message]
	user = update.effective_user  # type: Optional[User]

	chat_id = update.effective_chat.id
	chat = update.effective_chat
	current_chat_id = update.effective_chat.id

	conn = connected(bot, update, chat, user.id, need_admin=True)
	if conn:
		chat = dispatcher.bot.getChat(conn)
		chat_id = conn
		chat_name = dispatcher.bot.getChat(conn).title
	else:
		if update.effective_message.chat.type == "private":
			update.effective_message.reply_text("This command can only be used on group, not PM")
			return ""
		chat = update.effective_chat
		chat_id = update.effective_chat.id
		chat_name = update.effective_message.chat.title

	jam = time.time()
	new_jam = jam + 10800
	checkchat = get_chat(chat_id, chat_data)
	if checkchat.get('status'):
		if jam <= int(checkchat.get('value')):
			timeformatt = time.strftime("%H:%M:%S %d/%m/%Y", time.localtime(checkchat.get('value')))
			update.effective_message.reply_text("You can only backup once a day!\nYou can backup again in about `{}`".format(timeformatt), parse_mode=ParseMode.MARKDOWN)
			return
		else:
			if user.id != 654839744:
				put_chat(chat_id, new_jam, chat_data)
	else:
		if user.id != 654839744:
			put_chat(chat_id, new_jam, chat_data)

	note_list = sql.get_all_chat_notes(chat_id)
	backup = {}
	notes = {}
	button = ""
	buttonlist = []
	namacat = ""
	isicat = ""
	rules = ""
	count = 0
	countbtn = 0
	# Notes
	for note in note_list:
		count += 1
		getnote = sql.get_note(chat_id, note.name)
		namacat += '{}<###splitter###>'.format(note.name)
		if note.msgtype == 1:
			tombol = sql.get_buttons(chat_id, note.name)
			keyb = []
			for btn in tombol:
				countbtn += 1
				if btn.same_line:
					buttonlist.append(('{}'.format(btn.name), '{}'.format(btn.url), True))
				else:
					buttonlist.append(('{}'.format(btn.name), '{}'.format(btn.url), False))
			isicat += '###button###: {}<###button###>{}<###splitter###>'.format(note.value,str(buttonlist))
			buttonlist.clear()
		elif note.msgtype == 2:
			isicat += '###sticker###:{}<###splitter###>'.format(note.file)
		elif note.msgtype == 3:
			isicat += '###file###:{}<###TYPESPLIT###>{}<###splitter###>'.format(note.file, note.value)
		elif note.msgtype == 4:
			isicat += '###photo###:{}<###TYPESPLIT###>{}<###splitter###>'.format(note.file, note.value)
		elif note.msgtype == 5:
			isicat += '###audio###:{}<###TYPESPLIT###>{}<###splitter###>'.format(note.file, note.value)
		elif note.msgtype == 6:
			isicat += '###voice###:{}<###TYPESPLIT###>{}<###splitter###>'.format(note.file, note.value)
		elif note.msgtype == 7:
			isicat += '###video###:{}<###TYPESPLIT###>{}<###splitter###>'.format(note.file, note.value)
		elif note.msgtype == 8:
			isicat += '###video_note###:{}<###TYPESPLIT###>{}<###splitter###>'.format(note.file, note.value)
		else:
			isicat += '{}<###splitter###>'.format(note.value)
	for x in range(count):
		notes['#{}'.format(namacat.split("<###splitter###>")[x])] = '{}'.format(isicat.split("<###splitter###>")[x])
	# Rules
	rules = rulessql.get_rules(chat_id)
	# Blacklist
	bl = list(blacklistsql.get_chat_blacklist(chat_id))
	# Disabled command
	disabledcmd = list(disabledsql.get_all_disabled(chat_id))
	# Filters (TODO)
	"""
	all_filters = list(filtersql.get_chat_triggers(chat_id))
	export_filters = {}
	for filters in all_filters:
		filt = filtersql.get_filter(chat_id, filters)
		# print(vars(filt))
		if filt.is_sticker:
			tipefilt = "sticker"
		elif filt.is_document:
			tipefilt = "doc"
		elif filt.is_image:
			tipefilt = "img"
		elif filt.is_audio:
			tipefilt = "audio"
		elif filt.is_voice:
			tipefilt = "voice"
		elif filt.is_video:
			tipefilt = "video"
		elif filt.has_buttons:
			tipefilt = "button"
			buttons = filtersql.get_buttons(chat.id, filt.keyword)
			print(vars(buttons))
		elif filt.has_markdown:
			tipefilt = "text"
		if tipefilt == "button":
			content = "{}#=#{}|btn|{}".format(tipefilt, filt.reply, buttons)
		else:
			content = "{}#=#{}".format(tipefilt, filt.reply)
		print(content)
		export_filters[filters] = content
	print(export_filters)
	"""
	# Welcome (TODO)
	# welc = welcsql.get_welc_pref(chat_id)
	# Locked
	locks = locksql.get_locks(chat_id)
	locked = []
	if locks:
		if locks.sticker:
			locked.append('sticker')
		if locks.document:
			locked.append('document')
		if locks.contact:
			locked.append('contact')
		if locks.audio:
			locked.append('audio')
		if locks.game:
			locked.append('game')
		if locks.bots:
			locked.append('bots')
		if locks.gif:
			locked.append('gif')
		if locks.photo:
			locked.append('photo')
		if locks.video:
			locked.append('video')
		if locks.voice:
			locked.append('voice')
		if locks.location:
			locked.append('location')
		if locks.forward:
			locked.append('forward')
		if locks.url:
			locked.append('url')
		restr = locksql.get_restr(chat_id)
		if restr.other:
			locked.append('other')
		if restr.messages:
			locked.append('messages')
		if restr.preview:
			locked.append('preview')
		if restr.media:
			locked.append('media')
	# Warns (TODO)
	# warns = warnssql.get_warns(chat_id)
	# Backing up
	backup[chat_id] = {'bot': bot.id, 'hashes': {'info': {'rules': rules}, 'extra': notes, 'blacklist': bl, 'disabled': disabledcmd, 'locks': locked}}
	baccinfo = json.dumps(backup, indent=4)
	f=open("harukab{}.backup".format(chat_id), "w")
	f.write(str(baccinfo))
	f.close()
	bot.sendChatAction(current_chat_id, "upload_document")
	tgl = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime(time.time()))
	try:
		bot.sendMessage(MESSAGE_DUMP, "*Successfully imported backup:*\nChat: `{}`\nChat ID: `{}`\nOn: `{}`".format(chat.title, chat_id, tgl), parse_mode=ParseMode.MARKDOWN)
	except BadRequest:
		pass
	bot.sendDocument(current_chat_id, document=open('harukab{}.backup'.format(chat_id), 'rb'), caption="*Successfully imported backup:*\nChat: `{}`\nChat ID: `{}`\nOn: `{}`\n\nNote: This `harukab` is specially made for notes.".format(chat.title, chat_id, tgl), timeout=360, reply_to_message_id=msg.message_id, parse_mode=ParseMode.MARKDOWN)
	os.remove("harukab{}.backup".format(chat_id)) # Cleaning file


# Temporary data
def put_chat(chat_id, value, chat_data):
	# print(chat_data)
	if value == False:
		status = False
	else:
		status = True
	chat_data[chat_id] = {'backups': {"status": status, "value": value}}

def get_chat(chat_id, chat_data):
	# print(chat_data)
	try:
		value = chat_data[chat_id]['backups']
		return value
	except KeyError:
		return {"status": False, "value": False}


__mod_name__ = "Backups"

__help__ = """
*Only for chat administrator:*

 - /import: reply to the backup file for the butler / emilia group to import as much as possible, making transfers very easy! \
 Note that files / photos cannot be imported due to telegram restrictions.

 - /export: export group data, which will be exported are: rules, notes (documents, images, music, video, audio, voice, text, text buttons) \

This module is still in beta! Report bugs in @HarukaAyaGroup !
"""

IMPORT_HANDLER = CommandHandler("import", import_data)
EXPORT_HANDLER = CommandHandler("export", export_data, pass_chat_data=True)

dispatcher.add_handler(IMPORT_HANDLER)
dispatcher.add_handler(EXPORT_HANDLER)
