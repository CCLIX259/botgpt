import asyncio
import configparser
import multiprocessing
import os

import openai
from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.errors import Forbidden

config = configparser.ConfigParser()

openai.api_key = "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"


def get_file(path_):
    for root, dirs, files in os.walk(path_):
        return [file for file in files]


def get_ids_():
    ids = []
    for root, dirs, files in os.walk(f'./config/'):
        for dirses in dirs:
            ids.append(int(dirses))
    return ids


async def chat_gpt(promt, post):
    print(f'Пост: {post}. {promt}')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Пост: {post}. {promt}",
        max_tokens=1024,
        temperature=0.85
    )

    return response.choices[0].text.split('\n')[-1]


async def start_session(name_session, api_id, api_hash, proxy, time_, sleep, promt):
    proxy = {
        "scheme": "socks5",
        "hostname": proxy.split(':')[0],
        "port": int(proxy.split(':')[1]),
        "username": proxy.split(':')[2],
        "password": proxy.split(':')[3]
    }
    async with Client(f"./session/{name_session[:-2]}/" + name_session, api_id=api_id, api_hash=api_hash, proxy=proxy) as app:
        old_posts = []
        messages = 0
        while True:
            try:
                async for dialog in app.get_dialogs():
                    await asyncio.sleep(10)
                    if dialog.chat.type == ChatType.CHANNEL:
                        message = app.get_chat_history(dialog.chat.id, limit=-1, offset=-1)
                        async for i in message:
                            post = i.text or i.caption
                            if (i.id, i.chat.id) not in old_posts:
                                try:
                                    msg = await app.get_discussion_message(i.chat.id, i.id)
                                    await msg.reply(text=await chat_gpt(promt, post),
                                                    quote=True)
                                    old_posts.append((i.id, i.chat.id))
                                    break
                                except Forbidden:
                                    chat = await app.get_chat(i.chat.id)
                                    await chat.linked_chat.join()
                                    await msg.reply(text=await chat_gpt(promt, post),
                                                    quote=True)
                            messages += 1
                            if messages >= int(sleep):
                                await asyncio.sleep(1000)
                        await asyncio.sleep(float(time_))
            except Exception as e:
                print(e)


def run_async_function(name_session, api_id, api_hash, proxy, time_, sleep, promt):
    asyncio.run(start_session(name_session, api_id, api_hash, proxy, time_, sleep, promt))


def main():
    for id_ in get_ids_():
        for file in get_file(f"./session/{id_}"):
            config.read(f"./config/{id_}/config_{file}"[:-8] + ".ini", encoding="UTF-8")
            process = multiprocessing.Process(target=run_async_function,
                                              args=(config['SETTINGS']['name_session'],
                                                    config['SETTINGS']['api_id'],
                                                    config['SETTINGS']['api_hash'],
                                                    config['SETTINGS']['proxy'],
                                                    config['SETTINGS']['time'],
                                                    config['SETTINGS']['loop_account'],
                                                    config['SETTINGS']['promt']))
            process.start()


if __name__ == "__main__":
    main()
