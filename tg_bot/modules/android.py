import subprocess
import html
import json
import random
import time
import pyowm
from pyowm import timeutils, exceptions
from datetime import datetime
from typing import Optional, List
from pythonping import ping as ping3
from typing import Optional, List
from PyLyrics import *
from hurry.filesize import size

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS, BAN_STICKER
from tg_bot.__main__ import GDPR
from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.filters import CustomFilters

from tg_bot.modules.sql.translation import prev_locale

from tg_bot.modules.translations.strings import tld

from requests import get

AEX_OTA_API = "https://api.aospextended.com/ota/"

@run_async
def havoc(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/havoc '):]
    fetch = get(f'https://raw.githubusercontent.com/Havoc-Devices/android_vendor_OTA/pie/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][0]['filename']}]({usr['response'][0]['url']})
*Size:* `{usr['response'][0]['size']}`
*Version:* `{usr['response'][0]['version']}`
"""
    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def pixy(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/pixy '):]
    fetch = get(f'https://raw.githubusercontent.com/PixysOS-Devices/official_devices/master/{device}/build.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][0]['filename']}]({usr['response'][0]['url']})
*Size:* `{usr['response'][0]['size']}`
*Rom Type:* `{usr['response'][0]['romtype']}`
*Version:* `{usr['response'][0]['version']}`
"""
    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def pearl(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/pearl '):]
    fetch = get(f'https://raw.githubusercontent.com/PearlOS/OTA/master/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Maintainer:* `{usr['response'][0]['maintainer']}`
*Rom Type:* `{usr['response'][0]['romtype']}`
*Download:* [{usr['response'][0]['filename']}]({usr['response'][0]['url']})
*Size:* `{usr['response'][0]['size']}`
*Version:* `{usr['response'][0]['version']}`
*XDA Thread:* [Click me]({usr['response'][0]['xda']})
"""
    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def posp(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/posp '):]
    fetch = get(f'https://api.potatoproject.co/checkUpdate?device={device}&type=weekly')
    if fetch.status_code == 200 and str(fetch.json()['response']) != "[]":
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][-1]['filename']}]({usr['response'][-1]['url']})
*Size:* `{usr['response'][-1]['size']}`
*Version:* `{usr['response'][-1]['version']}`
"""
    else:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def dotos(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/dotos '):]
    fetch = get(f'https://raw.githubusercontent.com/DotOS/ota_config/dot-p/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][0]['filename']}]({usr['response'][0]['url']})
*Size:* `{usr['response'][0]['size']}`
*Version:* `{usr['response'][0]['version']}`
*Device Changelog:* `{usr['response'][0]['changelog_device']}`
"""
    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def viper(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/havoc '):]
    fetch = get(f'https://raw.githubusercontent.com/Viper-Devices/official_devices/master/{device}/build.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['response'][0]['filename']}]({usr['response'][0]['url']})
*Size:* `{usr['response'][0]['size']}`
*Version:* `{usr['response'][0]['version']}`
"""
    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def evo(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/evo '):]
    fetch = get(f'https://raw.githubusercontent.com/evolution-x/official_devices/master/builds/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        reply_text = f"""*Download:* [{usr['filename']}]({usr['url']})
*Size:* `{usr['size']}`
*Android Version:* `{usr['version']}`
*Maintainer:* [{usr['maintainer']}]({usr['maintainer_url']})
*XDA Thread:* [Here]({usr['forum_url']})
"""
    elif fetch.status_code == 404:
        reply_text = "Device not found!"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def enesrelease(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    usr = get(f'https://api.github.com/repos/EnesSastim/Downloads/releases/latest').json()
    reply_text = "*EnesSastim lastest upload*\n"
    for i in range(len(usr)):
        try:
            reply_text += f"[{usr['assets'][i]['name']}]({usr['assets'][i]['browser_download_url']})\n"
        except IndexError:
            continue
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

def phh(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    usr = get(f'https://api.github.com/repos/phhusson/treble_experimentations/releases/latest').json()
    reply_text = "*Phh lastest AOSP Release*\n"
    for i in range(len(usr)):
        try:
            reply_text += f"[{usr['assets'][i]['name']}]({usr['assets'][i]['browser_download_url']})\n"
        except IndexError:
            continue
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

def descendant(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    usr = get(f'https://api.github.com/repos/Descendant/InOps/releases/latest').json()
    reply_text = "*Descendant GSI Download*\n"
    for i in range(len(usr)):
        try:
            reply_text += f"[{usr['assets'][i]['name']}]({usr['assets'][i]['browser_download_url']})\n"
        except IndexError:
            continue
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

def miui(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/miui '):]
    result = "*Recovery ROM*\n"
    result += "*Stable*\n"
    stable_all = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "stable_recovery/stable_recovery.json").content)
    data = [i for i in stable_all if device == i['codename']]
    for i in data:
        result += "[" + i['filename'] + "](" + i['download'] + ")\n"

    result += "*Weekly*\n"
    weekly_all = json.loads(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "weekly_recovery/weekly_recovery.json").content)
    data = [i for i in weekly_all if device == i['codename']]
    for i in data:
        result += "[" + i['filename'] + "](" + i['download'] + ")\n"

    message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

@run_async
def getaex(bot: Bot, update: Update, args: List[str]):
    if len(args) != 2:
        update.effective_message.reply_text("Pass correct parameters, Check help for more info !")
        return

    device = args[0]
    version = args[1]
    res = requests.get(AEX_OTA_API + device + '/' + version.lower())
    if res.status_code == 200:
        apidata = json.loads(res.text)
        if apidata.get('error'):
            update.effective_message.reply_text("Sadly no builds available for " + device)
            return
        else:
            message = """ 
*AOSP EXTENDED for {}* \

`by:` [{}]({}) \

[XDA thread]({}) \



`Latest build:` [{}]({}) \

`Build date: {}` \

`Build size: {}` \

`md5: {}`
""".format(device, apidata.get('developer'), apidata.get('developer_url'),
           apidata.get('forum_url'),
           apidata.get('filename'),
           "https://downloads.aospextended.com/download/" + device + "/" + version + "/" + apidata.get('filename'),
           datetime.strptime(apidata.get('build_date'), "%Y%m%d-%H%M").strftime("%d %B %Y"),
           size(int(apidata.get('filesize'))),
           apidata.get('md5'))
            update.effective_message.reply_text(
                message, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            return
    else:
        update.effective_message.reply_text("No builds found for the provided device-version combo.")


__help__ = """
 *Device Specific Rom*
 - /pearl <device>: Get the Pearl Rom
 - /havoc <device>: Get the Havoc Rom
 - /posp <device>: Get the POSP Rom
 - /viper <device>: Get the Viper Rom
 - /evo <device>: Get the Evolution X Rom
 - /dotos <device>: Get the DotOS Rom
 - /aex <device> <android version>: Get the AEX Rom
 - /pixy <device>: Get the Pixy Rom
 *GSI*
 - /phh: Get the lastest Phh AOSP GSI!
 - /descendant: Get the lastest Descendant GSI!
 - /enesrelease: Get the lastest Enes upload
"""

__mod_name__ = "Android"


GETAEX_HANDLER = DisableAbleCommandHandler("aex", getaex, pass_args=True, admin_ok=True)
MIUI_HANDLER = DisableAbleCommandHandler("miui", miui, admin_ok=True)
EVO_HANDLER = DisableAbleCommandHandler("evo", evo, admin_ok=True)
HAVOC_HANDLER = DisableAbleCommandHandler("havoc", havoc, admin_ok=True)
VIPER_HANDLER = DisableAbleCommandHandler("viper", viper, admin_ok=True)
DESCENDANT_HANDLER = DisableAbleCommandHandler("descendant", descendant, pass_args=True, admin_ok=True)
ENES_HANDLER = DisableAbleCommandHandler("enesrelease", enesrelease, pass_args=True, admin_ok=True)
PHH_HANDLER = DisableAbleCommandHandler("phh", phh, pass_args=True, admin_ok=True)
PEARL_HANDLER = DisableAbleCommandHandler("pearl", pearl, admin_ok=True)
POSP_HANDLER = DisableAbleCommandHandler("posp", posp, admin_ok=True)
DOTOS_HANDLER = DisableAbleCommandHandler("dotos", dotos, admin_ok=True)
PIXY_HANDLER = DisableAbleCommandHandler("pixy", pixy, admin_ok=True)

dispatcher.add_handler(GETAEX_HANDLER)
dispatcher.add_handler(MIUI_HANDLER)
dispatcher.add_handler(EVO_HANDLER)
dispatcher.add_handler(HAVOC_HANDLER)
dispatcher.add_handler(VIPER_HANDLER)
dispatcher.add_handler(DESCENDANT_HANDLER)
dispatcher.add_handler(ENES_HANDLER)
dispatcher.add_handler(PHH_HANDLER)
dispatcher.add_handler(PEARL_HANDLER)
dispatcher.add_handler(POSP_HANDLER)
dispatcher.add_handler(DOTOS_HANDLER)
dispatcher.add_handler(PIXY_HANDLER)
