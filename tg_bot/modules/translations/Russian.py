from tg_bot import dispatcher, ALLOW_EXCL
RussianStrings = {

#Connections
    "Disabled connections to this chat for users": "Отключены соеденения к этому чату для пользователей",
    "Enabled connections to this chat for users": "Включены соеденения к этому чату для пользователей",
    "Please enter on/yes/off/no in group!": "Пожалуйста введите on/yes/off/no в группу!",
    "Successfully connected to *{}*": "Успешно подключено к *{}*",
    "Connection failed!": "Подключение не удалось!",
    "Connections to this chat not allowed!": "Подключение к этому чату не разрешено!",
    "Write chat ID to connect!": "Напишите ID чата для подключения",
    "Usage limited to PMs only!": "Использование ограничего в личных сообщениях только!",More s

#Multi
    "Invalid Chat ID provided!": "ID чата недействительный!", #Connections

#__main__
    #Module names
        "Admin": "Администрирование",
        "AFK": "Режим АФК",
        "AntiFlood": "Антифлуд",
        "Bans": "Баны",
        "Word Blacklists": "Черный списки",
        "Filters": "Фильтры",
        "Command disabling": "Отключение комманд",
        "Global Bans": "Глобальные баны",
        "Locks": "Блокировки",
        "Log Channels": "Логирование действий",
        "Misc": "Остальное",
        "Purges": "Чистка",
        "Muting": "Мут",
        "Notes": "Заметки",
        "Reporting": "Репорты",
        "RSS Feed": "RSS Лента",
        "Rules": "Правила",
        "Connections": "Соеденения",
        "Bios and Abouts": "Подпись человка",
        "Warnings": "Предупреждения",
        "Welcomes/Goodbyes": "Приветсвие/Прощание",

#Some main stuff
"Here is the help for the *{}* module:": "Вот помощь по модулю *{}*:",
"send-help": """Привет всем! Мое имя *{}*. Я модульный бот с функцией управления группами с различными фановыми фичами! 
Взгляните на следующие возможности, которые я могу вам предложить:

Главный комманды:
 - /start: краткая информация про бота.
 - /help: Я напишу вам это сообщение.
 - /help <название модуля>: Я расскажу вам про этот модуль.
 - /donate: Информация о том как вдонатить мне!
 - /lang: Смена языка бота
 - /settings: Показать текущие настройки модулей
   {}
   """.format(dispatcher.bot.first_name, "" if not ALLOW_EXCL else "\nВсе команды могут начинатся с `/` или `!`.\n")

    #Module helps
}