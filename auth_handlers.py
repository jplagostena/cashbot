import logging
import telegram_helper

from google_sheeter import GoogleAuth
from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update


ENTER_CODE = 0


def handler_auth(update: Update, context: CallbackContext):
    username = telegram_helper.get_username_from_update(update)
    logging.info("User %s starting auth.", username)
    auth = GoogleAuth(username)
    if auth.is_authorized():
        update.message.reply_text('El bot ya está autorizado!')
        return ConversationHandler.END
    url = auth.get_credential()
    update.message.reply_html('Si estás de acuerdo, por favor visita el <a href="' + url + '">enlace</a> y copia el código que te da Google')
    return ENTER_CODE


def handler_auth_code(update: Update, context: CallbackContext):
    username = telegram_helper.get_username_from_update(update)
    auth = GoogleAuth(username)
    code = update.message.text
    logging.info("user %s sent code %s", username, code)
    auth.get_credential(code=code)
    response_text = 'Autorización exitosa!'
    if not auth.is_authorized():
        response_text = 'Problemas con la autorización'
        logging.info('Problemas con la autorización de ' + username)

    update.message.reply_text(response_text)
    return ConversationHandler.END


def cancel_auth(bot, update):
    username = telegram_helper.get_username_from_update(update)
    logging.info("User %s canceled the auth.", username)