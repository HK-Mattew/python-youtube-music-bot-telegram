from unittest.util import strclass
from core.templates import get_template
from telegram.ext import (
    CallbackContext
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update)
from splitty import chunks
import pafy

ydl_opts = {
    # 'format': 'bestaudio/best',
    # 'outtmpl': file_name,
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'http_persistent': False,
    'cookiefile': 'cookies.txt',
    'verbose': True
}


def media_info(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user or (user and user.is_bot):return
    user_language_code = update.effective_user.language_code


    media_id = query.data.split('media-info=')[1]
    video = pafy.new(media_id, ydl_opts=ydl_opts)
    title = video.title
    url = video.watchv_url
    duration = video.duration
    author = video.author
    thumb_url = video.bigthumb
    streams = {
        'video': {},
        'audio': {}
    }
    video_keyboard = []
    audio_keyboard = []
    #strems video
    for stream_video in video.streams:
        streams['video'][stream_video.resolution] = {
            'url': stream_video.url,
            'size': stream_video.get_filesize()
        }
        video_keyboard.append(
            InlineKeyboardButton(
                text=f'{stream_video.resolution}',
                callback_data=f'media-download={media_id}?t=v&ql={stream_video.resolution}'
            )
        )
    #strems audio
    for stream_audio in video.audiostreams:
        streams['audio'][stream_audio.bitrate] = {
            'url': stream_audio.url,
            'size': stream_audio.get_filesize()
        }
        audio_keyboard.append(
            InlineKeyboardButton(
                text=f'{stream_audio.bitrate.upper() + "bps"}',
                callback_data=f'media-download={media_id}?t=a&ql={stream_audio.bitrate}'
            )
        )

    keyboard = []
    if audio_keyboard:
        keyboard.append([
            InlineKeyboardButton('⬇ [Audio/Music] Formats', callback_data='audio-format')
        ])
        for audio_keyboard_row in chunks(audio_keyboard, 3):
            keyboard.append(audio_keyboard_row)

    if video_keyboard:
        keyboard.append([
            InlineKeyboardButton('⬇ [Video] Formats', callback_data='video-format')
        ])
        for video_keyboard_row in chunks(video_keyboard, 3):
            keyboard.append(video_keyboard_row)


    text_template = get_template(
        template='TEMPLATE_MEDIA_INFO',
        params={
            'title': title,
            'url': url,
            'duration': duration,
            'author': author
        }
    )

    if thumb_url:
        context.bot.send_photo(
            chat_id=chat_id,
            photo=thumb_url,
            caption=text_template,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=text_template,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    







