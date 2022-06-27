import os
import ytthumb
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
from youtubesearchpython import VideosSearch

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
CHANNELS = set(int(x) for x in os.environ.get("CHANNELS", "").split())

Bot = Client(
    "YouTube-Search-Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)


@Bot.on_message(filters.private & filters.all)
async def text(bot, update):
    
    text = "Search youtube videos using below buttons.\n\nMade by @FayasNoushad"
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Search here", switch_inline_query_current_chat="")],
            [InlineKeyboardButton(text="Search in another chat", switch_inline_query="")]
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
    
    results = VideosSearch(update.query, limit=50).result()
    answers = []
    
    for result in results:
        if len(CHANNELS) > 0 and result["channel"]["id"] not in CHANNELS:
            continue
        title = result["title"]
        views_short = result["viewCount"]["short"]
        duration = result["duration"]
        duration_text = result["accessibility"]["duration"]
        views = result["viewCount"]["text"]
        publishedtime = result["publishedTime"]
        channel_name = result["channel"]["name"]
        channel_link = result["channel"]["link"]
        description = f"{views_short} | {duration}"
        details = f"**Title:** {title}" + "\n" \
        f"**Channel:** [{channel_name}]({channel_link})" + "\n" \
        f"**Duration:** {duration_text}" + "\n" \
        f"**Views:** {views}" + "\n" \
        f"**Published Time:** {publishedtime}" + "\n" \
        "\n" + "**Made by @FayasNoushad**"
        thumbnail = ytthumb.thumbnail(result["id"])
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Watch Video 📹", url=result["link"])]]
        )
        try:
            answers.append(
                InlineQueryResultPhoto(
                    title=title,
                    description=description,
                    caption=details,
                    photo_url=thumbnail,
                    reply_markup=reply_markup
                )
            )
        except:
            pass
    
    await update.answer(answers)


Bot.run()
