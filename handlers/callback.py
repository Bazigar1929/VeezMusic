# (C) 2021 VeezMusic-Project

from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from handlers.play import cb_admin_check
from helpers.decorators import authorized_users_only
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>✨ **𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗜'𝗠 {query.message.from_user.mention} !** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) !**

💡 **𝗳𝗶𝗻𝗱 𝗼𝘂𝘁 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗯𝗼𝘁'𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗮𝗻𝗱 𝗵𝗼𝘄 𝘁𝗵𝗲𝘆 𝘄𝗼𝗿𝗸 𝗯𝘆 𝗰𝗹𝗶𝗰𝗸𝗶𝗻𝗴 𝗼𝗻 𝗧𝗵𝗲\n» 📚 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻!**

❔ **𝘁𝗼 𝗸𝗻𝗼𝘄 𝗵𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗰𝗹𝗶𝗰𝗸 𝗼𝗻 𝘁𝗵𝗲 » ❓ 𝗯𝗮𝘀𝗶𝗰 𝗴𝘂𝗶𝗱𝗲 𝗯𝘂𝘁𝘁𝗼𝗻!**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "◾️𝗔𝗗𝗗 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣◾️",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("◽️𝗕𝗔𝗦𝗜𝗖 𝗚𝗨𝗜𝗗𝗘◽️", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("🔶𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦🔶", callback_data="cbcmds"),
                    InlineKeyboardButton("🔶𝗢𝗪𝗡𝗘𝗥🔶", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "🔹𝗦𝗨𝗣𝗣𝗢𝗥𝗧🔹", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "🔺𝗨𝗣𝗗𝗔𝗧𝗘𝗦🔺", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "◾𝗜𝗠𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡️◾️", url="https://github.com/levina-lab/VeezMusic"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>🌸 𝗵𝗲𝗹𝗹𝗼 𝘁𝗵𝗲𝗿𝗲, 𝘄𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝘁𝗵𝗲 𝗵𝗲𝗹𝗽 𝗺𝗲𝗻𝘂 !</b>

» **ɪɴ ᴛʜɪs ᴍᴇɴᴜ ʏᴏᴜ ᴄᴀɴ ᴏᴘᴇɴ sᴇᴠᴇʀᴀʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅ ᴍᴇɴᴜs, ɪɴ ᴇᴀᴄʜ ᴄᴏᴍᴍᴀɴᴅ ᴍᴇɴᴜ ᴛʜᴇʀᴇ ɪs ᴀʟsᴏ ᴀ ʙʀɪᴇғ ᴇxᴘʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴇᴀᴄʜ ᴄᴏᴍᴍᴀɴᴅ**

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✨ʙᴀsɪᴄ✨", callback_data="cbbasic"),
                    InlineKeyboardButton("✨ᴀᴅᴠᴀɴᴄᴇ✨", callback_data="cbadvanced"),
                ],
                [
                    InlineKeyboardButton("✨ᴀᴅᴍɪɴ✨", callback_data="cbadmin"),
                    InlineKeyboardButton("✨sᴜᴅᴏ✨", callback_data="cbsudo"),
                ],
                [InlineKeyboardButton("✨ᴏᴡɴᴇʀ✨", callback_data="cbowner")],
                [InlineKeyboardButton("🌸ʙᴀᴄᴋ ᴛᴏ ʜᴇʟᴘ", callback_data="cbguide")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>👑 𝗛𝗲𝗿𝗲 𝗜𝘀 𝗧𝗵𝗲 𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀</b>

🎧 [ 𝐁𝐀𝐙𝐈𝐆𝐀𝐑 𝐌𝐔𝐒𝐈𝐂 𝐁𝐎𝐓 ]

/play (𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲) - 𝗣𝗹𝗮𝘆 𝗦𝗼𝗻𝗴 𝗙𝗿𝗼𝗺 𝗬𝗼𝘂𝘁𝘂𝗯𝗲
/ytp (𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲) - 𝗣𝗹𝗮𝘆 𝗦𝗼𝗻𝗴 𝗗𝗶𝗿𝗲𝗰𝘁𝗹𝘆 𝗙𝗿𝗼𝗺 𝗬𝗼𝘂𝘁𝘂𝗯𝗲
/stream (𝗥𝗲𝗽𝗹𝘆 𝗧𝗼 𝗔𝘂𝗱𝗶𝗼) - 𝗣𝗹𝗮𝘆 𝗦𝗼𝗻𝗴 𝗨𝘀𝗶𝗻𝗴 𝗔𝘂𝗱𝗶𝗼 𝗙𝗶𝗹𝗲
/playlist - 𝗦𝗵𝗼𝘄 𝗧𝗵𝗲 𝗟𝗶𝘀𝘁 𝗦𝗼𝗻𝗴 𝗜𝗻 𝗤𝘂𝗲𝘂𝗲
/song (𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲) - 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗦𝗼𝗻𝗴 𝗙𝗿𝗼𝗺 𝗬𝗼𝘂𝘁𝘂𝗯𝗲
/search (𝗩𝗶𝗱𝗲𝗼 𝗡𝗮𝗺𝗲) - 𝗦𝗲𝗮𝗿𝗰𝗵 𝗩𝗶𝗱𝗲𝗼 𝗙𝗿𝗼𝗺 𝗬𝗼𝘂𝘁𝘂𝗯𝗲 𝗗𝗲𝘁𝗮𝗶𝗹𝗲𝗱
/vsong (𝗩𝗶𝗱𝗲𝗼 𝗡𝗮𝗺𝗲) - 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗩𝗶𝗱𝗲𝗼 𝗙𝗿𝗼𝗺 𝗬𝗼𝘂𝘁𝘂𝗯𝗲 𝗗𝗲𝘁𝗮𝗶𝗹𝗲𝗱
/lyric - (𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲) 𝗟𝘆𝗿𝗶𝗰𝘀 𝗦𝗰𝗿𝗮𝗽𝗽𝗲𝗿
/vk (𝗦𝗼𝗻𝗴 𝗡𝗮𝗺𝗲) - 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗦𝗼𝗻𝗴 𝗙𝗿𝗼𝗺 𝗜𝗻𝗹𝗶𝗻𝗲 𝗠𝗼𝗱𝗲

🎧 [ 𝐁𝐀𝐙𝐈𝐆𝐀𝐑 𝐌𝐔𝐒𝐈𝐂 𝐁𝐎𝐓 ]

/cplay - 𝗦𝘁𝗿𝗲𝗮𝗺 𝗠𝘂𝘀𝗶𝗰 𝗢𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗩𝗼𝗶𝗰𝗲 𝗖𝗵𝗮𝘁
/cplayer - 𝗦𝗵𝗼𝘄 𝗧𝗵𝗲 𝗦𝗼𝗻𝗴 𝗜𝗻 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴
/cpause - 𝗣𝗮𝘂𝘀𝗲 𝗧𝗵𝗲 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗠𝘂𝘀𝗶𝗰
/cresume - 𝗥𝗲𝘀𝘂𝗺𝗲 𝗧𝗵𝗲 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗪𝗮𝘀 𝗣𝗮𝘂𝘀𝗲𝗱
/cskip - 𝗦𝗸𝗶𝗽 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗧𝗼 𝗧𝗵𝗲 𝗡𝗲𝘅𝘁 𝗦𝗼𝗻𝗴
/cend - 𝗘𝗻𝗱 𝗧𝗵𝗲 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴 𝗠𝘂𝘀𝗶𝗰
/refresh - 𝗥𝗲𝗳𝗿𝗲𝘀𝗵 𝗧𝗵𝗲 𝗔𝗱𝗺𝗶𝗻 𝗖𝗮𝗰𝗵𝗲
/ubjoinc - 𝗜𝗻𝘃𝗶𝘁𝗲 𝗧𝗵𝗲 𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗙𝗼𝗿 𝗝𝗼𝗶𝗻 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗖𝗵𝗮𝗻𝗻𝗲𝗹

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌸ʙᴀᴄᴋ", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>👑 𝗛𝗲𝗿𝗲 𝗜𝘀 𝗧𝗵𝗲 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀</b>

/start (𝗜𝗻 𝗚𝗿𝗼𝘂𝗽) - 𝗦𝗲𝗲 𝗧𝗵𝗲 𝗕𝗼𝘁 𝗔𝗹𝗶𝘃𝗲 𝗦𝘁𝗮𝘁𝘂𝘀
/reload - 𝗥𝗲𝗹𝗼𝗮𝗱 𝗕𝗼𝘁 𝗔𝗻𝗱 𝗥𝗲𝗳𝗿𝗲𝘀𝗵 𝗧𝗵𝗲 𝗔𝗱𝗺𝗶𝗻 𝗟𝗶𝘀𝘁
/ping - 𝗖𝗵𝗲𝗰𝗸 𝗧𝗵𝗲 𝗕𝗼𝘁 𝗣𝗶𝗻𝗴 𝗦𝘁𝗮𝘁𝘂𝘀
/uptime - 𝗖𝗵𝗲𝗰𝗸 𝗧𝗵𝗲 𝗕𝗼𝘁 𝗨𝗽𝘁𝗶𝗺𝗲 𝗦𝘁𝗮𝘁𝘂𝘀
/id - 𝗦𝗵𝗼𝘄 𝗧𝗵𝗲 𝗚𝗿𝗼𝘂𝗽/𝗨𝘀𝗲𝗿 𝗜𝗱 & 𝗢𝘁𝗵𝗲𝗿

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌸ʙᴀᴄᴋ", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>👑 𝗛𝗲𝗿𝗲 𝗜𝘀 𝗧𝗵𝗲 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀</b>

/player - 𝗦𝗵𝗼𝘄 𝗧𝗵𝗲 𝗠𝘂𝘀𝗶𝗰 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 𝗦𝘁𝗮𝘁𝘂𝘀
/pause - 𝗣𝗮𝘂𝘀𝗲 𝗧𝗵𝗲 𝗠𝘂𝘀𝗶𝗰 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴
/resume - 𝗥𝗲𝘀𝘂𝗺𝗲 𝗧𝗵𝗲 𝗠𝘂𝘀𝗶𝗰 𝗪𝗮𝘀 𝗣𝗮𝘂𝘀𝗲𝗱
/skip - 𝗦𝗸𝗶𝗽 𝗧𝗼 𝗧𝗵𝗲 𝗡𝗲𝘅𝘁 𝗦𝗼𝗻𝗴
/end - 𝗦𝘁𝗼𝗽 𝗠𝘂𝘀𝗶𝗰 𝗦𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴
/join - 𝗜𝗻𝘃𝗶𝘁𝗲 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗝𝗼𝗶𝗻 𝗧𝗼 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽
/leave - 𝗢𝗿𝗱𝗲𝗿 𝗧𝗵𝗲 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗧𝗼 𝗟𝗲𝗮𝘃𝗲 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽
/auth - 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗨𝘀𝗲𝗿 𝗙𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗠𝘂𝘀𝗶𝗰 𝗕𝗼𝘁
/deauth - 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗙𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗠𝘂𝘀𝗶𝗰 𝗕𝗼𝘁
/control - 𝗢𝗽𝗲𝗻 𝗧𝗵𝗲 𝗣𝗹𝗮𝘆𝗲𝗿 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 𝗣𝗮𝗻𝗲𝗹
/delcmd (𝗢𝗻 | 𝗢𝗳𝗳) - 𝗘𝗻𝗮𝗯𝗹𝗲 / 𝗗𝗶𝘀𝗮𝗯𝗹𝗲 𝗗𝗲𝗹 𝗖𝗺𝗱 𝗙𝗲𝗮𝘁𝘂𝗿𝗲
/musicplayer (𝗢𝗻 / 𝗢𝗳𝗳) - 𝗗𝗶𝘀𝗮𝗯𝗹𝗲 / 𝗘𝗻𝗮𝗯𝗹𝗲 𝗠𝘂𝘀𝗶𝗰 𝗣𝗹𝗮𝘆𝗲𝗿 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌸ʙᴀᴄᴋ", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>👑 𝗛𝗲𝗿𝗲 𝗜𝘀 𝗧𝗵𝗲 𝗦𝘂𝗱𝗼 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀</b>

/leaveall - order the assistant to leave from all group
/stats - show the bot statistic
/rmd - remove all downloaded files

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌸ʙᴀᴄᴋ", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>👑 𝗛𝗲𝗿𝗲 𝗜𝘀 𝗧𝗵𝗲 𝗢𝘄𝗻𝗲𝗿 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀</b>

/stats - 𝗦𝗵𝗼𝘄 𝗧𝗵𝗲 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰
/broadcast - 𝗦𝗲𝗻𝗱 𝗔 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁
/block (𝗨𝘀𝗲𝗿 𝗜𝗱 - 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 - 𝗥𝗲𝗮𝘀𝗼𝗻) - 𝗕𝗹𝗼𝗰𝗸 𝗨𝘀𝗲𝗿 𝗙𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗬𝗼𝘂𝗿 𝗕𝗼𝘁
/unblock (𝗨𝘀𝗲𝗿 𝗜𝗱 - 𝗥𝗲𝗮𝘀𝗼𝗻) - 𝗨𝗻𝗯𝗹𝗼𝗰𝗸 𝗨𝘀𝗲𝗿 𝗬𝗼𝘂 𝗕𝗹𝗼𝗰𝗸𝗲𝗱 𝗙𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗬𝗼𝘂𝗿 𝗕𝗼𝘁
/blocklist - 𝗦𝗵𝗼𝘄 𝗬𝗼𝘂 𝗧𝗵𝗲 𝗟𝗶𝘀𝘁 𝗢𝗳 𝗨𝘀𝗲𝗿 𝗪𝗮𝘀 𝗕𝗹𝗼𝗰𝗸𝗲𝗱 𝗙𝗼𝗿 𝗨𝘀𝗶𝗻𝗴 𝗬𝗼𝘂𝗿 𝗕𝗼𝘁

📝 note: ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ᴡᴏʀᴋɪɴɢ ᴜsᴇ ᴀɴᴅ ᴇɴᴊᴏʏ.

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌸ᴄʟᴏsᴇ", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ 𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗕𝗢𝗧:

1.) ғɪʀsᴛ, ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
2.) ᴛʜᴇɴ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴀɴᴅ ɢɪᴠᴇ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs ᴇxᴄᴇᴘᴛ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.
3.) ᴀᴅᴅ @{ASSISTANT_NAME} ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴛʏᴘᴇ /userbotjoin ᴛᴏ ɪɴᴠɪᴛᴇ ʜᴇʀ.
4.) ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ ʙᴇғᴏʀᴇ sᴛᴀʀᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📚𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦", callback_data="cbhelp")],
                [InlineKeyboardButton("🌸ᴄʟᴏsᴇ", callback_data="close")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
@cb_admin_check
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        "**💡 here is the control menu of bot :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔶ᴘᴀᴜsᴇ", callback_data="cbpause"),
                    InlineKeyboardButton("🔶ʀᴇsᴜᴍᴇ", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("🔶sᴋɪᴘ", callback_data="cbskip"),
                    InlineKeyboardButton("🔶sᴛᴏᴘ", callback_data="cbend"),
                ],
                [InlineKeyboardButton("🔶ᴀɴᴛɪ ᴄᴍᴅ", callback_data="cbdelcmds")],
                [InlineKeyboardButton("🔶ᴄʟᴏsᴇ", callback_data="close")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
@cb_admin_check
@authorized_users_only
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>this is the feature information :</b>
        
**💡 Feature:** delete every commands sent by users to avoid spam in groups !

❔ usage:**

 1️⃣ to turn on feature:
     » type `/delcmd on`
    
 2️⃣ to turn off feature:
     » type `/delcmd off`
      
⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌸ʙᴀᴄᴋ", callback_data="cbback")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>💡 𝗛𝗘𝗟𝗟𝗢 𝗗𝗘𝗔𝗥 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗛𝗘𝗟𝗣 𝗠𝗘𝗡𝗨 !</b>

» **𝗜𝗻 𝗧𝗵𝗶𝘀 𝗠𝗲𝗻𝘂 𝗬𝗼𝘂 𝗖𝗮𝗻 𝗢𝗽𝗲𝗻 𝗦𝗲𝘃𝗲𝗿𝗮𝗹 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗠𝗲𝗻𝘂𝘀, 𝗜𝗻 𝗘𝗮𝗰𝗵 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗠𝗲𝗻𝘂 𝗧𝗵𝗲𝗿𝗲 𝗜𝘀 𝗔𝗹𝘀𝗼 𝗔 𝗕𝗿𝗶𝗲𝗳 𝗘𝘅𝗽𝗹𝗮𝗻𝗮𝘁𝗶𝗼𝗻 𝗢𝗳 𝗘𝗮𝗰𝗵 𝗖𝗼𝗺𝗺𝗮𝗻𝗱**

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🌸ʙᴀsɪᴄ", callback_data="cbbasic"),
                    InlineKeyboardButton("🌸ᴀᴅᴠᴀɴᴄᴇ", callback_data="cbadvanced"),
                ],
                [
                    InlineKeyboardButton("🌸ᴀᴅᴍɪɴ", callback_data="cbadmin"),
                    InlineKeyboardButton("🌸sᴜᴅᴏ", callback_data="cbsudo"),
                ],
                [InlineKeyboardButton("🌸ᴏᴡɴᴇʀ", callback_data="cbowner")],
                [InlineKeyboardButton("🌸ʙᴀᴄᴋ", callback_data="cbstart")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ 𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘 𝗢𝗨𝗥 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧:

1.) 🌸ғɪʀsᴛ, ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
2.) 🌸ᴛʜᴇɴ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ᴀɴᴅ ɢɪᴠᴇ ᴀʟʟ ᴘᴇʀᴍɪssɪᴏɴs ᴇxᴄᴇᴘᴛ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.
3.) 🌸ᴀᴅᴅ @{ASSISTANT_NAME} ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴛʏᴘᴇ /userbotjoin ᴛᴏ ɪɴᴠɪᴛᴇ ʜᴇʀ.
4.) 🌸ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғɪʀsᴛ ʙᴇғᴏʀᴇ sᴛᴀʀᴛ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.

⚡ __ᴘᴏᴡᴇʀᴅ ʙʏ ʙᴀᴢɪɢᴀʀ ʙᴏᴛs__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🌸ʙᴀᴄᴋ", callback_data="cbstart")]]
        ),
    )
