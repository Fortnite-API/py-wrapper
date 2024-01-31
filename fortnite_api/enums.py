from enum import Enum


class KeyFormat(Enum):
    HEX = 'hex'
    BASE64 = 'base64'


class GameLanguage(Enum):
    ARABIC = 'ar'
    GERMAN = 'de'
    ENGLISH = 'en'
    SPANISH = 'es'
    SPANISH_LATIN = 'es-419'
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
    GAMING_LEGENDS = 'gaminglegends'
    DARK = 'dark'
    STARWARS = 'starwars'
    MARVEL = 'marvel'
    DC = 'dc'
    ICON_SERIES = 'icon'
    SHADOW = 'shadow'
    SLURP = 'slurp'
    EPIC = 'epic'
    LAMBORGHINI = 'lamborghini'
    RARE = 'rare'
    UNCOMMON = 'uncommon'
    COMMON = 'common'
    UNKNOWN = 'unknown'


class BrCosmeticType(Enum):
    BANNER = 'banner'
    BACKPACK = 'backpack'
    CONTRAIL = 'contrail'
    OUTFIT = 'outfit'
    EMOTE = 'emote'
    EMOJI = 'emoji'
    GLIDER = 'glider'
    WRAP = 'wrap'
    LOADING_SCREEN = 'loadingscreen'
    MUSIC = 'music'
    PET = 'pet'
    PET_CARRIER = 'petcarrier'
    PICKAXE = 'pickaxe'
    SHOUT = 'shout'
    SPRAY = 'spray'
    TOY = 'toy'
    AURA = 'aura'

    CAR_BODY = 'body'
    DECAL = 'skin'
    WHEELS = 'wheel'
    TRAIL = 'drifttrail'

    JAM_TRACK = 'track'
    GUITAR = 'guitar'
    BASS = 'bass'
    DRUMS = 'drum'
    MICROPHONE = 'mic'
    KEYTAR = 'keyboard'

    UNKNOWN = 'unknown'


class NewsType(Enum):
    BATTLE_ROYALE = 'br'
    SAVE_THE_WORLD = 'stw'
    CREATIVE = 'creative'


class AccountType(Enum):
    EPIC = 'epic'
    PSN = 'psn'
    XBL = 'xbl'


class TimeWindow(Enum):
    SEASON = 'season'
    LIFETIME = 'lifetime'


class StatsImageType(Enum):
    ALL = 'all'
    KEYBOARD_MOUSE = 'keyboardMouse'
    GAMEPAD = 'gamepad'
    TOUCH = 'touch'
    NONE = 'none'


class ShopTileSize(Enum):
    SMALL = 'Small'
    NORMAL = 'Normal'
    DOUBLE_WIDE = 'DoubleWide'
    TRIPLE_WIDE = 'TripleWide'


class CosmeticCompatibleMode(Enum):
    BATTLE_ROYALE = 'ECosmeticCompatibleMode::BattleRoyale'
    LEGO = 'ECosmeticCompatibleMode::Juno'
    ROCKET_RACING = 'ECosmeticCompatibleMode::DelMar'
