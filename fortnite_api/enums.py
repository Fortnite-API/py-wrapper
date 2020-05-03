from enum import Enum


class KeyFormat(Enum):
    HEX = 'hex'
    BASE64 = 'base64'


class GameLanguage(Enum):
    ARABIC = 'ar'
    GERMAN = 'de'
    ENGLISH = 'en'
    SPANISH = 'es'
    SPANISH_LATIN = 'es'
    FRENCH = 'fr'
    ITALIAN = 'it'
    JAPANESE = 'ja'
    KOREAN = 'ko'
    POLISH = 'pl'
    PORTUGUESE_BRASIL = 'pt-BR'
    RUSSIAN = 'ru'
    TURKISH = 'tr'
    CHINESE_SIMPLIFIED = 'zh-CN'
    CHINESE_TRADITIONAL = 'zh-Hant'


class MatchMethod(Enum):
    FULL = 'full'
    CONTAINS = 'contains'
    STARTS = 'starts'
    ENDS = 'ends'


class BrCosmeticRarity(Enum):
    FROZEN = 'frozen'
    LAVA = 'lava'
    LEGENDARY = 'legendary'
    DARK = 'dark'
    STARWARS = 'starwars'
    MARVEL = 'marvel'
    DC = 'dc'
    ICON_SERIES = 'icon'
    SHADOW = 'shadow'
    EPIC = 'epic'
    RARE = 'rare'
    UNCOMMON = 'uncommon'
    COMMON = 'common'


class BrCosmeticType(Enum):
    BANNER = 'banner'
    BACKPACK = 'backpack'
    CONTRAIL = 'contrail'
    OUTFIT = 'outfit'
    EMOTE = 'emote'
    EMOJI = 'emoji'
    GLIDER = 'glider'
    WRAP = 'wrap'
    LOADING_SCREEN ='loadingscreen'
    MUSIC ='music'
    PET ='pet'
    PICKAXE = 'pickaxe'
    SHOUT = 'shout'
    SPRAY = 'spray'
    TOY = 'toy'


class NewsType(Enum):
    BATTLE_ROYALE = 'br'
    SAVE_THE_WORLD = 'stw'
    CREATIVE = 'creative'