# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/YouTube-Search-Bot/blob/main/LICENSE

import requests
from pyrogram import Client, filters
from pyrogram.types import *


Bot = Client(
    "YouTube-Search-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.all)
async def text(bot, update):
    text = "Search youtube videos using below buttons.\nMade by @FayasNoushad"
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Search here", switch_inline_query_current_chat)],
            [InlineKeyboardButton(text="Search in another chat", switch_inline_query)]
        ]
    )
    await update.reply_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def search(bot, update):
    results = requests.get("https://youtube.api.fayas.me/videos/?query=" + update.query).json()["result"][50:]
    answers = []
    for result in results:
        title = result["title"]
        description = f"{result["viewCount"]["short"]} | {result["duration"]}"
        details = f"**{title}**" + "\n" \
        f"**Channel:** [{result["channel"]["name"]}]({result["channel"]["link"]}" + "\n" \
        f"**Duration:** {result["accessibility"]["duration"]}" + "\n" \
        f"**Views:** {result["viewCount"]["text"]}" + "\n" \
        f"**Published Time:** {result["publishedTime"]}" + "\n" \
        "\n" + "Made by @FayasNoushad"
        thumbnail = "https://img.youtube.com/vi/" + result["id"] + "/sddefault.jpg"
        reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Watch Video 📹", url=result["link"])]
            ]
        )
        answers.append(
            InlineQueryResultPhoto(
                title=title,
                description=description,
                caption=details,
                photo_url=thumbnail,
                reply_markup=reply_markup
            )
        )
    await update.answer(answers)


Bot.run()
