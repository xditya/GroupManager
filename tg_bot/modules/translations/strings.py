from tg_bot.modules.sql.translation import prev_locale
from tg_bot.modules.translations.English import EnglishStrings
from tg_bot.modules.translations.Russian import RussianStrings

def tld(chat_id, t, show_none=True):
    LANGUAGE = prev_locale(chat_id)
    print(t)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('ru') and t in RussianStrings:
           return RussianStrings[t]
        else:
            if t in EnglishStrings:
                return EnglishStrings[t]
            else:
                return t
    elif show_none:
        if t in EnglishStrings:
            return EnglishStrings[t]
        else:
            return t



def tld_help(chat_id, t):
    LANGUAGE = prev_locale(chat_id)
    print("tld_help ", t)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name

        t = t + "_help"

        print("Test2", t)

        if LOCALE in ('ru') and t in RussianStrings:
            return RussianStrings[t]
        else:
            return False
    else:
        return False