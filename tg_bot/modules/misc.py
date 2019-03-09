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

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS, BAN_STICKER, MAPS_API, API_WEATHER
from tg_bot.__main__ import GDPR
from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.filters import CustomFilters

from tg_bot.modules.sql.translation import prev_locale

from tg_bot.modules.translations.strings import tld

from requests import get

GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"
GMAPS_TIME = "https://maps.googleapis.com/maps/api/timezone/json"


@run_async
def insults(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    text = random.choice(tld(chat.id, "INSULTS-K"))
    update.effective_message.reply_text(text)

@run_async
def runs(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(random.choice(tld(chat.id, "RUNS-K")))


@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user

    temp = random.choice(tld(chat.id, "SLAP_TEMPLATES-K"))
    item = random.choice(tld(chat.id, "ITEMS-K"))
    hit = random.choice(tld(chat.id, "HIT-K"))
    throw = random.choice(tld(chat.id, "THROW-K"))
    itemp = random.choice(tld(chat.id, "ITEMP-K"))
    itemr = random.choice(tld(chat.id, "ITEMR-K"))

    repl = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw, itemp=itemp, itemr=itemr)
    #user1=user1, user2=user2, item=item_ru, hits=hit_ru, throws=throw_ru, itemp=itemp_ru, itemr=itemr_ru

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@run_async
def get_bot_ip(bot: Bot, update: Update):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)


@run_async
def get_id(bot: Bot, update: Update, args: List[str]):
    user_id = extract_user(update.effective_message, args)
    chat = update.effective_chat  # type: Optional[Chat]
    if user_id:
        if update.effective_message.reply_to_message and update.effective_message.reply_to_message.forward_from:
            user1 = update.effective_message.reply_to_message.from_user
            user2 = update.effective_message.reply_to_message.forward_from
            update.effective_message.reply_text(tld(chat.id,
                "The original sender, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.").format(
                    escape_markdown(user2.first_name),
                    user2.id,
                    escape_markdown(user1.first_name),
                    user1.id),
                parse_mode=ParseMode.MARKDOWN)
        else:
            user = bot.get_chat(user_id)
            update.effective_message.reply_text(tld(chat.id, "{}'s id is `{}`.").format(escape_markdown(user.first_name), user.id),
                                                parse_mode=ParseMode.MARKDOWN)
    else:
        chat = update.effective_chat  # type: Optional[Chat]
        if chat.type == "private":
            update.effective_message.reply_text(tld(chat.id, "Your id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)

        else:
            update.effective_message.reply_text(tld(chat.id, "This group's id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)


@run_async
def info(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]
    user_id = extract_user(update.effective_message, args)
    chat = update.effective_chat  # type: Optional[Chat]

    if user_id:
        user = bot.get_chat(user_id)

    elif not msg.reply_to_message and not args:
        user = msg.from_user

    elif not msg.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        msg.reply_text(tld(chat.id, "I can't extract a user from this."))
        return

    else:
        return

    text =  tld(chat.id, "<b>User info</b>:")
    text += "\nID: <code>{}</code>".format(user.id)
    text += tld(chat.id, "\nFirst Name: {}").format(html.escape(user.first_name))

    if user.last_name:
        text += tld(chat.id, "\nLast Name: {}").format(html.escape(user.last_name))

    if user.username:
        text += tld(chat.id, "\nUsername: @{}").format(html.escape(user.username))

    text += tld(chat.id, "\nPermanent user link: {}").format(mention_html(user.id, "link"))

    if user.id == OWNER_ID:
        text += tld(chat.id, "\n\nThis person is my owner - I would never do anything against them!")
    else:
        if user.id in SUDO_USERS:
            text += tld(chat.id, "\nThis person is one of my sudo users! " \
            "Nearly as powerful as my owner - so watch it.")
        else:
            if user.id in SUPPORT_USERS:
                text += tld(chat.id, "\nThis person is one of my support users! " \
                        "Not quite a sudo user, but can still gban you off the map.")

            if user.id in WHITELIST_USERS:
                text += tld(chat.id, "\nThis person has been whitelisted! " \
                        "That means I'm not allowed to ban/kick them.")

    for mod in USER_INFO:
        mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


@run_async
def get_time(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    location = " ".join(args)
    if location.lower() == bot.first_name.lower():
        update.effective_message.reply_text(tld(chat.id, "Its always banhammer time for me!"))
        bot.send_sticker(chat.id, BAN_STICKER)
        return

    res = requests.get(GMAPS_LOC, params=dict(address=location, key=MAPS_API))

    if res.status_code == 200:
        loc = json.loads(res.text)
        print(loc)
        if loc.get('status') == 'OK':
            lat = loc['results'][0]['geometry']['location']['lat']
            long = loc['results'][0]['geometry']['location']['lng']

            country = None
            city = None

            address_parts = loc['results'][0]['address_components']
            for part in address_parts:
                if 'country' in part['types']:
                    country = part.get('long_name')
                if 'administrative_area_level_1' in part['types'] and not city:
                    city = part.get('long_name')
                if 'locality' in part['types']:
                    city = part.get('long_name')

            if city and country:
                location = "{}, {}".format(city, country)
            elif country:
                location = country

            timenow = int(datetime.utcnow().timestamp())
            res = requests.get(GMAPS_TIME, params=dict(location="{},{}".format(lat, long), timestamp=timenow, key=MAPS_API))

            if res.status_code == 200:
                offset = json.loads(res.text)['dstOffset']
                timestamp = json.loads(res.text)['rawOffset']
                time_there = datetime.fromtimestamp(timenow + timestamp + offset).strftime("%H:%M:%S on %A %d %B")
                update.message.reply_text(tld(chat.id, "It's {} in {}").format(time_there, location))


@run_async
def echo(bot: Bot, update: Update):
    message = update.effective_message
    message.delete()
    args = update.effective_message.text.split(None, 1)
    if message.reply_to_message:
        message.reply_to_message.reply_text(args[1])
    else:
        message.reply_text(args[1], quote=False)

@run_async
def stickerid(bot: Bot, update: Update):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text("Sticker ID:\n```" + 
                                            escape_markdown(msg.reply_to_message.sticker.file_id) + "```",
                                            parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text(tld(update.effective_chat, "Please reply to a sticker to get its ID."))


@run_async
def getsticker(bot: Bot, update: Update):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        newFile = bot.get_file(file_id)
        newFile.download('sticker.png')
        bot.sendDocument(chat_id, document=open('sticker.png', 'rb'))
        
    else:
        update.effective_message.reply_text(tld(chat_id, "Please reply to a sticker for me to upload its PNG."))


@run_async
def weather(bot, update, args):
    chat = update.effective_chat  # type: Optional[Chat]
    if len(args) == 0:
        update.effective_message.reply_text(tld(chat.id, "Write a location to check the weather."))
        return

    location = " ".join(args)
    if location.lower() == bot.first_name.lower():
        update.effective_message.reply_text(tld(chat.id, "I will keep an eye on both happy and sad times!"))
        bot.send_sticker(chat.id, BAN_STICKER)
        return

    try:
        LANGUAGE = prev_locale(chat.id)
        try:
            LANGUAGE = LANGUAGE.locale_name
        except:
            LANGUAGE = "en"
        print(LANGUAGE)
        owm = pyowm.OWM(API_WEATHER, language=LANGUAGE)
        observation = owm.weather_at_place(location)
        getloc = observation.get_location()
        thelocation = getloc.get_name()
        if thelocation == None:
            thelocation = "Unknown"
        theweather = observation.get_weather()
        temperature = theweather.get_temperature(unit='celsius').get('temp')
        if temperature == None:
            temperature = "Unknown"

        # Weather symbols
        status = ""
        status_now = theweather.get_weather_code()
        print(status_now)
        if status_now == 232: # Rain storm
            status += "⛈️ "
        elif status_now == 321: # Drizzle
            status += "🌧️ "
        elif status_now == 504: # Light rain
            status += "🌦️ "
        elif status_now == 531: # Cloudy rain
            status += "⛈️ "
        elif status_now == 622: # Snow
            status += "🌨️ "
        elif status_now == 781: # Atmosphere
            status += "🌪️ "
        elif status_now == 800: # Bright
            status += "🌤️ "
        elif status_now == 801: # A little cloudy
            status += "⛅️ "
        elif status_now == 804: # Cloudy
            status += "☁️ "

        print(getloc, observation)
        print(status)
        #print(status.formatted_address)
        

        status = status + theweather._detailed_status
                        

        update.message.reply_text(tld(chat.id, "Today in {} is being {}, around {}°C.\n").format(thelocation,
                status, temperature))

    except:
        update.effective_message.reply_text(tld(chat.id, "Sorry, location not found."))


@run_async
def gdpr(bot: Bot, update: Update):
    update.effective_message.reply_text(tld(update.effective_chat.id, "Deleting identifiable data..."))
    for mod in GDPR:
        mod.__gdpr__(update.effective_user.id)

    update.effective_message.reply_text(tld(update.effective_chat.id, "send_gdpr"), parse_mode=ParseMode.MARKDOWN)


@run_async
def markdown_help(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    update.effective_message.reply_text(tld(chat.id, "MARKDOWN_HELP-K"), parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(tld(chat.id, "Try forwarding the following message to me, and you'll see!"))
    update.effective_message.reply_text(tld(chat.id, "/save test This is a markdown test. _italics_, *bold*, `code`, "
                                        "[URL](example.com) [button](buttonurl:github.com) "
                                        "[button2](buttonurl://google.com:same)"))


@run_async
def stats(bot: Bot, update: Update):
    update.effective_message.reply_text("Current stats:\n" + "\n".join([mod.__stats__() for mod in STATS]))


def ping(bot: Bot, update: Update):
    tg_api = ping3('api.telegram.org', count=10)
    google = ping3('google.com', count=10)
    print(google)
    text = "*Pong!*\n"
    text += "Average speed to Telegram bot API server - `{}` ms\n".format(tg_api.rtt_avg_ms)
    if google.rtt_avg:
        gspeed = google.rtt_avg
    else:
        gspeed = google.rtt_avg
    text += "Average speed to Google - `{}` ms".format(gspeed)
    update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def google(bot: Bot, update: Update):
        query = update.effective_message.text.split(" ",1)
        result_ = subprocess.run(['gsearch', str(query[1])], stdout=subprocess.PIPE)
        result = str(result_.stdout.decode())
        update.effective_message.reply_markdown('*Searching:*\n`' + str(query[1]) + '`\n\n*RESULTS:*\n' + result)

@run_async
def github(bot: Bot, update: Update):
    message = update.effective_message
    text = message.text[len('/git '):]
    usr = get(f'https://api.github.com/users/{text}').json()
    if usr.get('login'):
        reply_text = f"""*Name:* `{usr['name']}`
*Username:* `{usr['login']}`
*Account ID:* `{usr['id']}`
*Account type:* `{usr['type']}`
*Location:* `{usr['location']}`
*Bio:* `{usr['bio']}`
*Followers:* `{usr['followers']}`
*Following:* `{usr['following']}`
*Hireable:* `{usr['hireable']}`
*Public Repos:* `{usr['public_repos']}`
*Public Gists:* `{usr['public_gists']}`
*Email:* `{usr['email']}`
*Company:* `{usr['company']}`
*Website:* `{usr['blog']}`
*Last updated:* `{usr['updated_at']}`
*Account created at:* `{usr['created_at']}`
"""
    else:
        reply_text = "User not found. Make sure you entered valid username!"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

SFW_STRINGS = (
    "20%",
    "40%",
    "60%",
    "80%",
    "Sad but you are not gay",
)

@run_async
def amigay(bot: Bot, update: Update):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message

    if user_id == OWNER_ID:
        update.effective_message.reply_text("OMG You are GAYLORD 100%")
    else:
        if user_id in SUDO_USERS:
            update.effective_message.reply_text("You are the follower of gaylord")
        else:
           message.reply_text(random.choice(tld(chat.id, "GAY-K")))

LYRICSINFO = "\n[Full Lyrics](http://lyrics.wikia.com/wiki/%s:%s)"

@run_async
def lyrics(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    text = message.text[len('/lyrics '):]
    song = " ".join(args).split("- ")
    reply_text = f'Looks up for lyrics'
    
    if len(song) == 2:
        while song[1].startswith(" "):
            song[1] = song[1][1:]
        while song[0].startswith(" "):
            song[0] = song[0][1:]
        while song[1].endswith(" "):
            song[1] = song[1][:-1]
        while song[0].endswith(" "):
            song[0] = song[0][:-1]
        try:
            lyrics = "\n".join(PyLyrics.getLyrics(
                song[0], song[1]).split("\n")[:20])
        except ValueError as e:
            return update.effective_message.reply_text("Song %s not found :(" % song[1], failed=True)
        else:
            lyricstext = LYRICSINFO % (song[0].replace(
                " ", "_"), song[1].replace(" ", "_"))
            return update.effective_message.reply_text(lyrics + lyricstext, parse_mode="MARKDOWN")
    else:
        return update.effective_message.reply_text("Invalid syntax! Try Artist - Song name .For example, Luis Fonsi - Despacito", failed=True)

BASE_URL = 'https://del.dog'

@run_async
def paste(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text("What am I supposed to do with this?!")
        return

    r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))

    if r.status_code == 404:
        update.effective_message.reply_text('Failed to reach dogbin')
        r.raise_for_status()

    res = r.json()

    if r.status_code != 200:
        update.effective_message.reply_text(res['message'])
        r.raise_for_status()

    key = res['key']
    if res['isUrl']:
        reply = f'Shortened URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'{BASE_URL}/{key}'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

@run_async
def get_paste_content(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text("Please supply a paste key!")
        return

    format_normal = f'{BASE_URL}/'
    format_view = f'{BASE_URL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BASE_URL}/raw/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text('Failed to reach dogbin')
            else:
                update.effective_message.reply_text('Unknown error occured')
        r.raise_for_status()

    update.effective_message.reply_text('```' + escape_markdown(r.text) + '```', parse_mode=ParseMode.MARKDOWN)

@run_async
def get_paste_stats(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text("Please supply a paste key!")
        return

    format_normal = f'{BASE_URL}/'
    format_view = f'{BASE_URL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BASE_URL}/documents/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text('Failed to reach dogbin')
            else:
                update.effective_message.reply_text('Unknown error occured')
        r.raise_for_status()

    document = r.json()['document']
    key = document['_id']
    views = document['viewCount']
    reply = f'Stats for **[/{key}]({BASE_URL}/{key})**:\nViews: `{views}`'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

@run_async
def ud(bot: Bot, update: Update):
  message = update.effective_message
  text = message.text[len('/ud '):]
  results = get(f'http://api.urbandictionary.com/v0/define?term={text}').json()
  reply_text = f'Word: {text}\nDefinition: {results["list"][0]["definition"]}'
  message.reply_text(reply_text)

__help__ = """
 - /id: get the current group id. If used by replying to a message, gets that user's id.
 - /runs: reply a random string from an array of replies.
 - /insults: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /info: get information about a user.
 - /gdpr: deletes your information from the bot's database. Private chats only.
 - /stickerid: reply to a sticker to me to tell you its file ID.
 - /getsticker: reply to a sticker to me to upload its raw PNG file.
 - /google: Search google
 - /markdownhelp: quick summary of how markdown works in telegram - can only be called in private chats.
 - /git: Returns info about a GitHub user or organization.
 - /amigay: Magic command that check your gayness
 - /lyrics: Find your favorite songs lyrics!
 - /paste: Create a paste or a shortened url using [dogbin](https://del.dog)
 - /getpaste: Get the content of a paste or shortened url from [dogbin](https://del.dog)
 - /pastestats: Get stats of a paste or shortened url from [dogbin](https://del.dog)
 - /ud: Type the word or expression you want to search. For example /ud Gay
"""

__mod_name__ = "Misc"

ID_HANDLER = DisableAbleCommandHandler("id", get_id, pass_args=True)
IP_HANDLER = CommandHandler("ip", get_bot_ip, filters=Filters.chat(OWNER_ID))
PING_HANDLER = DisableAbleCommandHandler("ping", ping)
GOOGLE_HANDLER = DisableAbleCommandHandler("google", google)
LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True)

TIME_HANDLER = DisableAbleCommandHandler("time", get_time, pass_args=True)

INSULTS_HANDLER = DisableAbleCommandHandler("insults", insults)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True)
INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True)
GITHUB_HANDLER = DisableAbleCommandHandler("git", github)
GAY_HANDLER = DisableAbleCommandHandler("amigay", amigay)

ECHO_HANDLER = CommandHandler("echo", echo, filters=Filters.user(OWNER_ID))
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help, filters=Filters.private)

STATS_HANDLER = CommandHandler("stats", stats, filters=CustomFilters.sudo_filter)
GDPR_HANDLER = CommandHandler("gdpr", gdpr, filters=Filters.private)

WEATHER_HANDLER = DisableAbleCommandHandler("weather", weather, pass_args=True)
STICKER_HANDLER = DisableAbleCommandHandler("stickerid", stickerid)
STICKERID_HANDLER = DisableAbleCommandHandler("getsticker", getsticker)

PASTE_HANDLER = DisableAbleCommandHandler("paste", paste, pass_args=True)
GET_PASTE_HANDLER = DisableAbleCommandHandler("getpaste", get_paste_content, pass_args=True)
PASTE_STATS_HANDLER = DisableAbleCommandHandler("pastestats", get_paste_stats, pass_args=True)
UD_HANDLER = DisableAbleCommandHandler("ud", ud)

dispatcher.add_handler(UD_HANDLER)
dispatcher.add_handler(PASTE_HANDLER)
dispatcher.add_handler(GET_PASTE_HANDLER)
dispatcher.add_handler(PASTE_STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(IP_HANDLER)
#dispatcher.add_handler(TIME_HANDLER)
dispatcher.add_handler(INSULTS_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(GDPR_HANDLER)
dispatcher.add_handler(PING_HANDLER)
#dispatcher.add_handler(WEATHER_HANDLER)
dispatcher.add_handler(STICKER_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GOOGLE_HANDLER)
dispatcher.add_handler(GITHUB_HANDLER)
dispatcher.add_handler(GAY_HANDLER)
dispatcher.add_handler(LYRICS_HANDLER)
