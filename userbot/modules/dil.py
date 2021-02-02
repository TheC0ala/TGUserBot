# Copyright (C) 2020 
#
# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# USERLAND - by BABAŞ #

from userbot.cmdhelp import CmdHelp
from userbot import PLUGIN_CHANNEL_ID, CMD_HELP
from userbot.events import register
from re import search
from json import loads, JSONDecodeError
from userbot.language import LANGUAGE_JSON
from os import remove

@register(outgoing=True, pattern="^.dil ?(.*)")
@register(outgoing=True, pattern="^.lang ?(.*)")
async def dil(event):
    global LANGUAGE_JSON

    komut = event.pattern_match.group(1)
    if search(r"y[uü]kle|install", komut):
        await event.edit("`Dil faylı yüklənir... Zəhmət olmasa gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            dosya = await reply.download_media()

            if ((len(reply.file.name.split(".")) >= 2) and (not reply.file.name.split(".")[1] == "ddqjson")):
                return await event.edit("`Zəhmət olmasa keçərli` **DDQJSON** `faylı verin!`")

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Zəhmət olmasa keçərli` **DDQJSON** `faylı verin!`")

            await event.edit(f"`{dosya['LANGUAGE']}` `dili yüklənir...`")
            pchannel = await event.client.get_entity(PLUGIN_CHANNEL_ID)

            dosya = await reply.download_media(file="./userbot/language/")
            dosya = loads(open(dosya, "r").read())
            await reply.forward_to(pchannel)
            
            LANGUAGE_JSON = dosya
            await event.edit(f"✅ `{dosya['LANGUAGE']}` `dili uğurla yükləndi!`\n\n**Əməliyyatların keçərli olması üçün botu yenidən başladın!**")
        else:
            await event.edit("**Zəhmət olmasa bir dil faylına cavab verin!**")
    elif search(r"bilgi|info", komut):
        await event.edit("`Dil faylının məlumatları gətirilir... Zəhmət olmasa gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            if ((len(reply.file.name.split(".")) >= 1) and (not reply.file.name.split(".")[1] == "ddqjson")):
                return await event.edit("`Zəhmət olmasa keçərli` **DDQJSON** `faylı verin!`")

            dosya = await reply.download_media()

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Zəhmət olmasa keçərli` **DDQJSON** `faylı verin!`")

            await event.edit(
                f"**Dil: **`{dosya['LANGUAGE']}`\n"
                f"**Dil Kodu: **`{dosya['LANGCODE']}`\n"
                f"**Çevirən: **`{dosya['AUTHOR']}`\n"

                f"\n\n`Dil faylını yükləmək üçün` `.dil yüklə` `komandasını işlədin.`"
            )
        else:
            await event.edit("**Zəhmət olmasa bir dil faylına cavab verin!**")
    else:
        await event.edit(
            f"**Dil: **`{LANGUAGE_JSON['LANGUAGE']}`\n"
            f"**Dil Kodu: **`{LANGUAGE_JSON['LANGCODE']}`\n"
            f"**Çevirən: **`{LANGUAGE_JSON ['AUTHOR']}`\n"

            f"\n\n@UserLandResmi ✨"
        )

CmdHelp('dil').add_command(
    'dil', None, 'Yüklədiyiniz dil faylı haqqında məlumat.'
).add_command(
    'dil melumat', None, 'Cavab verdiyiniz dil faylı haqqında məlumat verər.'
).add_command(
    'dil yüklə', None, 'Cavab verdiyiniz dil faylını yükləyər.'
).add()
