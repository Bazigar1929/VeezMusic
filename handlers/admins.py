# Copyright (C) 2021 VeezMusicProject

from asyncio import QueueEmpty

from callsmusic import callsmusic
from callsmusic.queues import queues
from config import BOT_USERNAME, que
from cache.admins import admins
from handlers.play import cb_admin_check
from helpers.channelmusic import get_chat_id
from helpers.dbtools import delcmd_is_on, delcmd_off, delcmd_on, handle_user_status
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


# Back Button
BACK_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🏡 Go Back", callback_data="cbback")]]
)

# @Client.on_message(filters.text & ~filters.private)
# async def delcmd(_, message: Message):
#    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!") or message.text.startswith("."):
#        await message.delete()
#    await message.continue_propagation()

# remove the ( # ) if you want the auto del cmd feature is on


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "🟢 Bot **𝗕𝗢𝗧 𝗥𝗘𝗟𝗢𝗔𝗗𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗙𝗨𝗟𝗟𝗬!**\n🟢 **𝗔𝗗𝗠𝗜𝗡 𝗟𝗜𝗦𝗧** 𝗛𝗔𝗦 𝗕𝗘𝗘𝗡 **𝗨𝗣𝗗𝗔𝗧𝗘𝗗 !**"
    )


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "🟡 **𝗛𝗘𝗔𝗥 𝗜𝗦 𝗧𝗛𝗘 𝗖𝗢𝗡𝗧𝗥𝗢𝗟 𝗠𝗘𝗡𝗨**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸ 𝗣𝗔𝗨𝗦𝗘", callback_data="cbpause"),
                    InlineKeyboardButton("▶️ 𝗥𝗘𝗦𝗨𝗠𝗘", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("⏩ 𝗦𝗞𝗜𝗣", callback_data="cbskip"),
                    InlineKeyboardButton("⏹ 𝗦𝗧𝗢𝗣", callback_data="cbend"),
                ],
                [InlineKeyboardButton("⛔ 𝗔𝗡𝗧𝗜 𝗖𝗠𝗗", callback_data="cbdelcmds")],
                [InlineKeyboardButton("🗑 𝗖𝗟𝗢𝗦𝗘", callback_data="close")],
            ]
        ),
    )


@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("🔴 **𝗡𝗼 𝗠𝘂𝘀𝗶𝗰 𝗜𝘀 𝗖𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗣𝗹𝗮𝘆𝗶𝗻𝗴**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text(
            "⏸ **𝗧𝗿𝗮𝗰𝗸𝗲𝗱 𝗣𝗮𝘂𝘀𝗲.**\n\n• **𝗧𝗼 𝗥𝗲𝘀𝘂𝗺𝗲 𝗧𝗵𝗲 𝗣𝗹𝗮𝘆𝗯𝗮𝗰𝗸, 𝗨𝘀𝗲 𝗧𝗵𝗲**\n» `/resume` 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."
        )


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("🔴 **𝗡𝗼 𝗠𝘂𝘀𝗶𝗰 𝗜𝘀 𝗣𝗮𝘂𝘀𝗲𝗱**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            "▶️ **Track resumed.**\n\n• **𝗧𝗼 𝗣𝗮𝘂𝘀𝗲 𝗧𝗵𝗲 𝗣𝗹𝗮𝘆𝗯𝗮𝗰𝗸 𝗨𝘀𝗲 𝗧𝗵𝗲**\n» `/pause` 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."
        )


@Client.on_message(command(["end", f"end@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("🔴 **𝗡𝗼 𝗠𝘂𝘀𝗶𝗰 𝗖𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗣𝗹𝗮𝘆𝗶𝗻𝗴**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("🟢 **𝗠𝘂𝘀𝗶𝗰 𝗣𝗹𝗮𝘆𝗯𝗮𝗰𝗸 𝗛𝗮𝘀 𝗘𝗻𝗱𝗲𝗱**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("🔴 **𝗡𝗼 𝗠𝘂𝘀𝗶𝗰 𝗜𝘀 𝗖𝘂𝗿𝗿𝗲𝗻𝘁𝗹𝘆 𝗣𝗹𝗮𝘆𝗶𝗻𝗴**")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(chat_id, queues.get(chat_id)["file"])

    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await message.reply_text("⏭✨ **𝗬𝗼𝘂 𝗛𝗮𝘃𝗲 𝗦𝗹𝗶𝗽𝗽𝗲𝗱 𝗧𝗼 𝗦𝗼𝗻𝗴.**")


@Client.on_message(command(["auth", f"auth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("💡 𝗥𝗲𝗽𝗹𝘆 𝗧𝗼 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗧𝗼 𝗔𝗹𝗹𝗼𝘄 𝗨𝘀𝗲𝗿 !")
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🟢 𝗨𝘀𝗲𝗿 𝗔𝗹𝗹𝗼𝘄𝗲𝗱.\n\n𝗢𝗻 𝗡𝗼𝘄 𝗢𝗻 .𝗧𝗵𝗮𝘁 𝗨𝘀𝗲𝗿 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀."
        )
    else:
        await message.reply("🟢 𝗨𝘀𝗲𝗿 𝗔𝗹𝗿𝗲𝗮𝗱𝘆 𝗔𝗹𝗹𝗼𝘄𝗲𝗱")


@Client.on_message(command(["deauth", f"deauth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("🔴 𝗥𝗲𝗽𝗹𝘆 𝗧𝗼 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗧𝗼 𝗗𝗲𝗻𝗻𝘆!")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🔴 𝗨𝘀𝗲𝗿 𝗗𝗲𝗻𝗻𝘆.\n\n𝗧𝗵𝗮𝘁 𝗨𝘀𝗲𝗿 𝗖𝗮𝗻'𝘁 𝗨𝘀𝗲 𝗢𝘄𝗻𝗲𝗿 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀"
        )
    else:
        await message.reply("🔴 𝗨𝘀𝗲𝗿 𝗔𝗹𝘄𝗮𝘀 𝗗𝗲𝗻𝗻𝘆!")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "𝗥𝗼𝗮𝗱 𝗧𝗵𝗲/help 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗧𝗼 𝗞𝗻𝗼𝘄 𝗛𝗼𝘄 𝗧𝗼 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀"
        )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            return await message.reply_text("✅ already activated")
        await delcmd_on(chat_id)
        await message.reply_text("🟢 activated successfully")
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 disabled successfully")
    else:
        await message.reply_text(
            "read the /help message to know how to use this command"
        )


# music player callbacks (control by buttons feature)


@Client.on_callback_query(filters.regex("cbpause"))
@cb_admin_check
async def cbpause(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if (query.message.chat.id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[query.message.chat.id] == "paused"
    ):
        await query.edit_message_text(
            "❌ **no music is currently playing**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text(
            "⏸ music playback has been paused", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbresume"))
@cb_admin_check
async def cbresume(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if (query.message.chat.id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[query.message.chat.id] == "resumed"
    ):
        await query.edit_message_text(
            "❌ **no music is paused**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.resume_stream(query.message.chat.id)
        await query.edit_message_text(
            "▶️ music playback has been resumed", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbend"))
@cb_admin_check
async def cbend(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "❌ **no music is currently playing**", reply_markup=BACK_BUTTON
        )
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        await query.edit_message_text(
            "✅ the music queue has been cleared and successfully left voice chat",
            reply_markup=BACK_BUTTON,
        )


@Client.on_callback_query(filters.regex("cbskip"))
@cb_admin_check
async def cbskip(_, query: CallbackQuery):
    global que
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "❌ **no music is currently playing**", reply_markup=BACK_BUTTON
        )
    else:
        queues.task_done(query.message.chat.id)

        if queues.is_empty(query.message.chat.id):
            callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await query.edit_message_text(
        "⏭ **You've skipped to the next song**", reply_markup=BACK_BUTTON
    )
