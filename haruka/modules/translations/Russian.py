from haruka import dispatcher

RUN_STRINGS = (
    "Куда ты собрался?",
    "А? что? они ушли?",
    "ZZzzZZzz... А? что? о, опять только эти, ничего страшного.",
    "Вернись сюда!",
    "Не так быстро...",
    "Посмотри на стену!",
    "Не оставляй меня наедине с ними!!",
    "Ты бежишь, ты умираешь.",
    "Ты пожалеешь об этом...",
    "Вы также можете попробовать /kickme, я слышала, что это весело.",
    "Иди, побеспокой кого-нибудь другого, здесь всем плевать.",
    "Ты можешь бежать, но ты не можешь спрятаться.",
    "Это всё, что у тебя есть?",
    "Я стою за тобой...",
    "У вас есть компания!",
    "Мы можем сделать это лёгким или трудным путем.",
    "Ты просто не понимаешь этого, не так ли?",
    "Да, тебе лучше бежать!",
    "Пожалуйста, напомните мне, как меня это волнует?",
    "На твоем месте я бы бежал быстрее.",
    "Это определённо тот дроид, которого мы ищем.",
    "Пусть шансы всегда будут в вашу пользу.",
    "Знаменитые последние слова.",
    "И они исчезли навсегда, чтобы их больше не видели.",
    "\"О, посмотри на меня! Я такой крутой, что могу убежать от бота! \"- это человек",
    "Да, да, просто нажмите /kickme уже.",
    "Вот, возьмите это кольцо и отправляйтесь в Мордор, раз уж вам по пути.",
    "Легенда гласит, что они всё ещё бегут...",
    "В отличие от Гарри Поттера, твои родители не могут защитить тебя от меня.",
    "Страх приводит к гневу. Гнев приводит к ненависти. Ненависть приводит к страданиям. Если вы продолжите бежать в страхе, вы можете "
    "стать следующим Вейдером.",
    "Несколько вычислений спустя, я решил, что мой интерес к вашим махинациям ровно 0.",
    "Легенда гласит, что они всё ещё бегут.",
    "Продолжайте, не уверен, что мы хотим, чтобы вы здесь оставались.",
    "Ты волше-Ой. Погоди. Ты не Гарри, продолжай двигаться.",
    "НЕ БЕГАТЬ ПО КОРИДОРАМ!",
    "Hasta la vista, детка.",
    "Кто выпустил собак?",
    "Это смешно, потому что никому нет дела.",
    "Ах, какая потеря. Он мне нравился.",
    "Честно говоря, моя дорогая, мне наплевать.",
    "Мой молочный коктейль приводит всех мальчиков во двор... Так беги быстрее!",
    "Вы не можете справиться с правдой!",
    "Давным-давно, в далёкой-далёкой галактике... Кому-то было бы до этого дело. Хотя уже нет.",
    "Эй, посмотри на них! Они убегают от неизбежного банхаммера... Мило.",
    "Хан выстрелил первым. Я поступлю так же, как он.",
    "За чем ты бежишь, за белым кроликом?",
    "Как сказал бы Доктор... Беги!",
)

SLAP_TEMPLATES = (
    "{user1} {hits} {user2} {itemp}.",
    "{user1} {hits} в лицо {user2} {itemp}.",
    "{user1} {throws} {itemr} в {user2}.",
    "{user1} берёт {item} и {throws} им в лицо {user2}.",
    "{user1} запускает {itemr} в направлении {user2}.",
    "{user1} начинает безобидно хлопать {user2} {itemp}.",
    "{user1} придавливает {user2} и несколько раз {hits} его {itemp}.",
    "{user1} хвататет {itemr} и {hits} {user2}",
    "{user1} привязывает {user2} к стулу и {throws} {itemr} в него.",
    "{user1} дружески подтолкнул {user2}, чтобы тот научился плавать в лаве."
)

ITEMS =  (
    "чугунная сковорода",
    "большая форель",
    "бейсбольная бита",
    "крикетная бита",
    "деревянная трость",
    "ноготь",
    "принтер",
    "лопата",
    "ЭЛТ-монитор",
    "учебник физики ",
    "тостер",
    "портрет Ричарда Столмана",
    "телевизор",
    "пятитонный грузовик",
    "рулон клейкой ленты",
    "книга",
    "ноутбук",
    "старый телевизор",
    "мешок камней",
    "радужная форель",
    "резиновый цыпленок",
    "шипастая летучая мышь",
    "огнетушитель",
    "тяжёлый камень",
    "кусок грязи",
    "улей",
    "кусок гнилого мяса",
    "медведь",
    "тонна кирпичей",
)

ITEMSP_RU =  (
    "чугунной сковородой",
    "большой форелью",
    "бейсбольной битой",
    "крикетной битой",
    "деревянной тростью",
    "ногтем",
    "принтером",
    "лопатой",
    "ЭЛТ-монитором",
    "учебником физики ",
    "тостером",
    "портретом Ричарда Столмана",
    "телевизором",
    "пятитонным грузовиком",
    "рулоном скотча",
    "книгой",
    "ноутбуком",
    "старым телевизором",
    "мешком камней",
    "радужной форелью",
    "резиновым цыпленоком",
    "шипастой летучей мышью",
    "огнетушителем",
    "тяжёлым камнем",
    "кусоком грязи",
    "улеем",
    "кусоком гнилого мяса",
    "медведем",
    "тонной кирпичей",
    "огромной булкой",
)

ITEMSR_RU =  (
    "чугунную сковородку",
    "большкую форель",
    "бейсбольную биту",
    "крикетную биту",
    "деревянную трость",
    "ноготь",
    "принтер",
    "лопата",
    "ЭЛТ-монитор",
    "учебник физики ",
    "тостер",
    "портрет Ричарда Столмана",
    "телевизор",
    "пятитонный грузовик",
    "рулон клейкой ленты",
    "книга",
    "ноутбук",
    "старый телевизор",
    "мешок камней",
    "радужная форель",
    "резиновый цыпленок",
    "шипастая летучая мышь",
    "огнетушитель",
    "тяжёлый камень",
    "кусок грязи",
    "улей",
    "кусок гнилого мяса",
    "медведь",
    "тонну кирпичей",
)


THROW =  (
    "бросает",
    "швыряет",
)

HIT =  (
    "бьёт",
    "молотит",
    "шлёпает",
    "хлопает",
    "колотит",
    "царапает",
)

MARKDOWN_HELP = """
Markdown - очень мощный инструмент для форматирования текста, который поддерживает  Telegram.  {} имеет некоторые улучшения, чтобы убедиться, что 
сохраненные сообщения правильно написаны , что позволяет создавать кнопки.

- <code>_италик_</code>: выделение с двух сторон текста с помощью '_' приведет к созданию курсивного текста.
- <code>*полужирный*</code>: выделение с двух сторон текста с помощью '*' приведет к получению жирного текста.
- <code>`код`</code>: выделение с двух сторон текста с помощью '`' приведет к получению моноширинного текста, также известного как «код»,
- <code>[ваш_текст](ваша_ссылка)</code>:  это создаст ссылку - сообщение просто покажет <code> ваш_текст </code>, \
и нажатие на него откроет страницу в <code>ваша_ссылка</code>.
Пример: <code>[test](ваша_ссылка)</code>

- <code>[Текст кнопки](buttonurl:ваша ссылка)</code>: это специальное расширение, позволяющее пользователям создавать кнопки-ссылки. <code> Текст Кнопки </code> будет отображаться на кнопке, а <code>ваша ссылка</code> \
будет открывать ваш URL-адрес.
Пример: <code>[Это кнопка](buttonurl:это_ссылка)</code>

Если вам нужно несколько кнопок в одной строке, используйте это:
<code>[one](buttonurl://ваша_ссылка)
[two](buttonurl://google.com:same)</code>
Это создаст две кнопки в одной строке, а не одну кнопку на строку.
"""

RussianStrings = {

#Connections
    "Disabled connections to this chat for users": "Отключены соединения к этому чату для пользователей",
    "Enabled connections to this chat for users": "Включены соединения к этому чату для пользователей",
    "Please enter on/yes/off/no in group!": "Пожалуйста введите on/yes/off/no в группу!",
    "Successfully connected to *{}*": "Успешно подключено к *{}*",
    "Connection failed!": "Подключение не удалось!",
    "Connections to this chat not allowed!": "Подключение к этому чату не разрешено!",
    "Write chat ID to connect!": "Напишите ID чата для подключения",
    "Usage limited to PMs only!": "Использование ограничего в личных сообщениях только!",

#Misc
    "RUNS-K": RUN_STRINGS,
    "SLAP_TEMPLATES-K": SLAP_TEMPLATES,
    "ITEMS-K": ITEMS,
    "HIT-K": HIT,
    "THROW-K": THROW,
    "ITEMP-K": ITEMSP_RU,
    "ITEMR-K": ITEMSR_RU,
    "MARKDOWN_HELP-K": MARKDOWN_HELP,

    "The original sender, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.":
        "Отправитель, {}, имеет ID `{}`.\nПересылающий, {}, имеет ID `{}`.",
    "{}'s id is `{}`.": "ID {} - `{}`.",
    "Your id is `{}`.": "Ваш ID - `{}`.",
    "This group's id is `{}`.": "ID этой группы - `{}`.",

    "I can't extract a user from this.": "Я не могу извлечь ID этого пользователя.",
    "<b>User info</b>:": "<b>Информация о пользователе</b>:",
    "\nFirst Name: {}": "\nИмя: {}",
    "\nLast Name: {}": "\nФамилия: {}",
    "\nUsername: @{}": "\nНик: @{}",
    "\nPermanent user link: {}": "\nПостоянная ссылка на пользователя: {}",
    "\n\nThis person is my owner - I would never do anything against them!":
        "\n\nЭтот человек - мой хозяин, я бы никогда ничего не сделала против него!",
    "\nThis person is one of my sudo users! Nearly as powerful as my owner - so watch it.":
        "\nЭтот человек является одним из моих пользователей sudo! Почти такой же мощный, как мой владелец - так что смотри.",
    "\nThis person is one of my support users! Not quite a sudo user, but can still gban you off the map.":
        "\nЭтот человек является одним из моих поддерживающих пользователей! Не совсем пользователь sudo, но он все равно может удалить вас.",
    "\nThis person has been whitelisted! That means I'm not allowed to ban/kick them.":
        "\nЭтот человек был включен в белый список! Это означает, что я не могу банить и кикать его.",

    "Its always banhammer time for me!": "Всегда есть время для банхаммера!",

    "It's {} in {}": "Сейчас {} в {}",

    "Please reply to a sticker to get its ID.": "Ответье на стикер чтобы получить его ID.",
    "Please reply to a sticker for me to upload its PNG.": "Ответье на стикер чтобы получить его изображение.",

    "Write a location to check the weather.": "Напишите место чтобы получить его погоду.",
    "I will keep an eye on both happy and sad times!": "Я буду следить за счастливыми и печальными временами!",
    "Today in {} is being {}, around {}°C.\n": "Сегодня в {} {}, примерно {}°C.\n",
    "Sorry, location not found.": "Простите, местоположение не найдено.",

    "Deleting identifiable data...": "Удаление пользовательских данных...",

    "Try forwarding the following message to me, and you'll see!":
        "Попробуйте переслать мне следующее сообщение, и вы увидите!",
    "/save test This is a markdown test. _italics_, *bold*, `code`, [URL](example.com) [button](buttonurl:github.com) [button2](buttonurl://google.com:same)":
    """/save test Это тест markdown. _италик_, *жирный*, `код`, \
[ССЫЛКА](example.com) 
[Кнопка](buttonurl:github.com)
[Кнопка2](buttonurl://google.com:same)""",

#Misc GDPR
"send-gdpr": """Ваши персональные данные были удалены.\n\nОбратите внимание, что это не разбанит вас \
из любых чатов, поскольку это данные телеграмма, а не данные YanaBot.
Флуд, предупреждения и АнтиСпам также сохраняются, начиная с \
[этого](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-erasure/), "
в котором четко указано, что право на стирание не применяется \
\"для выполнение задачи, выполняемой в общественных интересах\".""",

#Admin
"How am I meant to promote someone that's already an admin?": "Как я должна назначить кого-то, кто уже является администратором?",
"I can't promote myself! Get an admin to do it for me.": "Я не могу назначить себя! Получите администратора, чтобы сделать это для меня.",
"Successfully promoted in *{}*!": "Успешно назначен в *{}*!",

"This person CREATED the chat, how would I demote them?": "Этот человек СОЗДАЛ чат, как я могу его понизить?",
"Can't demote what wasn't promoted!": "Как я могу понизить того кто не является админом?",
"I can't demote myself!": "Я не могу понизить себя!",
"Successfully demoted in *{}*!": "Успешно понижен в *{}*!",
"Could not demote. I might not be admin, or the admin status was appointed by another user, so I can't act upon them!": 
"Не могу понизить. Возможно, я не администратор, или статус администратора был назначен другим пользователем, поэтому я не могу понизить его!",

"I don't have access to the invite link, try changing my permissions!": "У меня нет доступа к ссылке приглашения, попробуйте изменить мои права!",
"I can only give you invite links for supergroups and channels, sorry!": "Я могу дать ссылку для супергрупп и каналов!",

"Admins in": "Админы в",
"this chat": "этом чате",
" (Creator)": " (Создатель)",

#AFK
"{} is now AFK!": "{} сейчас АФК!",
"{} is no longer AFK!": "{} больше не АФК!",
"{} is AFK!": "{} сейчас АФК!",
"{} is AFK! says its because of: \n{}": "{} сейчас АФК! Потому что: \n{}",

#Antiflood
"I like to leave the flooding to natural disasters. But you, you were just a disappointment. Get out.":
     "Мне нравится оставлять флуд для стихийных бедствий. Но ты был просто разочарованием. Убирайся!",
"I can't kick people here, give me permissions first! Until then, I'll disable antiflood.":
    "Я не могу кикать людей здесь, сначала дайте мне разрешения! Я отключу antiflood.",
"Antiflood has been disabled.": "Антифлуд был выключен.",
"Antiflood has to be either 0 (disabled), or a number bigger than 3 (enabled)!":
    "Antiflood должен быть либо 0 (отключен), либо число больше 3 (включен)!",
"Antiflood has been updated and set to {}": "Антифлуд был установлен на {}",
"Unrecognised argument - please use a number, 'off', or 'no'.":
    "Неизвестный аргумент - используйте число, 'off', или 'no'.",
"I'm not currently enforcing flood control!": "В настоящее время я не применяю контроль над флудом!",
"I'm currently banning users if they send more than {} consecutive messages.":
     "В настоящее время я баню пользователей, если они отправляют более {} последовательных сообщений.",

#Antispam
"I've enabled antispam security in this group. This will help protect you from spammers, unsavoury characters, and the biggest trolls.":
 "Я включила защиту от спама в этой группе. Это поможет защитить вас от спамеров, отвратительных людей и самых больших троллей.",

"I've disabled antispam security in this group. GBans wont affect your users anymore. You'll be less protected from any trolls and spammers though!":
    "Я отключила защиту от спама в этой группе. Антиспам больше не будет влиять на ваших пользователей. Вы не будете защищены от троллей и спамеров!",

"Give me some arguments to choose a setting! on/off, yes/no!\n\nYour current setting is: {}\nWhen True, any gbans that happen will also happen in your group. When False, they won't, leaving you at the possible mercy of spammers.":
    "Дайте мне несколько аргументов, чтобы выбрать настройку! on/off, yes/no!\n\nВаши текущие параметры: {}\nЕсли True, защита от спаммеров (бан людей) также произойдут в вашей группе. Когда false, они не будут, оставляя вас на возможной милости спамеров.",

"Globally banned: <b>{}</b>": "Глобально забанен: <b>{}</b>",
"\nGlobally muted: <b>{}</b>": "\nГлобально замучен: <b>{}</b>",
"\nReason: {}": "\Причина: {}",

#Bans
    "I really wish I could ban admins...": "Мне так жаль, что я не могу забанить админа...",
    "I'm not gonna BAN myself, are you crazy?": "Я не собираюсь банить себя, ты с ума сошел?",
    "Banned!": "Забанен!",
    "Well damn, I can't ban that user.": "Черт, я не могу запретить этого пользователя.",
    "You haven't specified a time to ban this user for!": 
        "Вы не указали время, чтобы забанить этого пользователя!",
    "Banned! User will be banned for {}.": "Забанен! Пользователь забанен на {}.",

#Blacklist
    "<b>Current blacklisted words in {}:</b>\n": "<b>Текущие заблокированные слова в {}:</b>\n",
    "There are no blacklisted messages in <b>{}</b>!": "Нет запрещенных сообщений в <b>{}</b>!",
    "Added <code>{}</code> to the blacklist in <b>{}</b>!":
        "Добавлено <code>{}</code> в черный список в <b>{}</b>!",
    "Tell me which words you would like to add to the blacklist.":
        "Скажите, какие слова вы хотели бы добавить в черный список.",
    "Removed <code>{}</code> from the blacklist in <b>{}</b>!":
        "Удалено <code>{}</code> из черного списка в <b>{}</b>!",
    "This isn't a blacklisted trigger...!": "Это не тригер черного списка...!",
    "None of these triggers exist, so they weren't removed.":
        "Ни один из этих триггеров не существует, поэтому они не были удалены.",
    "Removed <code>{}</code> triggers from the blacklist in <b>{}</b>! {} did not exist, so were not removed.":
        "Удалено <code>{}</code> тригерра из черного списка в <b>{}</b>! {} из них не существовует, поэтому они не были удалены.",
    "Tell me which words you would like to remove from the blacklist.":
        "Скажите, какие слова вы хотите удалить из черного списка.",

    #Filters
    "*Filters in {}:*\n": "*Фильтры в {}:*\n",
    "local filters": "локальные фильтры",
    "*local filters:*\n": "*локальные фильтры:*\n",
    "No filters in {}!": "Нет фильтров в {}!",
    "There is no note message - You can't JUST have buttons, you need a message to go with it!":
        "Вы не можете просто иметь кнопки, вам нужен текст для нормальной работы!",
    "You didn't specify what to reply with!": "Вы не указали на что мне отвечать!",
    "Handler '{}' added in *{}*!": "Фильтр '{}' добавлен в *{}*!",
    "No filters are active in {}!": "Нет фильтров в {}!",
    "Yep, I'll stop replying to that in *{}*." : "Хорошо, я не буду отвечать на это в *{}*.",
    "That's not a current filter - run /filters for all active filters.":
        "Это не текущий фильтр - выполните /filters чтобы увидеть текущие фильтры.",
    
    #Disable
    "Disabled the use of `{}` in *{}*": "Использование `{}` выключено в *{}*",
    "That command can't be disabled": "Эта комманда не может быть выключена",
    "What should I disable?": "Что я должна отключить?",

    "Enabled the use of `{}` in *{}*": "Использование `{}` включено в *{}*",
    "Is that even disabled?": "Это было выключено?",
    "What should I enable?": "Что я должна включить?",

    "The following commands are toggleable:\n{}": "Следующие комманды могут быть выключены:\n{}",
    "No commands can be disabled.": "Нет отключаемых комманд.",
    "No commands are disabled in *{}*!": "Нет выключенных комманд в *{}*!",
    "No commands are disabled!": "Нет выключенных комманд!",
    "The following commands are currently restricted in *{}*:\n{}":
        "Следующие комманды выключены в *{}*:\n{}",

#Locks
    "Locked {} messages for all non-admins!": "Заблокированы {} сообщения для не админов!",
    "What are you trying to lock...? Try /locktypes for the list of lockables":
        "Что вы пытаетесь заблокировать...? Посмотрите /locktypes для списка возможных блокировок",
    "I'm not an administrator, or haven't got delete rights.":
        "Я не администратор или я не имею права на удаление сообщений.",
    "Unlocked {} for everyone!": "Разблокированы {} для всех!",
    "What are you trying to unlock...? Try /locktypes for the list of lockables":
        "Что вы пытаетесь разблокировать...? Посмотрите /locktypes для списка возможных блокировок",
    "What are you trying to unlock...?": "Что вы пытаетесь разблокировать...?",
    "I see a bot, and I've been told to stop them joining... but I'm not admin!":
        "Я вижу бота, и мне сказали банить их... Но я не админ!",
    "Only admins are allowed to add bots to this chat! Get outta here.":
        "Только админам разрешено добавлять ботов в этот чат! Убирайся отсюда.",
    "There are no current locks in *{}*.": "Нет текущих блокировок в *{}*.",
    "These are the locks in *{}*:": "Текущие блокировки в *{}*:",
    "this chat": "этом чате",

#Log channel
    "Now, forward the /setlog to the group you want to tie this channel to!":
        "Теперь перешлите /setlog в группу, с которой вы хотите связать этот канал!",
    "This channel has been set as the log channel for {}.": 
        "Этот канал был установлен как канал логов для {}.",
    "Successfully set log channel!": "Успешно установлен канал логов!",
    "*The steps to set a log channel are:*\n • add bot to the desired channel\n • send /setlog to the channel\n • forward the /setlog to the group\n":
        """*Настройка канала для логирования:*
 • Добавление бота в канал (Как админа!)
 • Отправка `/setlog` в канал
 • Пересылка отправленного сообщения `/setlog` в группе""",

    "Channel has been unlinked from {}": "Канал отключен от {}",
    "Log channel has been un-set.": "Канал логов не установлен.",
    "No log channel has been set yet!": "Канал логов еще не установлен!",

#Users
    "I've seen them in <code>{}</code> chats in total.": 
        "Я видела его в <code>{}</code> чатах.",
    "I've seen them in... Wow. Are they stalking me? They're in all the same places I am... oh. It's me.":
        "Я видела его в... Стоп. Вау. Вы преследуете меня? Я нахожусь во всех чатах, Ох... Да. Это я.",
    
#Msg_deleting
    "Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup.":
        "Не удается удалить все сообщения. Сообщения могут быть слишком старыми, или у меня могут не быть прав на удаление, или это может быть не супергруппа.",
    "Purge complete.": "Чистка завершена.",
    "Reply to a message to select where to start purging from.":
        "Ответьте на сообщение, чтобы выбрать, с чего начать чистку.",
    "Whadya want to delete?": "Что я должна удалить?",

#Muting
    "You'll need to either give me a username to mute, or reply to someone to be muted.":
        "Вам нужно либо дать мне имя пользователя, либо ответить на сообщение, чтобы он был замутен.",
    "I'm not muting myself!": "Я не буду мутить себя!",
    "Afraid I can't stop an admin from talking!": "Боюсь, я не могу остановить админов от разговора!",
    "You'll need to either give me a username to unmute, or reply to someone to be unmuted.":
        "Вам нужно либо дать мне имя пользователя, либо ответить на сообщение, чтобы он был размучен.",
    "This user already has the right to speak in {}.": "Этот пользователь уже имеет право говорить в {}.",
    "Yep, {} can start talking again in {}!": "Да, {} может говорить снова в {}!",
    "This user isn't even in the chat, unmuting them won't make them talk more than they already do!":
        "Этот пользователь даже не в чате",
    "I really wish I could mute admins...": "Мне очень жаль, что я не могу мутить админов...",
    "I'm not gonna MUTE myself, are you crazy?" : "Я не собираюсь себя мутить, ты с ума сошел?",
    "You haven't specified a time to mute this user for!":
        "Вы не указали время для мутинга этого пользователя!",
    "Muted for {} in {}!": "Я заткнула его на {} в {}!",
    "This user is already muted in {}!": "Этот пользователь и так заткнут.",
    "Well damn, I can't mute that user.": "Ну, черт побери, я не могу заткнуть этого пользователя.",

    "You'll need to either give me a username to restrict, or reply to someone to be restricted.":
        "Вам нужно либо указать мне имя пользователя, либо ответить на сообщение чтобы ограничить его.",
    "I'm not restricting myself!": "Я не буду ограничивать себя!",
    "Afraid I can't restrict admins!": "Боюсь, я не могу ограничить админов!",
    "{} is restricted from sending media in {}!": "{} запрещен к отправлению медиа в {}!",
    "This user is already restricted in {}!": "Этот пользователь и так ограничен в {}!",
    "This user isn't in the {}!": "Этот пользователь не в {}!",

    "You'll need to either give me a username to unrestrict, or reply to someone to be unrestricted.":
        "Вам нужно либо дать мне имя пользователя, либо ответить на сообщение, чтобы он мог слать медиа.",
    "This user already has the rights to send anything in {}.": 
        "У этого пользователя и так есть права отправлять что-либо в {}.",
    "Yep, {} can send media again in {}!": "Да, {} может отправлять что-либо в {}!",
    "This user isn't even in the chat, unrestricting them won't make them send anything than they already do!":
        "Этот пользователь даже не в чате.",
    "I really wish I could restrict admins...": "Мне очень хотелось бы ограничить админов...",
    "I'm not gonna RESTRICT myself, are you crazy?": "Я не собираюсь ОГРАНИЧИТЬ себя, ты с ума сошел?",
    "You haven't specified a time to restrict this user for!": 
        "Вы не указали время, чтобы ограничить этого пользователя!",
    "Well damn, I can't restrict that user.": "Ну, черт возьми, я не могу ограничить этого пользователя.",
    "{} is muted in {}!": "{} заткнут в {}!",
    "Restricted from sending media for {} in {}!": "Ограничен от отправление медиа {} в {}!",
    "Restricted for {} in {}!": "{} Ограничен от отправки мендиа в {}!",

#Notes
    "Get rekt": "Нечего давать.",


#Multi
    "Invalid Chat ID provided!": "ID чата недействительный!", #Connections
    "You don't seem to be referring to a user.": "Кажется, вы не обращаетесь к пользователю.", #Admin, Bans, Muting
    "I can't seem to find this user": "Я не могу найти этого пользователя", #Bans, Muting
    "Yes": "Да", #Antispam
    "No": "Нет", #Antispam

#__main__
    #Module names
        "Admin": "Администрирование",
        "AFK": "Режим АФК",
        "AntiFlood": "Антифлуд",
        "Bans": "Баны",
        "Word Blacklists": "Черные списки",
        "Filters": "Фильтры",
        "Command disabling": "Отключение комманд",
        "Antispam security": "Антиспам Защита",
        "Locks": "Блокировки",
        "Log Channels": "Логирование действий",
        "Misc": "Остальное",
        "Purges": "Чистка",
        "Muting & Restricting": "Муты и запреты",
        "Notes": "Заметки",
        "Reporting": "Репорты",
        "RSS Feed": "RSS Лента",
        "Rules": "Правила",
        "Connections": "Соединения",
        "Bios and Abouts": "Подпись человка",
        "Warnings": "Предупреждения",
        "Welcomes/Goodbyes": "Приветствие/Прощание",

#Some main stuff
"Here is the help for the *{}* module:\n{}": "Помощь по модулю *{}*:\n{}",
"Back": "Назад",
"send-help": """Привет всем! Моё имя *{}*. Я модульный бот с функцией управления группами с различными фановыми фичами! 
Взгляните на следующие возможности, которые я могу вам предложить:

Главный комманды:
 - /start: краткая информация про бота.
 - /help: Я напишу вам это сообщение.
 - /help <название модуля>: Я расскажу вам про этот модуль.
 - /donate: Информация о том как вдонатить мне!
 - /lang: Смена языка бота.
 - /settings: Показать текущие настройки модулей.
   {}
   """,


"\nAll commands can either be used with `/` or `!`.\n": "\nВсе коммнды могут начинатся с `/` или `!`\n",

#Module helps
}