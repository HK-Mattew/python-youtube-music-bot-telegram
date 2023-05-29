from telegram.ext import Updater
from config import Config


def get_bot_instance(bot_token):
    return Updater(bot_token).bot



def send_media_to_database_channel_on_telegram(media_type, media_path, media_title=None):
    BOT = get_bot_instance(Config.BOT_TOKEN)
    CHAT_ID = ('@'+ Config.TELEGRAM_CHANNEL_MEDIA_DB
            if not Config.TELEGRAM_CHANNEL_MEDIA_DB.startswith('@')
            else
            Config.TELEGRAM_CHANNEL_MEDIA_DB)

    if media_type == 'video':
        with open(media_path, 'rb') as filedata:
            tgmedia = BOT.send_video(
                chat_id=CHAT_ID,
                video=filedata,
                caption=f"{BOT.first_name}: @{BOT.username}"
            )
    elif media_type == 'audio':
        with open(media_path, 'rb') as filedata:
            tgmedia = BOT.send_audio(
                chat_id=CHAT_ID,
                audio=filedata,
                title=media_title,
                caption=f"{BOT.first_name}: @{BOT.username}"
            )
    
    return tgmedia