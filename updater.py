import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import expenditure_handlers
import auth_handlers
from config import config
from error_handler import error_callback

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(token=config.BOT_TOKEN)


def main():
    logger.info("Construyendo handlers")
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('gasto', expenditure_handlers.handler_gasto)],

        states={
            expenditure_handlers.CATEGORY: [CallbackQueryHandler(expenditure_handlers.handler_category)],

            expenditure_handlers.AMOUNT: [MessageHandler(Filters.text, expenditure_handlers.handler_amount),
                                          CommandHandler('cancelar', expenditure_handlers.cancel)],

            expenditure_handlers.DESCRIPTION: [MessageHandler(Filters.text, expenditure_handlers.handler_description),
                                               CommandHandler('cancelar', expenditure_handlers.cancel)],
        },

        fallbacks=[CommandHandler('cancelar', expenditure_handlers.cancel)]
    )

    auth_conversation_handler = ConversationHandler(entry_points=[CommandHandler('autorizar', auth_handlers.handler_auth)],
                                                    states={
                                                        auth_handlers.ENTER_CODE: [MessageHandler(
                                                            Filters.all,
                                                            auth_handlers.handler_auth_code
                                                        )]
                                                    },
                                                    fallbacks=[CommandHandler('cancelar', auth_handlers.cancel_auth)],
                                                    conversation_timeout=60)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(auth_conversation_handler)
    dispatcher.add_error_handler(error_callback)

    logger.info("Iniciando Updater")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
