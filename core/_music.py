from telegram.ext import (
    CallbackContext
    )
from telegram import (
    ReplyKeyboardMarkup,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    )
from core.tools._youtube import Music
from splitty import chunks



def music(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if not user or (user and user.is_bot):return
    chat_id = update.effective_chat.id
    # user_language_code = user.language_code


    if not context.args:
        input_text = update.message.text
    else:
        input_text = ' '.join(context.args)

    mus = Music()
    data = mus.search_music(input_text, limit=10)
    result_count = len(data['result'])

    keyboard = []

    for index in range(0, result_count):
        call_data = f'media-info={mus.get_id(data, index)}'
        keyboard.append(
            InlineKeyboardButton(text=f'» {mus.get_title(data, index)}', callback_data=call_data)
        )

    
    context.bot.send_message(
        chat_id=chat_id,
        text=f'🔎 Results for: {input_text}',
        reply_markup=InlineKeyboardMarkup(chunks(keyboard, 1))
    )

    # duration = mus.get_duration(result)

    # if duration['hours'] == 0 or (duration['hours'] <= 1 and duration['minutes'] <= 30):
    #     context.bot.send_message(
    #         chat_id=chat_id,
    #         text=f"🎵 {mus.get_title(result)}\n🔗 {mus.get_link(result)}",
    #         reply_markup=InlineKeyboardMarkup(
    #             [
    #                 [
    #                     InlineKeyboardButton('✅ Click here to listen to this song', callback_data=f'listen-yt={mus.get_link(result).split("https://www.youtube.com/watch?v=")[1]}')
    #                 ]
    #             ]
    #         )
    #         )
    # else:
    #     return context.bot.send_message(
    #         chat_id=chat_id,
    #         text='❌ This song is too big, try another one(The music must have a maximum of 1 hour and 30 minutes).'
    #         )