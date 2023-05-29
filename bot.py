from distutils.command.config import config
import os
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters
)
from config import Config
from core import (
    start,
    music
    )
from core.buttons_callback import buttons_callback
import warnings
warnings.filterwarnings("ignore")


if not os.path.exists(Config.DOWNLOAD_PATH):
    os.mkdir(Config.DOWNLOAD_PATH)


def main() -> None:

    TOKEN = (
        Config.BOT_TOKEN
        if not Config.BOT_DEV
        else
        Config.BOT_DEV_TOKEN
        )
    updater = Updater(TOKEN, workers=8, use_context=True)
    dispatcher = updater.dispatcher


    from core.convs.convs_admin import admin_conv_handler
    dispatcher.add_handler(admin_conv_handler, group=1)

    dispatcher.add_handler(CommandHandler(
        'start',
        start,
        filters=(Filters.chat_type.private & ~(Filters.update.edited_message)),
        run_async=True
    ),
        group=1
    )
    dispatcher.add_handler(CommandHandler(
        'music',
        music,
        filters=(Filters.chat_type.private & ~(Filters.update.edited_message)),
        pass_args=True,
        run_async=True
    ),
        group=1
    )
    dispatcher.add_handler(MessageHandler(
        filters=(
            Filters.text & Filters.chat_type.private & ~(Filters.update.edited_message)
            ),
        callback=music,
        run_async=True
    ),
        group=1
    )

    dispatcher.add_handler(
        CallbackQueryHandler(
            buttons_callback,
            run_async=True
        )
    )

    updater.start_polling()

    print(f'Bot: @{updater.bot.username} started!')
    updater.idle()


if __name__ == '__main__':
    main()
