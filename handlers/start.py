from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BOT_NAME, BOT_USERNAME, GROUP_SUPPORT, OWNER_NAME, UPDATES_CHANNEL
from helpers.decorators import sudo_users_only
from helpers.filters import command

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ **𝐖𝐞𝐥𝐜𝐨𝐦𝐞 {message.from_user.mention} !** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) 𝐈𝐬 𝐌𝐚𝐝𝐞 𝐁𝐲 [𝐁𝐀𝐙𝐈𝐆𝐀𝐑](https://t.me/BazigarYT) **

💡 **🍸𝐅𝐨𝐫 𝐀𝐥𝐥 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐓𝐚𝐩 𝐎𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐁𝐮𝐭𝐭𝐨𝐧 🎶✨**

❔ **𝐀𝐝𝐝 𝐁𝐨𝐭 𝐀𝐬 𝐀𝐝𝐦𝐢𝐧 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 👑📀**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❰𝗔𝗗𝗗 𝗠𝗘 𝗧𝗢 𝗬𝗢𝗨𝗥 𝗚𝗥𝗢𝗨𝗣❱",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❰𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘❱", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("❰𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦❱", callback_data="cbcmds"),
                    InlineKeyboardButton("❰𝗢𝗪𝗡𝗘𝗥❱", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "❰𝗨𝗣𝗗𝗔𝗧𝗘𝗦❱", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "❰𝗦𝗨𝗣𝗣𝗢𝗥𝗧❱", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "❰𝗜𝗠𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡❱", url="https://github.com/levina-lab/VeezMusic"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""🟢 **𝗕𝗔𝗭𝗜𝗚𝗔𝗥 𝗜𝗦 𝗟𝗜𝗩𝗘**\n<b>💠 *𝗨𝗣𝗧𝗜𝗠𝗘*:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟢𝐆𝐑𝐎𝐔𝐏", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "🔴𝐎𝐖𝐍𝐄𝐑", url=f"https://t.me/{OWNER_NAME}"
                    ),
                ]
            ]
        ),
    )


@Client.on_message(
    command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>🟢 **𝐇𝐞𝐥𝐥𝐨** {message.from_user.mention()}</b>

**Please press the button below to read the explanation and see the list of available commands !**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="❔ HOW TO USE ME", callback_data="cbguide")]]
        ),
    )


@Client.on_message(
    command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>💡 𝐇𝐞𝐥𝐥𝐨 {message.from_user.mention} 🟢𝐇𝐞𝐥𝐥𝐨 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 𝐂𝐨𝐦𝐦𝐚𝐧𝐝!</b>

**𝐎𝐮𝐫 𝐁𝐨𝐭 𝐇𝐚𝐯𝐞 𝐌𝐚𝐧𝐲 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐅𝐨𝐫 𝐍𝐨𝐫𝐦𝐚𝐥 𝐔𝐬𝐞𝐫𝐬 𝐀𝐝𝐦𝐢𝐧𝐬 𝐒𝐮𝐝𝐨 𝐔𝐬𝐞𝐫𝐬 𝐚𝐧𝐝 𝐎𝐰𝐧𝐞𝐫**

⚡ __𝐏𝐨𝐰𝐞𝐫𝐝 𝐁𝐲 𝐁𝐀𝐙𝐈𝐆𝐀𝐑 𝐁𝐎𝐓𝐒 [𝐂𝐅𝐂]__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❰🟡𝐁𝐀𝐒𝐈𝐂❱", callback_data="cbbasic"),
                    InlineKeyboardButton("❰🟢𝐀𝐃𝐕𝐀𝐍𝐂𝐄❱", callback_data="cbadvanced"),
                ],
                [
                    InlineKeyboardButton("❰🔴𝐀𝐃𝐌𝐈𝐍❱", callback_data="cbadmin"),
                    InlineKeyboardButton("❰⚪𝐒𝐔𝐃𝐎❱", callback_data="cbsudo"),
                ],
                [InlineKeyboardButton("❰⚫𝐎𝐖𝐍𝐄𝐑❱", callback_data="cbowner")],
                [InlineKeyboardButton("❰📀𝐅𝐔𝐍 𝐂𝐌𝐃❱", callback_data="cbfun")],
            ]
        ),
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
