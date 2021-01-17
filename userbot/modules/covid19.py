# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# TGUSERBOT - by BABAŞ

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("covid19")

# ████████████████████████████████ #

from userbot import CMD_HELP
from userbot.events import register
from requests import get
import pytz
import flag
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.covid ?(.*)$")
async def covid(event):
    try:
        if event.pattern_match.group(1) == '':
            country = 'AZ'
        else: 
            country = event.pattern_match.group(1)

        bayrak = flag.flag(country)
        worldData = get('https://coronavirus-19-api.herokuapp.com/all').json()
        countryData = get('https://coronavirus-19-api.herokuapp.com/countries/' + pytz.country_names[country]).json()
    except:
        await event.edit(LANG['SOME_ERRORS'])
        return

    sonuclar = (f"** {LANG['DATA']}**\n" +
                f"\n**{LANG['EARTH']}**\n" +
                f"**{LANG['CASE']}** `{worldData['cases']}`\n" +
                f"**{LANG['DEATH']}** `{worldData['deaths']}`\n" +
                f"**{LANG['HEAL']}** `{worldData['recovered']}`\n" +
                f"\n**{pytz.country_names[country]}**\n" +
                f"**{bayrak} {LANG['AZ_ALL_CASES']}** `{countryData['cases']}`\n" +
                f"**{bayrak} {LANG['AZ'CASES']}** `{countryData['todayCases']}`\n" +
                f"**{bayrak} {LANG['AZ_CASE']}** `{countryData['active']}`\n" +
                f"**{bayrak} {LANG['AZ_ALL_DEATHS']}** `{countryData['deaths']}`\n" +
                f"**{bayrak} {LANG['AZ_DEATHS']}** `{countryData['todayDeaths']}`\n" +
                f"**{bayrak} {LANG['AZ_HEAL']}** `{countryData['recovered']}`\n" +
                f"**{bayrak} Test Sayı:** `{countryData['totalTests']}`"
                )
    await event.edit(sonuclar)

CmdHelp('covid19').add_command(
    'covid', '<ölkə kodu>', 'Həm Dünya geneli həm də verdiyiniz ölkə üçün güncəl Covid 19 statistikası. Ölkəniz fərqlidirsə komandanın yanına əlavə etməyiniz bəsdir.',
    'covid tr -> Türkiyəni gətirər.'
).add_warning('`Ölkə yazmasanız Azərbaycanı seçər.`').add()
