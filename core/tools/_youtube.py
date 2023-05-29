import youtube_dl
from youtubesearchpython import VideosSearch



class Music:
    def __init__(self):
        pass

    def search_music(self, user_input, limit=1):
        return VideosSearch(user_input, limit=limit).result()

    def get_id(self, result, index=0):
        return result['result'][index]['id']

    def get_link(self, result, index=0):
        return result['result'][index]['link']

    def get_title(self, result, index=0):
        return result['result'][index]['title']

    def get_author(self, result, index=0):
        return result['result'][index]['author']

    def get_duration(self, result, index=0):
        result = result['result'][index]['duration'].split(':')
        split_count = len(result)
        duration = {
            'hours': 0,
            'minutes': 0,
            'seconds': 0
        }
        if split_count == 2:
            duration['minutes'] = int(result[0])
            duration['seconds'] = int(result[1])
        elif split_count == 3:
            duration['hours'] = int(result[0])
            duration['minutes'] = int(result[1])
            duration['seconds'] = int(result[2])
        
        return duration

    def download_music(self, file_name, link):
        # ydl_opts = {
        #     'outtmpl': file_name,
        #     'format': 'bestaudio/best',
        #     'postprocessors': [{
        #         'key': 'FFmpegExtractAudio',
        #         'preferredcodec': 'mp3',
        #         'preferredquality': '192',
        #     }],
        #     'prefer_ffmpeg': True
        # }
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_name,
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

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        pass