from datetime import datetime
import sys
from telegram.ext import (
    CallbackContext
)
from telegram import (
    Update,
    ChatAction
    )
from core.tools._tools import remove_special_characters
from core import medias
from config import Config
import random, os
import pafy
from core.tools._telegram import send_media_to_database_channel_on_telegram


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


def get_media_video(update: Update, context: CallbackContext, params):
    query = update.callback_query
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user or (user and user.is_bot):return
    user_language_code = update.effective_user.language_code

    query.message.delete()


    media_id = query.data.split('media-download=')[1].split('?')[0]
    media_type = params['t'].replace(
        'v', 'video', 1
        ).replace(
            'a', 'audio', 1
        )
    db_media_found = medias.find_one({
        'media_id': media_id,
        'media_type': media_type,
        'media_quality': params['ql']
    })


    if not db_media_found:
        video = pafy.new(media_id, ydl_opts=ydl_opts)

        media_title = video.title
        media_duration = video.duration
        media_thumb = video.bigthumb
        media_url = video.watchv_url
        streams = {
            'video': {},
            'audio': {}
        }
        streams_objects = {
            'video': {},
            'audio': {}
        }
        #strems video
        for stream_video in video.streams:
            streams['video'][stream_video.resolution] = {
                'url': stream_video.url,
                'extension': stream_video.extension,
                'size': stream_video.get_filesize()
            }
            streams_objects['video'][stream_video.resolution] = {
                'stream_obj': stream_video
            }
        #strems audio
        for stream_audio in video.audiostreams:
            streams['audio'][stream_audio.bitrate] = {
                'url': stream_audio.url,
                'extension': stream_audio.extension,
                'size': stream_audio.get_filesize()
            }
            streams_objects['audio'][stream_video.resolution] = {
                'stream_obj': stream_audio
            }

        
        stream = streams['video'].get(params['ql'])
        stream_object = streams_objects['video'].get(params['ql'])['stream_obj']
        if not stream:
            return context.bot.send_message(
                chat_id=chat_id,
                text='Sorry, the specified quality could not be obtained.'
                )


        file_path = (f'{Config.DOWNLOAD_PATH}/' + remove_special_characters(media_title) +f'-@{context.bot.username}-'+str(random.randint(0,999999))+f'.{stream["extension"]}').replace('  ', ' ').replace(' ', '-')
        downloading_message = context.bot.send_message(
            chat_id=chat_id,
            text=f"⬇️ Downloading...(this may take a while.)"
            )

        
        def run_asyn_download(*args, **kwargs):
            try:
                stream_object.download(filepath=file_path)
            except Exception as err:
                print(err, file=sys.stderr)
                return context.bot.send_message(
                    chat_id=chat_id,
                    text='🙁 Sorry, this video could not be downloaded.'
                    )

            try:
                tgmedia = send_media_to_database_channel_on_telegram(
                    media_type=media_type,
                    media_path=file_path,
                    media_title=media_title
                )

                context.bot.send_chat_action(
                    chat_id=chat_id,
                    action=ChatAction.UPLOAD_VIDEO
                )

                context.bot.send_video(
                    chat_id=chat_id,
                    video=tgmedia.video.file_id,
                    caption="✅ Here's your video ;)"
                )
                medias.insert_one({
                    'media_id': media_id,
                    'media_type': media_type,
                    'media_title': media_title,
                    'media_duration': media_duration,
                    'media_thumb': media_thumb,
                    'media_url': media_url,
                    'media_quality': params['ql'],
                    'media_streams': streams,
                    'media_tg_file_id': tgmedia.video.file_id,
                    'created_in': datetime.utcnow()
                })

                downloading_message.delete()
            except:
                print("\nError")

            os.remove(file_path)
        
        context.job_queue.run_once(run_asyn_download, when=1)
    else:
        context.bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.UPLOAD_VIDEO
        )
        context.bot.send_video(
            chat_id=chat_id,
            video=db_media_found['media_tg_file_id'],
            caption="✅ Here's your video ;)"
        )



def get_media_audio(update: Update, context: CallbackContext, params):
    query = update.callback_query
    chat_id = update.effective_chat.id
    user = update.effective_user
    if not user or (user and user.is_bot):return
    user_language_code = update.effective_user.language_code

    query.message.delete()

    media_id = query.data.split('media-download=')[1].split('?')[0]
    media_type = params['t'].replace(
        'v', 'video', 1
        ).replace(
            'a', 'audio', 1
        )
    db_media_found = medias.find_one({
        'media_id': media_id,
        'media_type': media_type,
        'media_quality': params['ql']
    })



    if not db_media_found:
        video = pafy.new(media_id, ydl_opts=ydl_opts)
        media_title = video.title
        media_duration = video.duration
        media_thumb = video.bigthumb
        media_url = video.watchv_url

        streams = {
            'video': {},
            'audio': {}
        }
        streams_objects = {
            'video': {},
            'audio': {}
        }
        #strems video
        for stream_video in video.streams:
            streams['video'][stream_video.resolution] = {
                'url': stream_video.url,
                'extension': stream_video.extension,
                'size': stream_video.get_filesize()
            }
            streams_objects['video'][stream_video.resolution] = {
                'stream_obj': stream_video
            }
        #strems audio
        for stream_audio in video.audiostreams:
            streams['audio'][stream_audio.bitrate] = {
                'url': stream_audio.url,
                'extension': stream_audio.extension,
                'size': stream_audio.get_filesize()
            }
            streams_objects['audio'][stream_audio.bitrate] = {
                'stream_obj': stream_audio
            }

        
        stream = streams['audio'].get(params['ql'])
        stream_object = streams_objects['audio'].get(params['ql'])['stream_obj']
        if not stream:
            return context.bot.send_message(
                chat_id=chat_id,
                text='Sorry, the specified quality could not be obtained.'
                )


        file_path = (f'{Config.DOWNLOAD_PATH}/' + remove_special_characters(media_title) +f'-@{context.bot.username}-'+str(random.randint(0,999999))+f'.{stream["extension"]}').replace('  ', ' ').replace(' ', '-')
        downloading_message = context.bot.send_message(
            chat_id=chat_id,
            text=f"⬇️ Downloading...(this may take a while.)"
            )

        
        def run_asyn_download(*args, **kwargs):
            try:
                stream_object.download(filepath=file_path)
            except Exception as err:
                print(err, file=sys.stderr)
                return context.bot.send_message(
                    chat_id=chat_id,
                    text='🙁 Sorry, this song could not be downloaded.'
                    )

            try:
                tgmedia = send_media_to_database_channel_on_telegram(
                    media_type=media_type,
                    media_path=file_path,
                    media_title=media_title
                )
                context.bot.send_chat_action(
                    chat_id=chat_id,
                    action=ChatAction.UPLOAD_AUDIO
                )
                context.bot.send_audio(
                    chat_id=chat_id,
                    audio=tgmedia.audio.file_id,
                    title=media_title,
                    caption="✅ Here's your audio/music ;)"
                )
                medias.insert_one({
                    'media_id': media_id,
                    'media_type': media_type,
                    'media_title': media_title,
                    'media_duration': media_duration,
                    'media_thumb': media_thumb,
                    'media_url': media_url,
                    'media_quality': params['ql'],
                    'media_streams': streams,
                    'media_tg_file_id': tgmedia.audio.file_id,
                    'created_in': datetime.utcnow()
                })

                downloading_message.delete()
            except Exception as err:
                print("\nError =>", err)

            os.remove(file_path)

        context.job_queue.run_once(run_asyn_download, when=1)
    else:
        context.bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.UPLOAD_AUDIO
        )
        context.bot.send_audio(
            chat_id=chat_id,
            audio=db_media_found['media_tg_file_id'],
            title=db_media_found['media_title'],
            caption="✅ Here's your audio/music ;)"
        )
