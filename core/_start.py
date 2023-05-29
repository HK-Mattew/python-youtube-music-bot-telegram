from datetime import datetime
from telegram.ext import CallbackContext
from telegram import (
    Update,
    ParseMode
    )
import telegram
from core.templates import get_template
from core import users


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):return
    chat_id = update.effective_chat.id
    # user_language_code = user.language_code

    user_db = users.find_one({'user_id': user.id})
    if not user_db:
        users.insert_one({
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language': user.language_code,
            'registered_in': datetime.utcnow()
        })


    html_text = get_template(
        template='TEMPLATE_START',
        params={
            'user_first_name': user.first_name.title()
        }
    )

    try:
        context.bot.send_message(
            chat_id=chat_id,
            text=html_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
            )
    except telegram.error.Unauthorized:
        pass