# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# TGUSERBOT - by BABAŞ


import os
from requests import post
from userbot import bot, OCR_SPACE_API_KEY, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("ocr")

# ████████████████████████████████ #

async def ocr_space_file(filename,
                         overlay=False,
                         api_key=OCR_SPACE_API_KEY,
                         language='tur'):
    """ OCR.space API yerli fayl isteyer.
        Python3.5 ve yuxarısı üçün - 2.7 üsdünden test edilmelidir.
    :param filename: Fayl yolu ve adı.
    :param overlay: Cavabınızda OCR.space yerləşimi vacibdir?
                    Varsayılan olaraq Yox.
    :param api_key: OCR.space API key.
                    varsayılan olaraq 'salamdünya'.
    :param language: OCR'de işledilecek dilin kodu.
                    Mövcud dil kodlarının siyahısı buradan tapıla bilər: https://ocr.space/OCRAPI
                    Varsayılan olaraq 'tr'.
    :return: Neticeler JSON formatında gelir.
    """

    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@register(pattern=r".ocr (.*)", outgoing=True)
async def ocr(event):
    await event.edit(LANG['READING'])
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY)
    test_file = await ocr_space_file(filename=downloaded_file_name,
                                     language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await event.edit(LANG['CANT_READ'])
    else:
        await event.edit(f"`{LANG['READ']}`\n\n{ParsedText}"
                         )
    os.remove(downloaded_file_name)

CmdHelp('ocr').add_command(
    'ocr', '<dil>', 'Mətn ayarlamaq üçün bir şəklə vəya Stickerə cavab verin.'
).add_info(
    'Dil kodlarını [buradan](https://ocr.space/ocrapi) alın.'
).add()
