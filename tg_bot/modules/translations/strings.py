from tg_bot.modules.sql.translation import prev_locale
from tg_bot.modules.translations.English import EnglishStrings
from tg_bot.modules.translations.German import GermanStrings
from tg_bot.modules.translations.Dutch import DutchStrings
from tg_bot.modules.translations.Indonesian import IndonesianStrings
from tg_bot.modules.translations.Finnish import FinnishStrings
from tg_bot.modules.translations.BrPortuguese import BrPortugueseStrings
from tg_bot.modules.translations.Russian import RussianStrings

def tld(chat_id, t, show_none=True):
    LANGUAGE = prev_locale(chat_id)
    print(t)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('nl') and t in DutchStrings:
            return DutchStrings[t]
        elif LOCALE in ('de') and t in GermanStrings:
           return GermanStrings[t]
        elif LOCALE in ('id') and t in IndonesianStrings:
           return IndonesianStrings[t]
        elif LOCALE in ('fi') and t in FinnishStrings:
           return FinnishStrings[t]
        elif LOCALE in ('pt-br') and t in BrPortugueseStrings:
           return BrPortugueseStrings[t]
        elif LOCALE in ('ru') and t in RussianStrings:
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
    print(t)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('ru') and t.help in RussianStrings:
           return RussianStrings[t.help]
        else:
            return t
    elif show_none:
        return t