import logging

from telegram.ext import CallbackContext
from telegram import Update

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error_callback(update: object, context: CallbackContext):
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    logger.warning('Update "%s" causó el error "%s"', update_str, context.error)
    update.message.reply_text("Uy! Algo anduvo mal. Si ves que algo funciona mal, decile a tu admin que mire los logs 🤷")