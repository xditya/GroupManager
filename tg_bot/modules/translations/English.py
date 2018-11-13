from tg_bot import dispatcher, ALLOW_EXCL
EnglishStrings = {
    "send-start": """Hi {}, my name {}! If you have any questions on how to use me, read /help - and then head to @NotAvaibleYet.

I'm a group manager bot maintained by [this wonderful person](tg://user?id={}). i be fork of [Marie](https://github.com/PaulSonOfLars/tgbot) 
I'm built in python3, using the \
python-telegram-bot library, and am fully opensource - you can find what makes me tick \
[here](https://gitlab.com/MrYacha/pYanaBot)!

Feel free to submit pull requests on github, or to contact my support group, @NotAvaibleYet, with any bugs, questions \
or feature requests you might have :)

If you're enjoying using me, and/or would like to help me survive in the wild, hit /donate to help fund/upgrade my VPS!
""",

    "send-help": """Hey there! My name is *{}*.
I'm a modular group management bot with a few fun extras! Have a look at the following for an idea of some of the things I can help you with.

Main commands available:
 - /start: start the bot
 - /help: PM's you this message.
 - /help <module name>: PM's you info about that module.
 - /donate: information about how to donate!
 - /lang: Change bot language
 - /settings:
   - in PM: will send you your settings for all supported modules.
   - in a group: will redirect you to pm, with all that chat's settings.
   {}
   """.format(dispatcher.bot.first_name, "" if not ALLOW_EXCL else "\nAll commands can either be used with `/` or `!`.\n")
}