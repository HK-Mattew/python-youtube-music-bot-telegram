from core.tools._tools import (
    remove_unnecessary_spaces_from_the_triple_string
    )




TEMPLATE_START = """
<b>
    🤗 Welcome, {user_first_name}!
</b>

<b>
    👇 Send me:
</b>
<i>
    » Song/video name or author to search for your song or video;
    » You can also send a youtube link;
</i>

<i>
    [Links]
    🔱 <a href="https://telega.io/catalog_bots/YouTubeMusicOfficialBot/card">Advertise in this bot</a>
    ⚙ <a href="https://github.com/HK-Mattew/">Developer</a>
</i>
"""


TEMPLATE_MEDIA_INFO = """
<b><a href="{url}">{title}</a></b>
👤 {author}
🕔 {duration}

Select download format/quality ↓
"""



_DATA = {
    'TEMPLATE_START': remove_unnecessary_spaces_from_the_triple_string(
        TEMPLATE_START
        ).replace('\n<', '<'),
    'TEMPLATE_MEDIA_INFO': remove_unnecessary_spaces_from_the_triple_string(
        TEMPLATE_MEDIA_INFO
        ).replace('\n<', '<'),
}