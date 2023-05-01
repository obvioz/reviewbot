import json
from typing import Optional

import aiohttp

from config import API
from database import DB, Photos


async def get_photo_file_path(photo):
    link = f"https://api.telegram.org/bot{API}/getFile?file_id={photo}"
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            html = await response.text()
            return json.loads(html)["result"]['file_path']
        
def get_photo_link(photo_path):
    return f"https://api.telegram.org/file/bot{API}/{photo_path}"


async def get_review_photos(review_id: int) -> Optional[list[str]]:
    photos = DB.get_photos_by_review_id(review_id)
    if photos:
        if isinstance(photos, Photos):
            return [photos.photo_data]
        else:
            photo_list = []
            for photo in photos:
                photo_list.append(photo.photo_data)
            return photo_list
    return None

            
        
