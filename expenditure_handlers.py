import logging
import config
import telegram_helper

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler
from config import config
from google_sheeter import GoogleAuth, GoogleSheeter

CATEGORY_COLUMNS = 3
CURRENT_EXPENDITURES = {}
CATEGORY, AMOUNT, DESCRIPTION = range(3)


def get_username_from_tuple(tuple):
    return tuple[0]


def get_enabled_usernames():
    return list(map(get_username_from_tuple, config.ENABLED_USERS))


def handler_gasto(update: Update, context: CallbackContext):
    username = telegram_helper.get_username_from_update(update)
    auth = GoogleAuth(username)
    logging.info("User %s starting conversation.", username)

    if not auth.is_authorized():
        logging.info("User %s needs to authorize this bot in its Google Account", username)
        update.message.reply_text('Necesitas autorizar el bot antes. Corré el comando /autorizar')
        return

    if username not in get_enabled_usernames():
        update.message.reply_text('No estás habilitado para usar esto!')
        return

    if username in CURRENT_EXPENDITURES:
        update.message.reply_text('Tenías un gasto a medio cargar, se descarta el gasto anterior')

    CURRENT_EXPENDITURES[username] = {}

    keyboard_opts = get_categories_keyboard()

    reply_markup = InlineKeyboardMarkup(keyboard_opts)
    update.message.reply_text('Categoria?', reply_markup=reply_markup)
    return CATEGORY


def get_categories_keyboard():
    keyboard_opts = []
    keyboard_opt_row = []
    idx = 0
    for category in config.CATEGORIES:
        keyboard_opt_row.append(InlineKeyboardButton(category, callback_data=category))
        idx = idx + 1
        if idx == CATEGORY_COLUMNS:
            keyboard_opts.append(keyboard_opt_row)
            keyboard_opt_row = []
            idx = 0
    if idx != CATEGORY_COLUMNS:
        keyboard_opts.append(keyboard_opt_row)
    return keyboard_opts


def handler_category(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data
    username = telegram_helper.get_username_from_update(update)
    CURRENT_EXPENDITURES[username]['category'] = category
    query.message.reply_text(text="Monto?")
    return AMOUNT


def handler_amount(update: Update, context: CallbackContext):
    amount = update.message.text
    # reemplazamos , por ., para validar el float. Si, no es la mejor manera de trabajar con formatos numéricos, pero...
    amount_to_validate = amount.replace(",", ".")
    if not telegram_helper.is_float(amount_to_validate):
        update.message.reply_text("El valor no parece numérico. Ponete los lentes 🤓")
        return AMOUNT
    CURRENT_EXPENDITURES[telegram_helper.get_username_from_update(update)]['amount'] = amount
    update.message.reply_text("Ingresá descripción")

    return DESCRIPTION


def handler_description(update: Update, context: CallbackContext):
    description = update.message.text
    username = telegram_helper.get_username_from_update(update)

    CURRENT_EXPENDITURES[username]['description'] = description
    update_sheet(username, CURRENT_EXPENDITURES)
    del CURRENT_EXPENDITURES[username]
    update.message.reply_text("Gasto cargado!")

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    username = telegram_helper.get_username_from_update(update)
    logging.info("User %s canceled the conversation.", username)
    del CURRENT_EXPENDITURES[username]
    update.message.reply_text("Carga cancelada")
    return ConversationHandler.END


def update_sheet(username, expenditure_dict):
    """
    :param username: username de telegram
    :param expenditure_dict: diccionario que tiene tres partes
    'category' -> string
    'amount' -> float
    'description' -> string
    :return:
    """
    auth = GoogleAuth(username)
    sheeter = GoogleSheeter(username, auth.get_credential())
    sheeter.update_sheet(username, expenditure_dict)
    logging.info("Gasto cargado. Datos: %s"%(str(expenditure_dict)))

