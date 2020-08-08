import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error_callback(bot, update, error):
    logger.warning('Update "%s" causó el error "%s"', update, error)
    update.message.reply_text("Uy! Algo anduvo mal. Decile a tu admin que mire los logs 🤷")