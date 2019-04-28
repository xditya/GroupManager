import os
import math
import requests
import urllib.request as urllib
from urllib.error import URLError, HTTPError

from PIL import Image

from typing import Optional, List
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError
from telegram import Update, Bot
from telegram.ext import CommandHandler, run_async
from telegram.utils.helpers import escape_markdown

from haruka import dispatcher

from haruka.modules.disable import DisableAbleCommandHandler

@run_async
def stickerid(bot: Bot, update: Update):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text("Sticker ID:\n```" +
                                            escape_markdown(msg.reply_to_message.sticker.file_id) + "```",
                                            parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text("Please reply to a sticker to get its ID.")


@run_async
def getsticker(bot: Bot, update: Update):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        newFile = bot.get_file(file_id)
        newFile.download('sticker.png')
        bot.send_document(chat_id, document=open('sticker.png', 'rb'))
        os.remove("sticker.png")
    else:
        update.effective_message.reply_text("Please reply to a sticker for me to upload its PNG.")


@run_async
def kang(bot: Bot, update: Update, args: List[str]):
    if os.path.isfile("kangsticker.png"):
        os.remove("kangsticker.png")

    msg = update.effective_message
    user = update.effective_user
    packname = f"c{user.id}_by_{bot.username}"
    kangsticker = "kangsticker.png"

    reply = msg.reply_to_message
    if reply:
        if reply.sticker:
            file_id = reply.sticker.file_id
        elif reply.photo:
            file_id = reply.photo[-1].file_id
        elif reply.document:
            file_id = reply.document.file_id
        else:
            msg.reply_text("Reply to an image or sticker to kang.")
            return
        kang_file = bot.get_file(file_id)
        kang_file.download(kangsticker)
        if args:
            sticker_emoji = str(args[0])
        elif reply.sticker and reply.sticker.emoji:
            sticker_emoji = reply.sticker.emoji
        else:
            sticker_emoji = "🤔"
    elif args and not reply:
        urlemoji = msg.text.split(" ")
        if len(urlemoji) == 3:                
            png_sticker = urlemoji[1]
            sticker_emoji = urlemoji[2]
        elif len(urlemoji) == 2:
            png_sticker = urlemoji[1]
            sticker_emoji = "🤔"
        else:
            msg.reply_text("/kang <link> <emoji(s) [Optional]>")
            return
        try:
            urllib.urlretrieve(png_sticker, kangsticker)
        except HTTPError as HE:
            if HE.reason == 'Not Found':
                msg.reply_text("Image not found.")
                return
            elif HE.reason == 'Forbidden':
                msg.reply_text("Couldn't access the provided link, The website might have blocked accessing to the website by bot or the website does not existed.")
                return
        except URLError as UE:
            msg.reply_text(f"{UE.reason}")
            return
        except ValueError as VE:
            msg.reply_text(f"{VE}\nPlease try again using http or https protocol.")
            return
    else:
        msg.reply_text("Please reply to a sticker, or an image to kang it!\nDo you know that you can kang image from website too? `/kang [picturelink] <emoji(s)>`.", parse_mode=ParseMode.MARKDOWN)
        return

    try:
        im = imresize(kangsticker)
        im.save(kangsticker, "PNG")
        bot.add_sticker_to_set(user_id=user.id, name=packname,
                                png_sticker=open('kangsticker.png', 'rb'), emojis=sticker_emoji)
        msg.reply_text("Sticker successfully added to [pack](t.me/addstickers/%s)" % packname + "\n"
                        "Emoji(s):" + " " + sticker_emoji, parse_mode=ParseMode.MARKDOWN)
    except OSError as e:
        msg.reply_text("I can only kang images m8.")
        print(e)
        return
    except TelegramError as e:
        if e.message == "Stickerset_invalid":
            makepack_internal(msg, user, open('kangsticker.png', 'rb'), sticker_emoji, bot)
        elif e.message == "Invalid sticker emojis":
            msg.reply_text("Invalid emoji(s).")
        elif e.message == "Stickers_too_much":
            msg.reply_text("Max packsize reached. Press F to pay respecc.")
        print(e)

def makepack_internal(msg, user, png_sticker, emoji, bot):
    name = user.first_name
    name = name[:50]
    packname = f"c{user.id}_by_{bot.username}"
    try:
        success = bot.create_new_sticker_set(user.id, packname, name + "'s haruka pack",
                                             png_sticker=png_sticker,
                                             emojis=emoji)
    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text("Your pack can be found [here](t.me/addstickers/%s)" % packname,
                           parse_mode=ParseMode.MARKDOWN)
        elif e.message == "Peer_id_invalid":
            msg.reply_text("I need you to PM to me first to able to gain your basic information.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                text="PM the bot", url=f"t.me/{bot.username}")]]))
        return

    if success:
        msg.reply_text("Sticker added and new pack successfully created. Get it [here](t.me/addstickers/%s)" % packname,
                       parse_mode=ParseMode.MARKDOWN)
    else:
        msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")

def imresize(kangsticker):
    im = Image.open(kangsticker)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512/size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512/size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    return im


__help__ = """
- /stickerid: Gives the ID of the sticker you've replied to.
- /getsticker: Uploads the .png of the sticker you've replied to.
- /kang: Reply to a sticker to add it to your pack or makes a new one if it doesn't exist.
"""

__mod_name__ = "Stickers"
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker)
KANG_HANDLER = DisableAbleCommandHandler("kang", kang, pass_args=True, admin_ok=True)

dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
