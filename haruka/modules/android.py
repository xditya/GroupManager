import html
import json
import time
import yaml
from datetime import datetime
from typing import Optional, List
from hurry.filesize import size as sizee

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from haruka import dispatcher, LOGGER
from haruka.__main__ import GDPR
from haruka.__main__ import STATS, USER_INFO
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.extraction import extract_user
from haruka.modules.helper_funcs.filters import CustomFilters

from requests import get

# DO NOT DELETE THIS, PLEASE.
# Made by @RealAkito on GitHub and Telegram.
# This module was inspired by Android Helper Bot by Vachounet.
# None of the code is taken from the bot itself, to avoid any more confusion.

LOGGER.info("Original Android Modules by @RealAkito on Telegram")


@run_async
def havoc(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/havoc '):]
    fetch = get(f'https://raw.githubusercontent.com/Havoc-Devices/android_vendor_OTA/pie/{device}.json')

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/havoc tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    if fetch.status_code == 200:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']

        reply_text = (f"*Download:* [{filename}]({url})\n"
                      f"*Build size:* `{buildsize_b}`\n"
                      f"*Version:* `{version}`")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    elif fetch.status_code == 404:
        reply_text = "Device not found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def pixys(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/pixys '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/pixys tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://raw.githubusercontent.com/PixysOS-Devices/official_devices/master/{device}/build.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        romtype = response['romtype']
        version = response['version']

        reply_text = (f"*Download:* [{filename}]({url})\n"
                      f"*Build size:* `{buildsize_b}`\n"
                      f"*Version:* `{version}`\n"
                      f"*Rom Type:* `{romtype}`")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    elif fetch.status_code == 404:
        reply_text = "Device not found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def pearl(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/pearl '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/pearl mido`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://raw.githubusercontent.com/PearlOS/OTA/master/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        response = usr['response'][0]
        maintainer = response['maintainer']
        romtype = response['romtype']
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']
        xda = response['xda']

        if xda == '':
            reply_text = (f"*Download:* [{filename}]({url})\n"
                          f"*Build size:* `{buildsize_b}`\n"
                          f"*Version:* `{version}`\n"
                          f"*Maintainer:* `{maintainer}`\n"
                          f"*ROM Type:* `{romtype}`")

            keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
            message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            return

        reply_text = (f"*Download:* [{filename}]({url})\n"
                      f"*Build size:* `{buildsize_b}`\n"
                      f"*Version:* `{version}`\n"
                      f"*Maintainer:* `{maintainer}`\n"
                      f"*ROM Type:* `{romtype}`\n"
                      f"*XDA Thread:* [Link]({xda})")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    elif fetch.status_code == 404:
        reply_text = "Device not found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def posp(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/posp '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/posp tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://api.potatoproject.co/checkUpdate?device={device}&type=weekly')
    if fetch.status_code == 200 and len(fetch.json()['response']) != 0:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']

        reply_text = (f"*Download:* [{filename}]({url})\n"
                      f"*Build size:* `{buildsize_b}`\n"
                      f"*Version:* `{version}`")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    else:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def los(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/los '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/los tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://download.lineageos.org/api/v1/{device}/nightly/*')
    if fetch.status_code == 200 and len(fetch.json()['response']) != 0:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']

        reply_text = (f"*Download:* [{filename}]({url})\n"
                      f"*Build size:* `{buildsize_b}`\n"
                      f"*Version:* `{version}`")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    else:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def dotos(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/dotos '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/dotos tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://raw.githubusercontent.com/DotOS/ota_config/dot-p/{device}.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']
        changelog = response['changelog_device']

        reply_text = (f"*Download:* [{filename}]({url})\n"
                      f"*Build size:* `{buildsize_b}`\n"
                      f"*Version:* `{version}`\n"
                      f"*Device Changelog:* `{changelog}`")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def viper(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/viper '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/viper tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get(f'https://raw.githubusercontent.com/Viper-Devices/official_devices/master/{device}/build.json')
    if fetch.status_code == 200:
        usr = fetch.json()
        response = usr['response'][0]
        filename = response['filename']
        url = response['url']
        buildsize_a = response['size']
        buildsize_b = sizee(int(buildsize_a))
        version = response['version']

        reply_text = (f"*Download:* [{filename}]({url})\n"
                      f"*Build size:* `{buildsize_b}`\n"
                      f"*Version:* `{version}`")

        keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    elif fetch.status_code == 404:
        reply_text="Device not found"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
def evo(bot: Bot, update: Update):
    message = update.effective_message
    device = message.text[len('/evo '):]
    if device == "example":
        reply_text = "Why are you trying to execute a example json?"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    if device == "x00t":
        device = "X00T"

    if device == "x01bd":
        device = "X01BD"

    fetch = get(f'https://raw.githubusercontent.com/Evolution-X-Devices/official_devices/master/builds/{device}.json')

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/evo tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    if device == 'gsi':
        reply_text = """
Please check Evolution Updates channel! @EvolutionXUpdates or Click the button down below to download the GSIs!
"""
        keyboard = [[InlineKeyboardButton(text="Click to Download", url="https://sourceforge.net/projects/evolution-x/files/GSI/")]]
        message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    if fetch.status_code == 200:
        try:
            usr = fetch.json()
            filename = usr['filename']
            url = usr['url']
            version = usr['version']
            maintainer = usr['maintainer']
            maintainer_url = usr['telegram_username']
            size_a = usr['size']
            size_b = sizee(int(size_a))

            reply_text = (f"*Download:* [{filename}]({url})\n"
                          f"*Build Size:* `{size_b}`\n"
                          f"*Android Version:* `{version}`\n"
                          f"*Maintainer:* [{maintainer}](https://t.me/{maintainer_url})\n")

            keyboard = [[InlineKeyboardButton(text="Click to Download", url=f"{url}")]]
            message.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            return

        except ValueError:
            reply_text = "Tell the rom maintainer to fix their OTA json. I'm sure this won't work with OTA and it won't work with this bot too :P"
            message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            return

    elif fetch.status_code == 404:
        reply_text = "Device not found!"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return


def enesrelease(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    usr = get(f'https://api.github.com/repos/EnesSastim/Downloads/releases/latest').json()
    reply_text = "*Enes Sastim's lastest upload(s)*\n"
    for i in range(len(usr)):
        try:
            name = usr['assets'][i]['name']
            url = usr['assets'][i]['browser_download_url']
            reply_text += f"[{name}]({url})\n"
        except IndexError:
            continue
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


def phh(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    usr = get(f'https://api.github.com/repos/phhusson/treble_experimentations/releases/latest').json()
    reply_text = "*Phh's lastest AOSP Release(s)*\n"
    for i in range(len(usr)):
        try:
            name = usr['assets'][i]['name']
            url = usr['assets'][i]['browser_download_url']
            reply_text += f"[{name}]({url})\n"
        except IndexError:
            continue
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


def descendant(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    usr = get(f'https://api.github.com/repos/Descendant/InOps/releases/latest').json()
    reply_text = "*Descendant GSI Download(s)*\n"
    for i in range(len(usr)):
        try:
            name = usr['assets'][i]['name']
            url = usr['assets'][i]['browser_download_url']
            download_count = usr['assets'][i]['download_count']
            reply_text += f"[{name}]({url}) - Downloaded `{download_count}` Times\n\n"
        except IndexError:
            continue
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)


def miui(bot: Bot, update: Update):
    giturl = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/"
    message = update.effective_message
    device = message.text[len('/miui '):]

    if device == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/miui whyred`!"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    result = "*Recovery ROM*\n\n"
    result += "*Stable*\n"
    stable_all = yaml.load(get(giturl + "stable_recovery/stable_recovery.yml").content, Loader=yaml.FullLoader)
    data = [i for i in stable_all if device == i['codename']]
    if len(data) != 0:
        for i in data:
            result += "[" + i['filename'] + "](" + i['download'] + ")\n\n"

        result += "*Weekly*\n"
        weekly_all = yaml.load(get(giturl + "weekly_recovery/weekly_recovery.yml").content, Loader=yaml.FullLoader)
        data = [i for i in weekly_all if device == i['codename']]
        for i in data:
            result += "[" + i['filename'] + "](" + i['download'] + ")"
    else:
        result = "Couldn't find any device matching your query."

    message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


@run_async
def getaex(bot: Bot, update: Update, args: List[str]):
    AEX_OTA_API = "https://api.aospextended.com/ota/"
    message = update.effective_message

    if len(args) != 2:
        reply_text = "Please type your device **codename** and **Android Version** into it!\nFor example, `/aex jason pie`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    device = args[0]
    version = args[1]
    res = get(AEX_OTA_API + device + '/' + version.lower())
    if res.status_code == 200:
        apidata = json.loads(res.text)
        if apidata.get('error'):
            message.reply_text("Sadly there isn't any build available for " + device)
            return
        else:
            developer = apidata.get('developer')
            developer_url = apidata.get('developer_url')
            xda = apidata.get('forum_url')
            filename = apidata.get('filename')
            url = "https://downloads.aospextended.com/download/" + device + "/" + version + "/" + apidata.get('filename')
            builddate = datetime.strptime(apidata.get('build_date'), "%Y%m%d-%H%M").strftime("%d %B %Y")
            buildsize = sizee(int(apidata.get('filesize')))

            message = (f"*Download:* [{filename}]({url})\n"
                       f"*Build date:* `{builddate}`\n"
                       f"*Build size:* `{buildsize}`\n"
                       f"*By:* [{developer}]({developer_url})\n")

            keyboard = [[InlineKeyboardButton(text="Click here to download", url=f"{url}")]]
            update.effective_message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            return
    else:
        message.reply_text("No builds found for the provided device-version combo.")


@run_async
def bootleggers(bot: Bot, update: Update):
    message = update.effective_message
    codename = message.text[len('/bootleggers '):]

    if codename == '':
        reply_text = "Please type your device **codename** into it!\nFor example, `/bootleggers tissot`"
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        return

    fetch = get('https://bootleggersrom-devices.github.io/api/devices.json')
    if fetch.status_code == 200:
        nestedjson = fetch.json()

        if codename.lower() == 'x00t':
            devicetoget = 'X00T'
        else:
            devicetoget = codename.lower()

        reply_text = ""
        devices = {}

        for device, values in nestedjson.items():
            devices.update({device: values})

        if devicetoget in devices:
            for oh, baby in devices[devicetoget].items():
                dontneedlist = ['id', 'filename', 'download', 'xdathread']
                peaksmod = {'fullname': 'Device name', 'buildate': 'Build date', 'buildsize': 'Build size',
                            'downloadfolder': 'SourceForge folder', 'mirrorlink': 'Mirror link', 'xdathread': 'XDA thread'}
                if baby and oh not in dontneedlist:
                    if oh in peaksmod:
                        oh = peaksmod[oh]
                    else:
                        oh = oh.title()

                    if oh == 'SourceForge folder':
                        reply_text += f"\n*{oh}:* [Here]({baby})"
                    elif oh == 'Mirror link':
                        reply_text += f"\n*{oh}:* [Here]({baby})"
                    else:
                        reply_text += f"\n*{oh}:* `{baby}`"

            reply_text += f"\n*XDA Thread:* [Here]({devices[devicetoget]['xdathread']})"
            reply_text += f"\n*Download:* [{devices[devicetoget]['filename']}]({devices[devicetoget]['download']})"
            reply_text = reply_text.strip("\n")
        else:
            reply_text = 'Device not found.'

    elif fetch.status_code == 404:
        reply_text="Couldn't reach Bootleggers API."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


__help__ = """
*This module is made with love by* @RealAkito *and code beauty by* @kandnub
 *Device Specific Rom*
 - /pearl <device>: Get the Pearl Rom
 - /havoc <device>: Get the Havoc Rom
 - /posp <device>: Get the POSP Rom
 - /viper <device>: Get the Viper Rom
 - /evo <device>: Get the Evolution X Rom
 - /dotos <device>: Get the DotOS Rom
 - /aex <device> <android version>: Get the AEX Rom
 - /pixys <device>: Get the Pixy Rom
 - /los <device>: Get the LineageOS Rom
 - /bootleggers <device>: Get the Bootleggers Rom
 *GSI*
 - /phh: Get the lastest Phh AOSP Oreo GSI!
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
PIXYS_HANDLER = DisableAbleCommandHandler("pixys", pixys, admin_ok=True)
LOS_HANDLER = DisableAbleCommandHandler("los", los, admin_ok=True)
BOOTLEGGERS_HANDLER = DisableAbleCommandHandler("bootleggers", bootleggers, admin_ok=True)

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
dispatcher.add_handler(PIXYS_HANDLER)
dispatcher.add_handler(LOS_HANDLER)
dispatcher.add_handler(BOOTLEGGERS_HANDLER)
