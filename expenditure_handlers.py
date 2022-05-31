import logging
from typing import Any, Dict
import telegram_helper

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler
from config import config
from google_sheeter import GoogleAuth, GoogleSheeter

CATEGORY_COLUMNS = 3
CURRENT_EXPENDITURES: Dict[str, Any] = {}
CATEGORY, AMOUNT, DESCRIPTION = range(3)


def get_username_from_tuple(tuple):
    return tuple[0]


def get_enabled_usernames():
    return list(map(get_username_from_tuple, config.ENABLED_USERS))


def handler_gasto(update: Update, context: CallbackContext):
    username = telegram_helper.get_username_from_update(update)
    auth = GoogleAuth(username)
    logging.info("User %s starting conversation.", username)
    
    msg = update.message
    if msg is None:
        raise ValueError("message no puede ser None en el update")

    if username not in get_enabled_usernames():
        msg.reply_text('No estás habilitado para usar esto!')
        return
    
    if not auth.is_authorized():
        logging.info("User %s needs to authorize this bot in its Google Account", username)
        msg.reply_text('Necesitas autorizar el bot antes. Corré el comando /autorizar')
        return

    if username in CURRENT_EXPENDITURES:
        msg.reply_text('Tenías un gasto a medio cargar, se descarta el gasto anterior')

    CURRENT_EXPENDITURES[username] = {}

    keyboard_opts = get_categories_keyboard()

    reply_markup = InlineKeyboardMarkup(keyboard_opts)
    msg.reply_text('Categoria?', reply_markup=reply_markup)

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
    if query is not None:
        category = query.data
        username = telegram_helper.get_username_from_update(update)
        CURRENT_EXPENDITURES[username]['category'] = category
        if query.message is not None:
            query.message.reply_text(text="Monto?")
        return AMOUNT


def handler_amount(update: Update, context: CallbackContext):
    msg = update.message
    if msg is None:
        raise ValueError("message no puede ser None en el update")
        
    amount = msg.text
    if amount is None:
        raise ValueError("Amount no puede ser nulo")

    # reemplazamos , por ., para validar el float. Si, no es la mejor manera de trabajar con formatos numéricos, pero...
    amount_to_validate = amount.replace(",", ".")
    if not telegram_helper.is_float(amount_to_validate):
        msg.reply_text("El valor no parece numérico. Ponete los lentes 🤓")
        return AMOUNT
    CURRENT_EXPENDITURES[telegram_helper.get_username_from_update(update)]['amount'] = amount
    
    msg.reply_text("Ingresá descripción")

    return DESCRIPTION


def handler_description(update: Update, context: CallbackContext):
    msg = update.message
    if msg is None:
        raise ValueError("message no puede ser None en el update")

    description = msg.text
    username = telegram_helper.get_username_from_update(update)

    CURRENT_EXPENDITURES[username]['description'] = description
    update_sheet(username, CURRENT_EXPENDITURES)
    del CURRENT_EXPENDITURES[username]
    msg.reply_text("Gasto cargado!")

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    msg = update.message
    if msg is None:
        raise ValueError("message no puede ser None en el update")
    username = telegram_helper.get_username_from_update(update)
    
    logging.info("User %s canceled the conversation.", username)
    del CURRENT_EXPENDITURES[username]
    msg.reply_text("Carga cancelada")
    
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

