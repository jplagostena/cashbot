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


class TestConfig(Config):
    SPREADSHEET_ID = 'an_id_for_tests'
    SHEET_TITLE = 'Sheet_Test'
    BOT_TOKEN = 'a_bot_token'
    CATEGORIES = ('cat1', 'cat2', 'cat3')
    ENABLED_USERS = [('telegram1', 'name1'), ('telegram2', 'name2')]


devConfig = DevConfig()


class ProdConfig(Config):
    pass


prodConfig = ProdConfig()

configs = {
    'prod': ProdConfig(),
    'dev': DevConfig(),
    'test': TestConfig()
}

config = configs[env]





