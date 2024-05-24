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
    OUTFIT = 'outfit'
    BACKPACK = 'backpack'
    PET = 'pet'
    PET_CARRIER = 'petcarrier'
    PICKAXE = 'pickaxe'
    GLIDER = 'glider'
    CONTRAIL = 'contrail'
    AURA = 'aura'

    EMOTE = 'emote'
    EMOJI = 'emoji'
    SPRAY = 'spray'
    TOY = 'toy'

    WRAP = 'wrap'

    BANNER = 'banner'
    MUSIC = 'music'
    LOADING_SCREEN = 'loadingscreen'

    GUITAR = 'guitar'
    BASS = 'bass'
    DRUMS = 'drum'
    MICROPHONE = 'mic'
    KEYTAR = 'keyboard'

    CAR_BODY = 'body'
    DECAL = 'skin'
    WHEELS = 'wheel'
    TRAIL = 'drifttrail'
    BOOST = 'booster'

    JAM_TRACK = 'track'

    LEGO_BUILD = 'legoset'
    LEGO_DECOR_BUNDLE = 'legoprop'

    SHOUT = 'shout'
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
    SMALL = 'Size_1_x_1'
    NORMAL = 'Size_1_x_2'
    DOUBLE_WIDE = 'Size_2_x_2'
    TRIPLE_WIDE = 'Size_3_x_2'
    QUAD_WIDE = 'Size_4_x_2'
    PENTA_WIDE = 'Size_5_x_2'


class CosmeticCompatibleMode(Enum):
    ALL = 'ECosmeticCompatibleMode::MAX'
    BATTLE_ROYALE = 'ECosmeticCompatibleMode::BattleRoyale'
    LEGO = 'ECosmeticCompatibleMode::Juno'
    ROCKET_RACING = 'ECosmeticCompatibleMode::DelMar'
    FESTIVAL = 'ECosmeticCompatibleMode::Sparks'
