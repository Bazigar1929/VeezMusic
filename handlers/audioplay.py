# this module i created only for playing music using audio file, idk, because the audio player on play.py module not working
# so this is the alternative
# audio play function
# tede ganteng tq

from os import path

import converter
from callsmusic import callsmusic, queues
from config import (
    AUD_IMG,
    BOT_USERNAME,
    DURATION_LIMIT,
    GROUP_SUPPORT,
    QUE_IMG,
    UPDATES_CHANNEL,
)
from handlers.play import convert_seconds
from helpers.filters import command, other_filters
from helpers.gets import get_file_name
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(command(["stream", f"stream@{BOT_USERNAME}"]) & other_filters)
async def stream(_, message: Message):
    costumer = message.from_user.mention
    lel = await message.reply_text("🔁 **𝗙𝗶𝗻𝗱𝗶𝗻𝗴** sound...")

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="✨ 𝗦𝗨𝗣𝗣𝗢𝗥𝗧", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    text="🌻 𝗨𝗣𝗗𝗔𝗧𝗘", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    audio = message.reply_to_message.audio if message.reply_to_message else None
    if not audio:
        return await lel.edit("💭 **𝗣𝗹𝗲𝗮𝘀𝗲 𝗥𝗲𝗽𝗹𝘆 𝗧𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗔𝘂𝗱𝗶𝗼 𝗙𝗶𝗹𝗲**")
    if round(audio.duration / 60) > DURATION_LIMIT:
        return await lel.edit(
            f"🔴 **music with duration more than** `{DURATION_LIMIT}` **minutes, can't play !**"
        )

    # tede_ganteng = True
    title = audio.title
    file_name = get_file_name(audio)
    duration = convert_seconds(audio.duration)
    file_path = await converter.convert(
        (await message.reply_to_message.download(file_name))
        if not path.isfile(path.join("downloads", file_name))
        else file_name
    )
    # ambil aja bg
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo=f"{QUE_IMG}",
            caption=f"💡 **Track added to queue »** `{position}`\n\n🏷 **Name:** {title[:50]}\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {costumer}",
            reply_markup=keyboard,
        )
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo=f"{AUD_IMG}",
            caption=f"🏷 **Name:** {title[:50]}\n⏱ **Duration:** `{duration}`\n💡 **Status:** `Playing`\n"
            + f"🎧 **Request by:** {costumer}",
            reply_markup=keyboard,
        )

    return await lel.delete()
