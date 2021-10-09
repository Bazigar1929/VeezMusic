import asyncio

from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"join@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>• **𝐈 𝐌 𝐍𝐨𝐭 𝐇𝐚𝐯𝐞 𝐏𝐞𝐞𝐦𝐢𝐬𝐬𝐢𝐨𝐧:**\n\n» 🔴__Add Users__</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "👑: 𝐈'𝐦 𝐉𝐨𝐢𝐧𝐞𝐝 𝐇𝐞𝐚𝐫 𝐅𝐨𝐫 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐌𝐮𝐬𝐢𝐜 𝐈𝐧 𝐕𝐂"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>🟢𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐉𝐨𝐢𝐧𝐞𝐝</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n\n User {user.first_name} couldn't join your group due to heavy join requests for userbot."
            "\n\nor manually add assistant to your Group and try again</b>",
        )
        return
    await message.reply_text(
        f"<b>🟢𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐉𝐨𝐢𝐧𝐞𝐝 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩</b>",
    )


@Client.on_message(
    command(["leave", f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def rem(client, message):
    try:
        await USER.send_message(message.chat.id, "🟢𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐋𝐞𝐚𝐯𝐞 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>user couldn't leave your group, may be floodwaits.\n\nor manually kick me from your group</b>"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("⚪ **𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐋𝐞𝐚𝐯𝐢𝐧𝐠 𝐀𝐥𝐥 𝐂𝐡𝐚𝐭𝐬 !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐋𝐞𝐚𝐯𝐢𝐧𝐠 𝐀𝐥𝐥 𝐂𝐡𝐚𝐭𝐬...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐋𝐞𝐚𝐯𝐢𝐧𝐠...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats.\nFailed {failed} chats."
    )


@Client.on_message(
    command(["joinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply(
            "❌ `NOT_LINKED`\n\n• **The userbot could not play music, due to group not linked to channel yet.**"
        )
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>• ** 𝐈 𝐌 𝐍𝐨𝐭 𝐇𝐚𝐯𝐞 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧:**\n\n» 🔴__Add Users__</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "⚪: 𝐈'𝐦 𝐉𝐨𝐢𝐧𝐞𝐝 𝐇𝐞𝐚𝐫 𝐅𝐨𝐫 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐌𝐮𝐬𝐢𝐜 𝐎𝐧 𝐕𝐂"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>🟢𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐉𝐨𝐢𝐧𝐞𝐝 𝐂𝐡𝐚𝐧𝐧𝐞𝐥</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑\n\n**userbot couldn't join to channel** due to heavy join requests for userbot, make sure userbot is not banned in channel."
            f"\n\nor manually add @{ASSISTANT_NAME} to your channel and try again</b>",
        )
        return
    await message.reply_text(
        "<b>🟢𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐉𝐨𝐢𝐧𝐞𝐝 𝐂𝐡𝐚𝐧𝐧𝐞𝐥</b>",
    )
