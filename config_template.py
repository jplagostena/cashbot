import os

env = os.getenv('BOT_ENV', 'dev')


class Config(object):
    """
     Completar con los datos de configuración reales y renombrar
     el archivo como config.py
    """
    SPREADSHEET_ID = 'GOOGLE_SPREADSHEET_ID'
    SHEET_TITLE = 'SHEET TITLE IN THE SPREADSHEET'
    BOT_TOKEN = 'TELEGRAM BOT TOKEN'
    CATEGORIES = ('Your', 'categories', 'here')
    ENABLED_USERS = [('telegram-handle1', 'NameToShowInTheSheet1'), ('telegram-handle-2', 'NameToShowInTheSheet2')]


class DevConfig(Config):
    pass


devConfig = DevConfig()


class ProdConfig(Config):
    pass


prodConfig = ProdConfig()

configs = {
    'prod': prodConfig,
    'dev': devConfig,
}

config = configs[env]





