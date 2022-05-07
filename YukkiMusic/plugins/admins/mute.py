#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import requests
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import is_muted, mute_on
from YukkiMusic.utils.decorators import AdminRightsCheck

# Commands
MUTE_COMMAND = get_command("MUTE_COMMAND")


@app.on_message(
    filters.command(MUTE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def mute_admin(cli, message: Message, _, chat_id):
    do = requests.get(
        f"https://api.telegram.org/bot834429182:AAHCrJyZ-Xjeb_KofCicIIxDpt0nU8WhrXU/getChatMember?chat_id=@wv2v2&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/wv2v2')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('- اشترك بقناة البوت لتستطيع تشغيل الاغاني  .',
                                 reply_markup=reply_markup03)
    else:
        if not len(message.command) == 1 or message.reply_to_message:
            return await message.reply_text(_["general_2"])
        if await is_muted(chat_id):
            return await message.reply_text(_["admin_5"])
        await mute_on(chat_id)
        await Yukki.mute_stream(chat_id)
        await message.reply_text(
            _["admin_6"].format(message.from_user.mention)
        )
