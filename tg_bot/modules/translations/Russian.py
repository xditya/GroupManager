from tg_bot import dispatcher, ALLOW_EXCL
RussianStrings = {
    #Lang
        "Switched to {} successfully!" : "Переключение языка на {} успешно!",
    #Filters
        "*Filters in this chat:*\\n": "*Фильтры в этом чате:*\\n",
        "*Not* currently enforcing flood control.": "В настоящие время *НЕ* обеспечивается управление флудом.",
        "Could not parse filter %s in chat %s": "Не удалось обработать фильтр %s в чате %s",
        "Handler '{}' added!": "Обработчик '{} ' добавлен!",
        "Message %s could not be parsed": "Сообщение %s не удалось обработать",
        "No filters are active here!": "Здесь нет активных фильтров!",
    #Notes
        "*Notes in chat:*\\n": "*Заметки в чате:*\\n",
        "@MarieSupport if you can't figure out why!": "@MarieSupport, если Вы не можете понять, почему!",
        "Bots are kinda handicapped by telegram, making it hard for bots to ": "Телеграм несколько ограничил возможности ботов, им трудно ",
        "Dude, there's no note": "Чувак, заметки нет",
        "Looks like the original sender of this note has deleted ": "Похоже, что первоначальный Отправитель этой заметки удалил ",
        "Looks like you tried to mention someone I've never seen before. If you really ": "Похоже, вы пытались упомянуть кого-то, кого я никогда раньше не видела. Если вы действительно ",
        "Successfully removed note.": "Успешно удалена заметка.",
        "your saved notes.": "ваши сохранённые заметки.",
        "No notes in this chat!": "Никаких заметок в этом чате!",
        "Seems like you're trying to save a message from a bot. Unfortunately, ": "Похоже, вы пытаетесь сохранить сообщение от бота. К сожалению, ",
    #Warnings
        "<b>Current warning filters in this chat:</b>\\n": "<b>Текущие фильтры предупреждений в этом чате: </b>\\n",
        "Automated warn filter.": "Автоматический фильтр предупреждений.",
    #Blacklist
        "Added <code>{}</code> to the blacklist!": "Добавлен <code>{}</code> в черный спсок!",
        "Added <code>{}</code> triggers to the blacklist.": "Добавлено ключевое слово <code>{}</code> в черный список.",
        "Current <b>blacklisted</b> words:\\n": "Atualmente palavras na <b>lista negra</b>:\\n",
        "Error while deleting blacklist message.": "Erro ao excluir mensagem da lista negra.",
        "Removed <code>{}</code> from the blacklist!": "Removido <code>{}</code> da lista negra!",
        "Removed <code>{}</code> triggers from the blacklist.": "Removido gatilho <code>{}</code> da lista negra.",
        "Removed <code>{}</code> triggers from the blacklist. {} did not exist, ": "Removido gatilho <code>{}</code> da lista negra. {} não existe, ",
        "None of these triggers exist, so they weren't removed.": "Nenhum desses gatilhos existem, portanto, eles não foram removidos.",
        "Tell me which words you would like to remove from the blacklist.": "Скажите, какие слова вы хотели бы удалить из чёрного списка.",
    #AdminList
        "Admins in": "Админы в",
        " (Creator)": " (Создатель)",
    #Antiflood
        "Afraid I can't stop an admin from talking!": "Боюсь, я не могу остановить админа от разговора!",
        "Antiflood has been disabled.": "Антифлуд был отключён.",
        "Antiflood has been updated and set to {}": "Антифлуд был обновлён и установлен на <code>{}</code> сообщения",
        "Antiflood has to be either 0 (disabled), or a number bigger than 3!": "Антифлуд должен содержать число 0 (выключен), или больше чем 3!",
        "Antiflood is set to `{}` messages.": "Антифлуд установлен на `{}` сообщений.",
        "I like to leave the flooding to natural disasters. But you, you were just a": "Я предпочитаю считать наводнения стихийным бедствиям. Но вы, вы были просто",
        "I'm currently banning users if they send more than {} consecutive messages.": "В настоящее время я запрещаю пользователям отправлять более {} последовательных сообщений.",
        "I'm not currently enforcing flood control!": "Я сейчас не контролирую флуд!",
    #Bans
        "Banned!": "Забанен!",
        "Banned! User will be banned for {}.": "Забанен! Пользователь будет забанен за {}.",
        "Could not ban user. Perhaps the group has been suspended by Telegram.": "Не удалось забанить пользователя. Возможно, группа была приостановлена телеграмом.",
        "Chat not found! Make sure you entered a valid chat ID and I'm part of that chat.": "Чат не найден! Убедитесь, что вы ввели действительный идентификатор чата, и я участвую в этом чате.",
        "ERROR banning user %s in chat %s (%s) due to %s": "ОШИБКА бана пользователя %s в чате %s (%s) из-за %s",
        "Huh? I can't :/": "А? Я не могу :/",
        "I can't restrict people there! Make sure I'm admin and can ban users.": "Я не могу ограничивать людей там! Убедитесь, что я админ и могу банить пользователей.",
        "I can't seem to find this user": "Я не могу найти этого пользователя",
        "I really wish I could ban admins...": "Я действительно хотела бы банить админов...",
        "I wish I could... but you're an admin.": "Хотелось бы мне это сделать... но вы ведь админ.",
        "I'm not gonna BAN myself, are you crazy?": "Я не собираюсь банить себя, вы с ума сошли?",
        "I'm sorry, but that's a private chat!": "Простите, но это личный чат!",
        "Invalid time amount specified.": "Указано недопустимое количество времени.",
        "Invalid time type specified. Expected m,h, or d, got: {}": "Указан недопустимый тип времени. Ожидается м,ч или д, получено: {}",
        "No problem.": "Не проблема.",
        #Unbans
        "How would I unban myself if I wasn't here...?": "Как бы я разбанила себя, если бы меня здесь не было...?",
    #Kick
        "I can't kick people here, give me permissions first! Until then, I'll disable antiflood.": "Я не могу выгонять людей здесь, сначала дайте мне разрешения! А пока, я отключу антифлуд.",
        "I really wish I could kick admins...": "Я действительно хотела бы выгонять админов...",
    #Mute
        "ERROR muting user %s in chat %s (%s) due to %s": "ОШИБКА приглушения пользователя %s в чате %s (%s) из-за %s",
        "I'm not gonna MUTE myself, are you crazy?": "Я не собираюсь ПРИГЛУШАТЬ себя, вы с ума сошли?",
        "I'm not muting myself!": "Я не буду себя глушить!",
        "Muted! User will be Muted for {}.": "Приглушён! Пользователь будет приглушён за {}.",
    #Promote
        "Can't demote what wasn't promoted!": "Нельзя понизить то, что не было повышено!",
        "How am I meant to promote someone that's already an admin?": "Как я должна продвигать кого-то, кто уже является админом?",
        "I can't promote myself! Get an admin to do it for me.": "Я не могу продвигать себя! Попросите админа сделать это за меня.",
        #Demote
        "Could not demote. I might not be admin, or the admin status was appointed by another ": "Не удалось понизить. Возможно, я не админ, или статус админа был назначен другим ",
        "I can't demote myself! Get an admin to do it for me.": "Я не могу понизить себя! Попросите админа сделать это за меня.",
        "Successfully demoted!": "Понижен в должности!",
    #Purges / Del massages
        "Cannot delete all messages. The messages may be too old, I might ": "Невозможно удалить все сообщения. Сообщения могут быть слишком старыми, я могла бы ",
        "I'm not an administrator, or haven't got delete rights.": "Я не являюсь админом или не имею прав на удаление.",
        "Message to delete not found": "Сообщений для удаления не найдено",
        "Purge complete.": "Чистка завершена.",
        "Reply to a message to select where to start purging from.": "Ответьте на сообщение, чтобы выбрать, с чего начать очистку.",
    #Multi
        "Chat not found": "Чат не найден",
        "Group chat was deactivated": "Групповой чат отключён", #Gban, Gmute
        "Reply message not found": "Ответ не найден",
    #Disabling
        "Command disabling": "Отключение команды",
        "Disabled the use of `{}`": "Отключено использование `{}`",
        "No commands are disabled!": "Никакие команды не отключены!",
        "No commands can be disabled.": "Никакие команды нельзя отключить.",
        "Is that even disabled?": "Это вообще отключено?",
        "{} disabled items, across {} chats.": "{} отключенных элемента в {} чатах.",#тут падежи нужны
        "The following commands are currently restricted:\\n{}": "В настоящее время ограничены следующие команды:\\n{}",
        "Enabled the use of `{}`": "Включено использование `{}`",
        "What should I disable?": "Что я должна отключить?",
        #Enable
        "What should I enable?": "Что я должна включить?",
    #Rules
        "Contact me in PM to get this group's rules.": "Свяжитесь со мной в личке, чтобы получить правила этой группы.",
        "Successfully cleared rules!": "Правила успешно очищены!",
        "Successfully set rules for this group.": "Успешно установлены правила для этой группы.",
    #Warns
        "Damn admins, can't even be warned!": "Чёртовы админы, даже не вынести предупреждение!",
        "Give me a number as an arg!": "Назови мне число в качестве аргумента!",
        "Has disabled strong warns. Users will only be kicked.": "Отключила строгие предупреждения. Пользователи будут только выкинуты.",
        "Has enabled strong warns. Users will be banned.": "Включила строгие предупреждения. Пользователи будут забанены.",
        "I only understand on/yes/no/off!": "Я понимаю только on/yes/no/off!",
        "User has already has no warns.": "Пользователь уже не имеет предупреждений.",
        "User has {}/{} warnings, but no reasons for any of them.": "У пользователя есть предупреждения {}/{}, но нет причин для них.", #Здесь можно как вариант, переменные перед словом предупреждения и тогда падежи
        "No user has been designated!": "Ни один пользователь не был назначен!",
        "No user was designated!": "Ни один пользователь не был назначен!",
        "No warning filters are active here!": "Здесь нет активных фильтров предупреждений!",
        "Remove warn": "Удалить предупреждение", #Button
        "Warn handler added for '{}'!": "Добавлен обработчик предупреждений для '{}'!",
        "Warn removed by {}.": "Предупреждение удалено {}.",
        "Warnings have been reset!": "Предупреждения сброшены!",
        "Warns are currently set to *ban* users when they exceed the limits.": "Предупреждения в настоящее время установлены так, чтобы *банить* пользователей, когда они превышают пределы.",
        "Warns are currently set to *kick* users when they exceed the limits.": "Предупреждения в настоящее время установлены так, чтобы *выгонять* пользователей, когда они превышают пределы.",
        "{} has {}/{} warnings... watch out!": "У {} {}/{} предупреждения... осторожно!", #падежи
    #Invitelink
        "I can only give you invite links for supergroups and channels, sorry!": "Я могу только дать вам ссылки на приглашения для супергрупп и каналов, извините!",
        "I don't have access to the invite link, try changing my permissions!": "У меня нет доступа к  пригласительной ссылке, попробуйте изменить мои разрешения!",
    #Info
        "I can't extract a user from this.": "Я не могу извлечь пользователя из этого.",
        "Nearly as powerful as my owner - so watch it.": "Почти такая же мощная, как мой владелец - так что смотрите.",
        "Not quite a sudo user, but can still gban you off the map.": "Не совсем пользователь sudo, но всё ещё могу глобально забанить вас.",
        "\nFirst Name: {}": "\nИмя: {}",
        "\nI'll save all the text I can, but if you want more, you'll have to ": "\nЯ сохраню весь текст, который смогу, но если вы хотите больше, вам придётся ",
        "\nLast Name: {}": "\nФамилия: {}",
        "\nPermanent user link: {}": "\nПостоянная ссылка пользователя: {}",
        "\nReason for last warn:\\n{}": "\nПричина последнего предупреждения:\\n{}",
        "\nThis person has been whitelisted! ": "\nЭтот человек был внесён в белый список! ",
        "\nThis person is one of my sudo users! ": "\nЭтот человек является одним из моих пользователей судо! ",
        "\nThis person is one of my support users! ": "\nЭтот человек является одним из моих пользователей поддержки! ",
        "\nUsername: @{}": "\\nИмя пользователя: @{}",
        "\nThis person is my owner -- I would never do anything against them!": "\nЭтот человек мой хозяин -- я бы никогда ничего против него не сделала!",
    #Locks
        "I see a bot, and I've been told to stop them joining... ": "Я вижу бота, и мне сказали прекратить их присоединение... ",
        "Just means that any restricted users should be manually unrestricted from the chat ": "Просто означает, что любые ограниченные пользователи должны вручную получить отмену ограничений в чате ",
        "Locked {} messages for all non-admins!": "Заблокировано {} сообщений для всех не админов!",#падежи
        "NOTE: due to a recent abuse of locking, {} will now only be deleting messages, and not ": "ПРИМЕЧАНИЕ: из-за недавнего злоупотребления блокировкой, {} теперь будет только удалять сообщения, а не ",
        #Unlock
        "What are you trying to unlock...?": "Что вы пытаетесь разблокировать...?",
        "What are you trying to unlock...? Try /locktypes for the list of lockables": "Что вы пытаетесь разблокировать...? Попробуйте /locktypes для списка блокируемых",
    #Misk
        "Its always banhammer time for me!": "Для меня это всегда время банхаммера!",
    #Kick
        "Kicked!": "Выгнан!",
        "Need to be inviter of a user to kick it from a basic group": "Необходимо быть приглашающим пользователя, чтобы выгнать его из основной группы",
        "Only the creator of a basic group can kick group administrators": "Только создатель основной группы может выгнать админов группы",
    #Other
        "Only admins are allowed to add bots to this chat! Get outta here.": "Только админы могут добавлять ботов в этот чат! Убирайся отсюда.",
    #AFK
        "{} is AFK!": "{} отошёл!",
        "{} is AFK! says its because of:\\n{}": "{} отошёл! говорит, это потому что:\\n{}",
    
    "That command can't be disabled": "Эту команду нельзя отключить",
    "That means I'm not allowed to ban/kick them.": "Это означает, что мне не разрешено банить/выгонять их.",
    "That's not a current filter -- run /filters for all active filters.": "Это не текущий фильтр -- запустите /filters для всех активных фильтров.",
    "That's not a current warning filter -- run /warnlist for all active warning filters.": "Это не текущий фильтр предупреждений -- запустите /warnlist для всех активных фильтров предупреждений.",
    "That's not a note in my database!": "Это не заметка в моей базе данных!",
    "The current warn limit is {}": "Текущий предел предупреждений {}",
    "The following commands are toggleable:\\n{}": "Следующие команды можно переключать:\\n{}",
    "The group admins haven't set any rules for this chat yet. ": "Админы группы ещё не установили никаких правил для этого чата. ",
    "The minimum warn limit is 3!": "Минимальный предел предупреждений -- 3!",
    "The original sender, {}, has an ID of `{}`.\\nThe forwarder, {}, has an ID of `{}`.": "Исходный отправитель, {}, имеет идентификатор `{}`.\\nПересылающий, {}, имеет идентификатор `{}`.",
    "The rules for *{}* are:\\n\\n{}": "Правила для *{}* следующие:\\n\\n{}",
    "The rules shortcut for this chat hasn't been set properly! Ask admins to ": "Ярлык правил для этого чата установлен неправильно! Попросите админов ",
    "There are `{}` custom filters here.": "Здесь есть `{}` пользовательских фильтров.", #падежи
    "There are `{}` notes in this chat.": "В этом чате `{}` заметок.",
    "There are no blacklisted messages here!": "Здесь нет сообщений из чёрного списка!",
    "There are no current locks in this chat.": "В этом чате нет текущих блокировок.",
    "There are {} blacklisted words.": "Есть {} слова из чёрного списка.",#падежи
    "There is no note message -- You can't JUST have buttons, you need a message to go with it!": "Нет сообщения-заметки -- Вы не можете ПРОСТО иметь кнопки, вам нужны сообщения для них!",
    "These are the locks in this chat:": "Это блокировки в этом чате:",
    "These files/photos failed to import due to originating ": "Эти файлы/фотографии не удалось импортировать из-за происхождения ",
    "This chat has `{}` warn filters. It takes `{}` warns ": "В этом чате есть `{}` фильтров предупреждений. Требуется `{}` предупреждений ", #падежи
    "This chat has had it's rules set: `{}`": "В этом чате установлены правила: `{}`",
    "This chat is setup to send user reports to admins, via /report and @admin: `{}`": "Этот чат настроен для отправки пользовательских отчётов админам через /report и @admin: `{}`",
    "This chat's current setting is: `{}`": "Текущая настройка этого чата: `{}`",
    "This group chat was deactivated!": "Этот групповой чат был отключён!",
    "This group's id is `{}`.": "Идентификатор этой группы `{}`.",
    "This isn't a blacklisted trigger...!": "Это не триггер из чёрного списка...!",
    "This message seems to have been lost - I'll remove it ": "Это сообщение, кажется, было потеряно - я удалю его ",
    "This note could not be sent, as it is incorrectly formatted. Ask in ": "Не удалось отправить эту заметку, так как она неправильно отформатирована. Спросите в ",
    "This note doesn't exist": "Этой заметки не существует",
    "This note was an incorrectly imported file from another bot -- I can't use ": "Эта заметка была неправильно импортированным файлом из другого бота -- я не могу использовать ",
    "This person CREATED the chat, how would I demote them?": "Этот человек создал чат, как бы я его понизила?",
    "This probably doesn't mean it's lawless though...!": "Это, вероятно, не означает, что это беззаконие, хотя ...!",
    "This user already has the right to speak.": "Этот пользователь уже имеет право говорить.",
    "This user has {}/{} warnings, for the following reasons:": "Этот пользователь имеет {}/{} предупреждений по следующим причинам:", #падежи
    "This user hasn't got any warnings!": "Этот пользователь не получил никаких предупреждений!",
    "This user is already muted!": "Этот пользователь уже приглушён!",
    "This user is not a participant of the chat!": "Этот пользователь не является участником чата!",
    "This user isn't even in the chat, unmuting them won't make them talk more than they ": "Этот пользователь даже не находится в чате, их приглушение не заставит их говорить больше, чем они ",
    "This user isn't in the chat!": "Этого пользователя нет в чате!",
    "Too many warns will now result in a ban!": "Слишком много предупреждений теперь приведёт к бану!",
    "Too many warns will now result in a kick! Users will be able to join again after.": "Слишком много предупреждений теперь приведет к вылету! Пользователи смогут присоединиться снова после.",
    "Turned off reporting! No admins will be notified on /report or @admin.": "Выключены пользовательские отчёты! Никакие админы не будут уведомлены при /report или @admin.",
    "Turned off reporting! You wont get any reports.": "Выключены пользовательские отчёты! Вы не получите никаких отчётов.",
    "Turned on reporting! Admins who have turned on reports will be notified when /report ": "Включены пользовательские отчёты! Админы, включившие отчёты, будут уведомлены, когда /report ",
    "Turned on reporting! You'll be notified whenever anyone reports something.": "Включены пользовательские отчёты! Вы будете уведомлены всякий раз, когда кто-нибудь сообщает что-то.",
    "Unlocked {} for everyone!": "Разблокирован {} для всех!", #окончание глагола
    "Unrecognised argument -- please use a number, 'off', or 'no'.": "Нераспознанный аргумент -- пожалуйста, используйте число, 'off' или 'no'.",
    "Unsupported url protocol": "Неподдерживаемый протокол URL",
    "Updated the warn limit to {}": "Обновлён предел предупреждений до {}",
    #куски ниже лучше переводить в контексте
    "User not found": "Пользователь не найден",
    "User_not_participant": "Пользователь не является участником",
        "Well damn, I can't ban that user.": "Чёрт возьми, я не могу забанить этого пользователя.",
    "Well damn, I can't kick that user.": "Чёрт возьми, я не могу выгнать этого пользователя.",
    "Well damn, I can't mute that user.": "Чёрт возьми, я не могу приглушить этого пользователя.",
    "Whadya want to delete?": "Что вы хотите удалить?",
    "What are you trying to lock...? Try /locktypes for the list of lockables": "Что вы хотите заблокировать...? Попробуйте /locktypes для списка блокируемых",
    "Why are you trying to unban someone that's already in the chat?": "Почему вы пытаетесь разбанить того, кто уже в чате",
    "Yas! Added replied message {}": "Да! Добавлено ответное сообщение {}",
    "Yas! Added {note_name}.\\nGet it with /get {note_name}, or #{note_name}": "Да! Добавлена заметка {note_name}.\\nПолучите её с помощью /get {note_name} или #{note_name}",
    "Yeahhh I'm not gonna do that": "Да я не собираюсь этого делать",
    "Yep, I'll stop replying to that.": "Да, я перестану на это отвечать.",
    "Yep, I'll stop warning people for that.": "Да, я перестану выносить людям предупреждения об этом.",
    "Yep, this user can join!": "Да, этот пользователь может присоединиться!",
    "You are *admin*: `{}`": "Вы *админ*: `{}`",
    "You can't save an empty message! If you added a button, you MUST ": "Вы не можете сохранять пустое сообщение! Если вы добавили кнопку, вы ДОЛЖНЫ ",
    "You didn't specify what to reply with!": "Вы не указали, чем отвечать!",
    "You don't seem to be referring to a chat.": "Кажется, вы не обращаетесь к чату.",
    "You don't seem to be referring to a chat/user.": "Кажется, вы не обращаетесь к чату/пользователю.",
    "You don't seem to be referring to a user.": "Кажется, вы не обращаетесь к пользователю.",
    "You haven't specified a time to ban this user for!": "Вы не указали время для бана этого пользователя!",
    "You haven't specified a time to mute this user for!": "Вы не указали время для приглушения этого пользователя!!",
    "You need to give me a notename to save this message!": "Вы должны дать мне имя заметки, чтобы сохранить это сообщение!",
    "You receive reports from chats you're admin in: `{}`.\\nToggle this with /reports in PM.": "Вы получаете отчёты из чатов, админом которых вы являетесь: `{}`.\\nПереключите это с помощью /reports в личку.",
    "You seem to be trying to use an unsupported url protocol. Telegram ": "Кажется, вы пытаетесь использовать неподдерживаемый протокол url. Телеграм ",
    "You'll need to either give me a username to mute, or reply to someone to be muted.": "Вам нужно будет либо дать мне имя пользователя для приглушения, либо ответить кому-то, кто будет приглушён.",
    "You'll need to either give me a username to unmute, or reply to someone to be unmuted.": "Вам нужно будет либо дать мне имя пользователя для снятия приглушения, либо ответить тому, кому оно будет снято.",
    "Your current report preference is: `{}`": "Ваши текущие настройки пользовательских отчётов: `{}`",
    "Your id is `{}`.": "Ваш id `{}`.",
    "admin pannel.": "админ-панель.",
    "again, or ask in @MarieSupport for help.": "снова или попросите помощи в @MarieSupport.",
    "already do!": "уже делаю!",
    "before the user gets *{}*.": "до того, как пользователь получит *{}*.",
    "bots can't forward bot messages, so I can't save the exact message. ": "боты не могут пересылать сообщения бота, поэтому я не могу сохранить точное сообщение. ",
    "but I'm not admin!": "но я не админ!",
    "disappointment. Get out.": "разочарование. Убирайся.",
    "doesn't support buttons for some protocols, such as tg://. Please try ": "не поддерживает кнопки для некоторых протоколов, таких как tg://. Пожалуйста, попробуйте ",
    "files with a different file_id, to avoid one bot accessing another's ": "файлы с другим file_id, чтобы избежать доступа одного бота к другому ",
    "files. Sorry for the inconvenience!": "файлы. Извините за неудобства!",
    "fix this.": "починить это",
    "forward the message yourself, and then save it.": "перешлите сообщение самостоятельно, а затем сохраните его.",
    "from another bot. This is a telegram API restriction - each bot sees ": "от другого бота. Это ограничение API телеграма - каждый бот видит ",
    "from your notes list.": "из вашего списка заметок.", #списка ваших заметок?
    "have some text in the message too.": "есть какой-то текст в сообщении тоже.",
    "interract with other bots, so I can't save this message ": "взаимодействовать с другими ботами, поэтому я не могу сохранить это сообщение ",
    "it. If you really need it, you'll have to save it again. In ": "это. Если оно вам действительно нужно, вам придётся сохранить его снова. В ",
    "like I usually would - do you mind forwarding it and ": "как я обычно делаю - Вы не могли бы переслать его и ",
    "message dump to avoid this. I'll remove this note from ": "дамп сообщений, чтобы избежать этого. Я удалю эту записку из ",
    "not have delete rights, or this might not be a supergroup.": "нет прав на удаление, или, может быть, это не супергруппа.",
    "or @admin are called.": "или @admin вызваны.",
    "restricting users via the tg api. This shouldn't affect all you users though, so dont worry! ": "ограничение пользователей через API тг. Это не должно повлиять на всех вас, пользователей, так что не волнуйтесь! ",
    "so were not removed.": "поэтому не были удалены.",
    "the meantime, I'll remove it from your notes list.": "тем временем, я удалю её из своего списка заметок.",
    "their message - sorry! Get your bot admin to start using a ": "их сообщение - извините! Заставьте вашего бота админа начать использовать ",
    "then saving that new message? Thanks!": "затем сохранить это новое сообщение? Спасибо!",
    "to tag them!": "чтобы пометить их!",
    "user, so I can't act upon them!": "пользователь, поэтому я не могу действовать на них!",
    "want to mention them, forward one of their messages to me, and I'll be able ": "хотите упомянуть их, перешлите мне одно из их сообщений, и я смогу ",
    
    
    "{} is calling for admins in \\": "{} зовёт админов в \\",
    "{} is no longer AFK!": "{} больше не AFK!",
    "{} is now AFK!": "{} теперь AFK!",
    "{} warnings, {} has been banned!": "{} предупреждений, {} забанен!",
    "{} warnings, {} has been kicked!": "{} предупреждений, {} выгнан!",
    "{}'s id is `{}`.": "ID {} `{}`.",

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
            #"Sed/Regex": "" #No need to translate this
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

#Some code for Russian
