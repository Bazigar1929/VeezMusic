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
        f"""<b>🙋‍♂️ **𝗪𝗲𝗹𝗰𝗼𝗺𝗲 {message.from_user.first_name}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) 𝗔𝗹𝗹𝗼𝘄𝘀 𝗬𝗼𝘂 𝗧𝗼 𝗣𝗹𝗮𝘆 𝗠𝘂𝘀𝗶𝗰 𝗢𝗻 𝗚𝗿𝗼𝘂𝗽𝘀 𝗧𝗵𝗿𝗼𝘂𝗴𝗵 𝗧𝗵𝗲 𝗡𝗲𝘄 𝘁𝗲𝗹𝗲𝗴𝗿𝗮𝗺'𝘀 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁𝘀!**

💡 **𝗳𝗶𝗻𝗱 𝗼𝘂𝘁 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗯𝗼𝘁'𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗮𝗻𝗱 𝗵𝗼𝘄 𝘁𝗵𝗲𝘆 𝘄𝗼𝗿𝗸 𝗯𝘆 𝗰𝗹𝗶𝗰𝗸𝗶𝗻𝗴 𝗼𝗻 𝘁𝗵𝗲 » 📚 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗯𝘂𝘁𝘁𝗼𝗻!**

❔ **𝘁𝗼 𝗸𝗻𝗼𝘄 𝗵𝗼𝘄 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗰𝗹𝗶𝗰𝗸 𝗼𝗻 𝘁𝗵𝗲 » ❓ 𝗯𝗮𝘀𝗶𝗰 𝗴𝘂𝗶𝗱𝗲 𝗯𝘂𝘁𝘁𝗼𝗻!**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂", callback_data="cbcmds"),
                    InlineKeyboardButton(
                        "𝙰𝙳𝙳 𝙼𝙴 𝙸𝙽 𝙶𝚁𝙾𝚄𝙿",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "𝚂𝚄𝙿𝙿𝙾𝚁𝚃", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "𝚄𝙿𝙳𝙰𝚃𝙴𝚂", url=f"https://t.me/{UPDATES_CHANNEL}"
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
        f"""🟢 **𝗡𝗢𝗜𝗡𝗢𝗜 𝗜𝗦 𝗟𝗜𝗩𝗘**\n<b>💠 **𝗨𝗣𝗧𝗜𝗠𝗘:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨𝙶𝚁𝙾𝚄𝙿", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "✨𝙾𝚆𝙽𝙴𝚁", url=f"https://t.me/{𝙾𝚆𝙽𝙴𝚁_𝙽𝙰𝙼𝙴}"
                    ),
                ]
            ]
        ),
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 `𝙹𝙾 𝙷𝚄𝙺𝚄𝙼 𝙼𝙴𝚁𝙴 𝙰𝙰𝙽𝙺𝙰!!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🌸𝙲𝙵𝙲 𝙱𝙾𝚃 𝚂𝚃𝙰𝚄𝚃𝚂:\n"
        f"• **𝚄𝙿𝚃𝙸𝙼𝙴:** `{uptime}`\n"
        f"• **𝚂𝚃𝙰𝚁𝚃 𝚃𝙸𝙼𝙴:** `{START_TIME_ISO}`"
    )
