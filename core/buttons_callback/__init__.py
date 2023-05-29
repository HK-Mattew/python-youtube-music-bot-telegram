from telegram.ext import (
    CallbackContext,
    ConversationHandler
)
from telegram import Update
from .media_info import media_info
from .listenyt import get_media_video, get_media_audio




def buttons_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    if not user or (user and user.is_bot):return ConversationHandler.END


    if query.data.startswith('media-info='):
        query.answer('🔃 Loading...')
        # query.message.delete()
        return media_info(update, context)
    
    elif query.data.startswith('media-download='):
        query.answer()
        params_str = query.data.split('media-download=')[1].split('?')[1]
        params = dict(
            (
                x.split('=')
                if not x.startswith('?')
                else x.replace('?', '').split('=')
            )
            for x in params_str.split('&')
            )
        if params['t'] == 'v':#Video
            return get_media_video(update, context, params)

        if params['t'] == 'a':#Audio
            return get_media_audio(update, context, params)




    elif query.data == 'video-format':
        query.answer('Select the video format below ⬇')
        return

    elif query.data == 'audio-format':
        query.answer('Select the audio/music format below ⬇')
        return