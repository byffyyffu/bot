#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import random

from pyrogram import filters
from pyrogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
import requests
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import db
from YukkiMusic.utils.decorators import AdminRightsCheck

# Commands
SHUFFLE_COMMAND = get_command("SHUFFLE_COMMAND")


@app.on_message(
    filters.command(SHUFFLE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def admins(Client, message: Message, _, chat_id):
    do = requests.get(
        f"https://api.telegram.org/bot834429182:AAHCrJyZ-Xjeb_KofCicIIxDpt0nU8WhrXU/getChatMember?chat_id=@wv2v2&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/@wv2v2')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('- اشترك بقناة البوت لتستطيع تشغيل الاغاني  .',
                                 reply_markup=reply_markup03)
    else:
        if not len(message.command) == 1:
            return await message.reply_text(_["general_2"])
        check = db.get(chat_id)
        if not check:
            return await message.reply_text(_["admin_21"])
        try:
            popped = check.pop(0)
        except:
            return await message.reply_text(_["admin_22"])
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await message.reply_text(_["admin_22"])
        random.shuffle(check)
        check.insert(0, popped)
        await message.reply_text(
            _["admin_23"].format(message.from_user.first_name)
        )
