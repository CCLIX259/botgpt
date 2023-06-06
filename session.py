import asyncio

from pyrogram import Client
from pyrogram.errors.exceptions import FloodWait

API_ID = 19309010
API_HASH = "dfdf154157cca400bd53b00100468fa5"


async def set_name(name_session, name):
    app = Client(f"./session/{name_session}/{name_session}", api_id=API_ID, api_hash=API_HASH)
    async with app:
        try:
            name = name.split()
            await app.update_profile(first_name=name[0], last_name=name[1])
            return "[+] Успешно изменен!"
        except Exception as e:
            print(e)
            return "[-] Не удалось изменить!"


async def set_description(name_session, description):
    app = Client(f"./session/{name_session}/{name_session}", api_id=API_ID, api_hash=API_HASH)
    async with app:
        try:
            await app.update_profile(bio=description)
            return "[+] Успешно изменен!"
        except Exception as e:
            print(e)
            return "[-] Не удалось изменить!"


async def joined_channels(path_, channels):
    app = Client(f"./session/{path_}", api_id=API_ID, api_hash=API_HASH)
    async with app:
        for channel in channels:
            try:
                chat = await app.get_chat(channel)
                await app.join_chat(chat.id)
            except FloodWait:
                await asyncio.sleep(300)
                continue
            except Exception as e:
                print(e)


async def set_photo(name_session):
    app = Client(f"./session/{name_session}/{name_session}", api_id=API_ID, api_hash=API_HASH)
    async with app:
        try:
            await app.set_profile_photo(photo=f'./photo/{name_session}.jpg')
            return "[+] Успешно изменен!"
        except Exception as e:
            print(e)
            return "[-] Не удалось изменить!"
