import os
from asyncio.queues import QueueEmpty
from os import path
from typing import Callable

import aiofiles
import aiohttp
import converter
import ffmpeg
import requests
from cache.admins import admins as a
from callsmusic import callsmusic
from callsmusic.callsmusic import client as USER
from callsmusic.queues import queues
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    DURATION_LIMIT,
    GROUP_SUPPORT,
    THUMB_IMG,
    UPDATES_CHANNEL,
    que,
)
from downloaders import youtube
from helpers.admins import get_administrators
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only
from helpers.filters import command, other_filters
from helpers.gets import get_file_name
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch

aiohttpsession = aiohttp.ClientSession()
chat_id = None
useer = "NaN"
DISABLED_GROUPS = []


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("💡 only admin can tap this button !", show_alert=True)
            return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(title, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/Roboto-Medium.ttf", 55)
    font2 = ImageFont.truetype("etc/finalfont.ttf", 75)
    draw.text((25, 528), "Playing here...", (0, 0, 0), font=font)
    draw.text((25, 610), f"{title[:20]}...", (0, 0, 0), font=font2)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    command(["playlist", f"playlist@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def playlist(client, message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("🔴 **𝗡𝗼 𝗠𝘂𝘀𝗶𝗰 𝗜𝘀 𝗖𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗣𝗹𝗮𝘆𝗶𝗻𝗴**")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "💡 **now playing** on {}".format(message.chat.title)
    msg += "\n\n• " + now_playing
    msg += "\n• Req By " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Queued Song**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n• {name}"
            msg += f"\n• Req by {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================
def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        stats = "⚙ settings for **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "🎚 𝗩𝗼𝗹𝘂𝗺𝗲: {}%\n".format(vol)
            stats += "🎵 𝗦𝗼𝗻𝗴 𝗣𝗹𝗮𝘆: `{}`\n".format(len(que))
            stats += "💡 𝗡𝗼𝘄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴: **{}**\n".format(queue[0][0])
            stats += "🎧 𝗣𝗹𝗮𝘆 𝗕𝘆: {}".format(queue[0][1].mention(style="md"))
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
            ],
            [
                InlineKeyboardButton("🎶𝗣𝗟𝗔𝗬𝗟𝗜𝗦𝗧", "playlist"),
            ],
            [InlineKeyboardButton("✨𝗖𝗟𝗢𝗦𝗘", "cls")],
        ]
    )
    return mar


@Client.on_message(
    command(["player", f"player@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def settings(client, message):
    global que
    playing = None
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply(
            "😕 **𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱**\n\n» 𝗣𝗹𝗲𝗮𝘀𝗲 𝗧𝘂𝗿𝗻 𝗢𝗻 𝗬𝗼𝘂𝗿 𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁 𝗣𝗹𝗲𝗮𝘀𝗲"
        )


@Client.on_message(
    command(["musicplayer", f"musicplayer@{BOT_USERNAME}"])
    & ~filters.edited
    & ~filters.bot
    & ~filters.private
)
@authorized_users_only
async def music_onoff(_, message):
    global DISABLED_GROUPS
    try:
        message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "**i'm only know** `/musicplayer on` **and** `/musicplayer off`"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await message.reply("`𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **music player already turned on.**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(f"🟢 **music player turned on**\n\n💬 `{message.chat.id}`")

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await message.reply("`𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴...`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **music player already turned off.**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(f"🟢 **music player turned off**\n\n💬 `{message.chat.id}`")
    else:
        await message.reply_text(
            "**i'm only know** `/musicplayer on` **and** `/musicplayer off`"
        )


@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("🔴 **𝗡𝗼 𝗠𝘂𝘀𝗶𝗰 𝗜𝘀 𝗖𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗣𝗹𝗮𝘆𝗶𝗻𝗴**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "💡 **now playing** on {}".format(cb.message.chat.title)
        msg += "\n\n• " + now_playing
        msg += "\n• Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Queued Song**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Req by {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
        chet_id = cb.message.chat.id
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer(
                "assistant is not connected to voice chat !", show_alert=True
            )
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("music paused!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "play":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer(
                "assistant is not connected to voice chat !", show_alert=True
            )
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("music resumed!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("🔴 **𝗡𝗼 𝗠𝘂𝘀𝗶𝗰 𝗜𝘀 𝗖𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗣𝗹𝗮𝘆𝗶𝗻𝗴**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "💡 **now playing** on {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Queued Song**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Req by {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "resume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer(
                "voice chat is not connected or already playing", show_alert=True
            )
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("music resumed!")

    elif type_ == "puse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer(
                "voice chat is not connected or already paused", show_alert=True
            )
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)

            await cb.answer("music paused!")

    elif type_ == "cls":
        await cb.answer("closed menu")
        await cb.message.delete()

    elif type_ == "menu":
        stats = updated_stats(cb.message.chat, qeue)
        await cb.answer("menu opened")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("📖 PLAY-LIST", "playlist"),
                ],
                [InlineKeyboardButton("◽️ Close", "cls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)

    elif type_ == "skip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer(
                "assistant is not connected to voice chat !", show_alert=True
            )
        else:
            callsmusic.queues.task_done(chet_id)

            if callsmusic.queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)

                await cb.message.edit("• no more playlist\n• leaving voice chat")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, callsmusic.queues.get(chet_id)["file"]
                )
                await cb.answer("skipped")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text("⏭ **You've skipped to the next song.**")

    elif type_ == "leave":
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("🟢 music playback has ended")
        else:
            await cb.answer(
                "assistant is not connected to voice chat !", show_alert=True
            )


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(_, message: Message):
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🔎 **𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴...**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"<b>💡 𝗣𝗹𝗲𝗮𝘀𝗲 𝗔𝗱𝗱 𝗧𝗵𝗲 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗙𝗶𝗿𝘀𝘁.</b>",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>💡 To use me, I need to be an Administrator with the permissions:\n\n» 🔴 __Delete messages__\n» 🔴 __Ban users__\n» 🔴 __Add users__\n» 🔴 __Manage voice chat__\n\n**Then type /reload</b>",
                    )
                    return
                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "🤖: i'm joined to this group for playing music on voice chat",
                    )
                    await lel.edit(
                        f"🟢 **𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗝𝗼𝗶𝗻𝗲𝗱 𝗖𝗵𝗮𝘁**",
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 𝗙𝗹𝗼𝗼𝗱 𝗪𝗮𝗶𝘁 𝗘𝗿𝗿𝗼𝗿 🔴 \n\n𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗖𝗮𝗻𝘁 𝗝𝗼𝗶𝗻 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 𝗗𝘂𝗲 𝗧𝗼 𝗠𝗮𝗻𝘆 𝗝𝗼𝗶𝗻 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗙𝗼𝗿 𝗨𝘀𝗲𝗿𝗯𝗼𝘁."
                        f"\n\nor add @{ASSISTANT_NAME} 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 𝗠𝗮𝗻𝘂𝗮𝗹𝗹𝘆 𝗧𝗵𝗲𝗻 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻.</b>",
                    )
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"» **𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗪𝗮𝘀 𝗕𝗮𝗻𝗻𝗲𝗱 𝗜𝗻 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 !**\n\n**𝗨𝗻𝗯𝗮𝗻  @{ASSISTANT_NAME} 𝗔𝗻𝗱 𝗔𝗱𝗱𝗲𝗱 𝗔𝗴𝗮𝗶𝗻 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 𝗠𝗮𝗻𝘂𝗮𝗹𝗹𝘆."
        )
        return
    text_links = None
    if message.reply_to_message:
        if message.reply_to_message.audio or message.reply_to_message.voice:
            pass
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == "url"]
        text_links = [entity for entity in entities if entity.type == "text_link"]
    else:
        urls = None
    if text_links:
        urls = True
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"🔴 **𝗠𝘂𝘀𝗶𝗰 𝗪𝗶𝘁𝗵 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗠𝗼𝗿𝗲 𝗧𝗵𝗮𝗻** `{DURATION_LIMIT}` **𝗠𝗶𝗻𝘂𝘁𝗲𝘀 𝗖𝗮𝗻𝘁 𝗣𝗹𝗮𝘆 🌸 !**"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("◾️ ᴍᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("◽️ ᴄʟᴏsᴇ", callback_data="cls"),
                ],
                [
                    InlineKeyboardButton(
                        "🔺 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/f5652cf748e9f27875bf7.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        message.from_user.first_name
        await generate_cover(title, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🔎 **𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴...**")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:60]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            results[0]["views"]
        except Exception as e:
            await lel.edit(
                "😕 **𝗖𝗼𝘂𝗹𝗱 𝗡𝗼𝘁 𝗙𝗶𝗻𝗱 𝗪𝗵𝗶𝗰𝗵 𝗬𝗼𝘂 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 🔴**\n\n» **𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗧𝗵𝗲 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲 𝗢𝗿 𝗜𝗻𝗰𝗹𝘂𝗱𝗲 𝗧𝗵𝗲 𝗔𝗿𝘁𝗶𝘀𝘁 𝗡𝗮𝗺𝗲 𝗔𝘀𝘀 𝗪𝗲𝗹𝗹**"
            )
            print(str(e))
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("◾️ ᴍᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("◽️ ᴄʟᴏsᴇ", callback_data="cls"),
                ],
                [
                    InlineKeyboardButton(
                        "🔺 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],
            ]
        )
        message.from_user.first_name
        await generate_cover(title, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        ydl_opts = {"format": "bestaudio[ext=m4a]"}

        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
        except:
            await lel.edit(
                "😕 **𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲 𝗡𝗼𝘁 𝗗𝗲𝘁𝗲𝗰𝘁𝗲𝗱**\n\n» **𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗧𝗵𝗲 𝗡𝗮𝗺𝗲 𝗢𝗳 𝗧𝗵𝗲 𝗦𝗼𝗻𝗴 𝗬𝗼𝘂 𝗪𝗮𝗻𝘁 𝗧𝗼 𝗣𝗹𝗮𝘆**"
            )
        # veez project
        try:
            toxxt = "\n"
            j = 0
            user = user_name
            emojilist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            while j < 5:
                toxxt += f"{emojilist[j]} [{results[j]['title'][:25]}...](https://youtube.com{results[j]['url_suffix']})\n"
                toxxt += f" ├ 💡 **Duration** - `{results[j]['duration']}`\n"
                toxxt += f" └ ⚡ __Powered by {BOT_NAME} AI__\n\n"
                j += 1
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "1️⃣", callback_data=f"plll 0|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "2️⃣", callback_data=f"plll 1|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "3️⃣", callback_data=f"plll 2|{query}|{user_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "4️⃣", callback_data=f"plll 3|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "5️⃣", callback_data=f"plll 4|{query}|{user_id}"
                        ),
                    ],
                    [InlineKeyboardButton(text="◽️ Close", callback_data="cls")],
                ]
            )
            await message.reply_photo(
                photo=f"{THUMB_IMG}", caption=toxxt, reply_markup=keyboard
            )

            await lel.delete()
            # veez project
            return
            # veez project
        except:
            await lel.edit("__no more results to choose, starting to playing...__")

            # print(results)
            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:60]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"{title}.jpg"
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
                results[0]["views"]
            except Exception as e:
                await lel.edit(
                    "😕 **𝗖𝗼𝘂𝗹𝗱 𝗡𝗼𝘁 𝗙𝗶𝗻𝗱 𝗪𝗵𝗶𝗰𝗵 𝗬𝗼𝘂 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 🔴**\n\n» **𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗧𝗵𝗲 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲 𝗢𝗿 𝗜𝗻𝗰𝗹𝘂𝗱𝗲 𝗧𝗵𝗲 𝗔𝗿𝘁𝗶𝘀𝘁 𝗡𝗮𝗺𝗲 𝗔𝘀𝘀 𝗪𝗲𝗹𝗹**"
                )
                print(str(e))
                return
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("◾️ ᴍᴇɴᴜ", callback_data="menu"),
                        InlineKeyboardButton("◽️ ᴄʟᴏsᴇ", callback_data="cls"),
                    ],
                    [
                        InlineKeyboardButton(
                            "🔺 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                        )
                    ],
                ]
            )
            message.from_user.first_name
            await generate_cover(title, thumbnail)
            file_path = await converter.convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"💡 **Track added to queue »** `{position}`\n\n🏷 **𝗡𝗔𝗠𝗘:** [{title[:35]}...]({url})\n⏱ **𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration}`\n🎧 **𝗣𝗟𝗔𝗬 𝗕𝗬:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            await lel.edit(
                "😕 **𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱**\n\n» 𝗣𝗹𝗲𝗮𝘀𝗲 𝗧𝘂𝗿𝗻 𝗢𝗻 𝗬𝗼𝘂𝗿 𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁 𝗣𝗹𝗲𝗮𝘀𝗲"
            )
            return
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **𝗡𝗔𝗠𝗘:** [{title[:60]}]({url})\n⏱ **𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration}`\n💡 **𝗦𝗧𝗔𝗧𝗨𝗦:** `Playing`\n"
            + f"🎧 **𝗣𝗟𝗔𝗬 𝗕𝗬:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()


@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que
    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_ = cbd.split(None, 1)[1]
    try:
        x, query, useer_id = typed_.split("|")
    except:
        await cb.message.edit(
            "😕 **𝗖𝗼𝘂𝗹𝗱 𝗡𝗼𝘁 𝗙𝗶𝗻𝗱 𝗪𝗵𝗶𝗰𝗵 𝗬𝗼𝘂 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 🔴**\n\n» **𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗧𝗵𝗲 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲 𝗢𝗿 𝗜𝗻𝗰𝗹𝘂𝗱𝗲 𝗧𝗵𝗲 𝗔𝗿𝘁𝗶𝘀𝘁 𝗡𝗮𝗺𝗲 𝗔𝘀𝘀 𝗪𝗲𝗹𝗹**"
        )
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer("💡 sorry, this is not for you !", show_alert=True)
        return
    # await cb.message.edit("🔁 **𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴...**")
    x = int(x)
    try:
        cb.message.reply_to_message.from_user.first_name
    except:
        cb.message.from_user.first_name
    results = YoutubeSearch(query, max_results=5).to_dict()
    resultss = results[x]["url_suffix"]
    title = results[x]["title"][:60]
    thumbnail = results[x]["thumbnails"][0]
    duration = results[x]["duration"]
    results[x]["views"]
    url = f"https://www.youtube.com{resultss}"
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await cb.message.edit(
                f"🔴 **𝗠𝘂𝘀𝗶𝗰 𝗪𝗶𝘁𝗵 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗠𝗼𝗿𝗲 𝗧𝗵𝗮𝗻** `{DURATION_LIMIT}` **𝗠𝗶𝗻𝘂𝘁𝗲𝘀 𝗖𝗮𝗻𝘁 𝗣𝗹𝗮𝘆 🌸 !**"
            )
            return
    except:
        pass
    try:
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("◾️ ᴍᴇɴᴜ", callback_data="menu"),
                InlineKeyboardButton("◽️ ᴄʟᴏsᴇ", callback_data="cls"),
            ],
            [InlineKeyboardButton("🔺 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}")],
        ]
    )
    await generate_cover(title, thumbnail)
    file_path = await converter.convert(youtube.download(url))
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.delete()
        await b.send_photo(
            chat_id,
            photo="final.png",
            caption=f"💡 **Track added to queue »** `{position}`\n\n🏷 **𝗡𝗔𝗠𝗘:** [{title[:35]}...]({url})\n⏱ **𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration}`\n🎧 **𝗣𝗟𝗔𝗬 𝗕𝗬:** {r_by.mention}",
            reply_markup=keyboard,
        )
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await cb.message.delete()
        await b.send_photo(
            chat_id,
            photo="final.png",
            caption=f"🏷 **𝗡𝗔𝗠𝗘:** [{title[:60]}]({url})\n⏱ **𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration}`\n💡 **𝗦𝗧𝗔𝗧𝗨𝗦:** `Playing`\n"
            + f"🎧 **𝗣𝗟𝗔𝗬 𝗕𝗬:** {r_by.mention}",
            reply_markup=keyboard,
        )
    if path.exists("final.png"):
        os.remove("final.png")


@Client.on_message(command(["ytp", f"ytp@{BOT_USERNAME}"]) & other_filters)
async def ytplay(_, message: Message):
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🎶 **𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴...**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"💡 **𝗣𝗹𝗲𝗮𝘀𝗲 𝗔𝗱𝗱 𝗧𝗵𝗲 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗙𝗶𝗿𝘀𝘁**",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "💡 **To use me, I need to be an Administrator with the permissions:\n\n» 🔴 __Delete messages__\n» 🔴 __Ban users__\n» 🔴 __Add users__\n» 🔴 __Manage voice chat__\n\n**Then type /reload**",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "🤖: 𝗜'𝗺 𝗝𝗼𝗶𝗻𝗲𝗱 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 𝗙𝗼𝗿 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 𝗠𝘂𝘀𝗶𝗰 𝗜𝗻 𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁",
                    )
                    await lel.edit(
                        f"🟢 **𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝗳𝘂𝗹𝗹𝘆 𝗝𝗼𝗶𝗻𝗲𝗱 𝗖𝗵𝗮𝘁 𝗚𝗿𝗼𝘂𝗽 🌸**",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"🔴 **𝗙𝗹𝗼𝗼𝗱 𝗪𝗮𝗶𝘁 𝗘𝗿𝗿𝗼𝗿** 🔴 \n\n**𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗖𝗮𝗻𝘁 𝗝𝗼𝗶𝗻 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 𝗗𝘂𝗲 𝗧𝗼 𝗠𝗮𝗻𝘆 𝗝𝗼𝗶𝗻 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗙𝗼𝗿 𝗨𝘀𝗲𝗿𝗯𝗼𝘁.**"
                        f"\n\n**or add @{ASSISTANT_NAME} 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 𝗠𝗮𝗻𝘂𝗮𝗹𝗹𝘆 𝗧𝗵𝗲𝗻 𝗧𝗿𝘆 𝗔𝗴𝗮𝗶𝗻.**",
                    )
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"💡 **𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗪𝗮𝘀 𝗕𝗮𝗻𝗻𝗲𝗱 𝗜𝗻 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 !** \n\n**𝗨𝗻𝗯𝗮𝗻  @{ASSISTANT_NAME} 𝗔𝗻𝗱 𝗔𝗱𝗱 𝗧𝗼 𝗧𝗵𝗶𝘀 𝗚𝗿𝗼𝘂𝗽 𝗔𝗴𝗮𝗶𝗻 𝗠𝗮𝗻𝘂𝗮𝗹𝗹𝘆.**"
        )
        return

    message.from_user.id
    message.from_user.first_name

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("🎶 **𝗖𝗼𝗻𝗻𝗲𝗰𝘁𝗶𝗻𝗴 𝗧𝗼 𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁 ✨🌸**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:60]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]

    except Exception as e:
        await lel.edit(
            "😕 **𝗖𝗼𝘂𝗹𝗱 𝗡𝗼𝘁 𝗙𝗶𝗻𝗱 𝗪𝗵𝗶𝗰𝗵 𝗬𝗼𝘂 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 🔴**\n\n» **𝗣𝗹𝗲𝗮𝘀𝗲 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗧𝗵𝗲 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲 𝗢𝗿 𝗜𝗻𝗰𝗹𝘂𝗱𝗲 𝗧𝗵𝗲 𝗔𝗿𝘁𝗶𝘀𝘁 𝗡𝗮𝗺𝗲 𝗔𝘀𝘀 𝗪𝗲𝗹𝗹**"
        )
        print(str(e))
        return
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"🔴 **𝗠𝘂𝘀𝗶𝗰 𝗪𝗶𝘁𝗵 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 𝗠𝗼𝗿𝗲 𝗧𝗵𝗮𝗻** `{DURATION_LIMIT}` **𝗠𝗶𝗻𝘂𝘁𝗲𝘀 𝗖𝗮𝗻𝘁 𝗣𝗹𝗮𝘆 🌸 !**"
            )
            return
    except:
        pass
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("◾️ ᴍᴇɴᴜ", callback_data="menu"),
                InlineKeyboardButton("◽️ ᴄʟᴏsᴇ", callback_data="cls"),
            ],
            [
                InlineKeyboardButton(
                    "🔺 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
                InlineKeyboardButton("🔸 ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
            ],
        ]
    )
    message.from_user.first_name
    await generate_cover(title, thumbnail)
    file_path = await converter.convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"💡 **Track added to queue »** `{position}`\n\n🏷 **𝗡𝗔𝗠𝗘:** [{title[:35]}...]({url})\n⏱ **𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration}`\n🎧 **𝗣𝗟𝗔𝗬 𝗕𝗬:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            await lel.edit(
                "😕 **𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱**\n\n» 𝗣𝗹𝗲𝗮𝘀𝗲 𝗧𝘂𝗿𝗻 𝗢𝗻 𝗬𝗼𝘂𝗿 𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁 𝗣𝗹𝗲𝗮𝘀𝗲"
            )
            return
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **𝗡𝗔𝗠𝗘:** [{title[:60]}]({url})\n⏱ **𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡:** `{duration}`\n💡 **𝗦𝗧𝗔𝗧𝗨𝗦:** `Playing`\n"
            + f"🎧 **𝗣𝗟𝗔𝗬 𝗕𝗬:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
