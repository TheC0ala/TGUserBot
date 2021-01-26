# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# TGUSERBOT - by BABAŞ #

from asyncio import sleep
from random import choice, getrandbits, randint
from re import sub
import time
import asyncio

from collections import deque

import requests

from cowpy import cow

from userbot import CMD_HELP, ZALG_LIST
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot.cmdhelp import CmdHelp

# ================= CONSTANT =================
EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNS_STR = [
    "Hey! Hara Gedirsən?",
    "Nəə? qaçdılar?",
    "ZZzzZZzz... Noldu? yenə onlar imiş, boş ver.",
    "Geri gəl!",
    "Qaçın OneBot gəlir!!",
    "Divara diqqət elə!",
    "Məni onlarla tək qoymaa!!",
    "Qaçarsan ölərsən.",
    "Zarafatcıl səni, mən hər yerdəyəm.",
    "Bunu elədiyinə peşman olacaqsan...",
    "/kickme düyməsinidə yoxlaya bilərsən, Əyləncəli olduğunu deyirlər.",
    "Get başqa birini narahat elə, burda kimsə vecinə almır.",
    "Qaça bilərsən amma gizlənə bilməssən.",
    "Edə bildiklərin bu qədərdi?",
    "Arxandayam...",
    "Qonaqların var!",
    "Bunu asan yoldan həll edə bilərik, vəya çətin yoldan.",
    "Anlamırsan hə?",
    "Haha, qaçsan yaxşı olar!",
    "Zəhmət olmasa, xatırlat mənə nə qədər vecimdəsən?",
    "Sənin yerində olsam daha sürətli qaçardım.",
    "Bu axtardığımız robotdur.",
    "Bəlmə bəxt sənə gülər.",
    "Məşhur son sözlər.",
    "Və sonsuza qədər yox oldular, heç görünmədilər.",
    "\"Hey, mənə baxın! Bottan qaça bilirəm çox coolam😎!\" - bu şəxs",
    "Hə Hə, 👉 /kickme 👈 bas.",
    "Bu üzüyü alın və Mordor'a gedin.",
    "Əfsanayə görə onlar hələdə işləyirlər...",
    "Harry Potter'ın əksinə, valideyinlətin səni məndən qoruya bilməz.",
    "Qorxu əsəbə, Əsəb nifrətə, nifrət acıya yol açar. Qorxu içində qaçmağa davam etsən,"
    "bir sonrakı Vader sən ola bilərsən.",
    "Əfsanəyə görə onlar hələdə işləyirlər.",
    "Davam elə, səni burda istədiyimizə əmin deyiləm.",
    "Sən bir sihirb- Oh. Gözlə. Sən Harry deyilsən, davam elə.",
    "KORİDORDA QAÇMAYINN!",
    "Görüşərik.",
    "Kim itləri buraxd?",
    "Gülməlidir çün ki heç kim vecinə almır.",
    "Ah, nə böyük itki. Bu səfərkini sevmişdim.",
    "Açıqcası vecimdə deyil.",
    "Həqiqəti QALDIRA BİLMƏSSƏN!",
    "Uzun zaman əvvəl, çox çox uzaqdakı bir qalaksiya biriləri vecinə ala bilərdi. Amma artıq yox.",
    "Hey, onlara bax! Qaçınılmaz banhammer'dan qaçırlar... Nə qədərdə şirin.",
    "Ağ dovşanın, arxasında nə edirsən!?",
    "Həkimində dediyi kimi... QAÇ!",
]

HELLOSTR = [
    "Salaamm",
    "‘Nə var nə yox Müdür!",
    "Necəsən?",
    "‘Hey Nolub?",
    "Salam! Salam! Salam!",
    "Salam, kim var orda!?, Mən danışıram.",
    "Bunun kim olduğunu bilirsən",
    "Hey Yo!",
    "Nətərsən",
    "Salamlar və Salamlar!",
    "Salam, gün işığı!",
    "Hey, nətərsən, salam!",
    "Necə gedir’, balaca cücə?",
    "Bööö!",
    "Salam, birinci sinif uşağı!",
    "Barışaq!",
    "Salam, dostum!",
    "Salam!",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES = [
    "{victim} isdifadəçisini {item} ilə {hits} .",
    "{victim} isdifadəçisini {item} ilə üzünə {hits} .",
    "{victim} isdifadəçisini {item} iə biraz {hits} .",
    "{victim} isdifadəçisinə {item} {throws} .",
    "{victim} isdifadəçisini {item} ile yüzüne {throws} .",
    "{victim} isdifadəçisinə tərəf {item} atır.",
    "{victim} axmaqına {item} ilə şillə vurur.",
    "{victim} isdifadəçisini yerə sabitləyib arxa arxaya {item} ilə {hits} .",
    "{item} alaraq {victim} {hits}.",
    "{victim} isdifadəçisini stola bağlayıb {item} {throws} .",
    "{victim} isdifadəçisini dostca itələyərək lavada üzməyi örgənməsini istəyir."
]

ITEMS = [
    "dəmir tava",
    "böyük alabalığ",
    "beyzbol çubuğu",
    "kriket çubuğu",
    "taxta",
    "mismar",
    "yazıcı",
    "kürək",
    "tüplü monitor",
    "fizik dəftəri",
    "tost maşını",
    "Mona Liza portreti",
    "televizor",
    "beş ton kamaz",
    "kitab",
    "dizüstü kompüter",
    "iPhone 11 Pro",
    "plastik toyuq",
    "mismarlı çubuğ",
    "yanğın söndürücü",
    "kubik",
    "kir yığını",
    "arı pətəyi",
    "çürük ət",
    "fil",
    "kola",
]

THROW = [
    "atır",
    "tullayır",
    "fırladır",
    "yağdırır",
]

HIT = [
    "vurur",
    "möhkəm vurur",
    "şillələyir",
    "yumruqlayır",
    "keçirir",
]

# ===========================================

@register(outgoing=True, pattern="^.heyvan ?(.*)")
async def hayvan(e):
    arg = e.pattern_match.group(1)
    if arg == "pişik":
        args = "cat"
    elif arg == "it":
        args = "dog"
    elif arg == "quş":
        args = "birb"
    elif arg == "qurd":
        args = "fox"
    elif arg == "panda":
        args = "panda"
    else:
        arg = "pişik"
        args = "cat"

    foto = requests.get(f'https://some-random-api.ml/img/{args}').json()["link"]
    await e.delete()
    await e.client.send_message(
        e.chat_id,
        f"`Təsadüfi {arg} şəkli\n@UserBotTG`",
        file=foto
    )

@register(outgoing=True, pattern="^.qerar$")
async def karar(e):
    msaj = ""
    if e.reply_to_msg_id:
        rep = await e.get_reply_message()
        replyto = rep.id
        msaj += f"[Dostum](tg://user?id={rep.from_id}), "
    else:
        e.edit("`Zəhmət olmasa bir mesaja cavab verin.`")
        return
    yesno = requests.get('https://yesno.wtf/api').json()
    if yesno["answer"] == "yes":
        cevap = "hə"
    else:
        cevap = "yox"
    msaj += f"Deyəsən buna {cevap} deyəcəm."

    await e.delete()
    await e.client.send_message(
        e.chat_id,
        msaj,
        reply_to=replyto,
        file=yesno["image"]
    )

@register(outgoing=True, pattern=r"^.(\w+)say (.*)")
async def univsaye(cowmsg):
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern="^:/$", ignore_unsafe=True)
async def kek(keks):
    """ Kendinizi kontrol edin ;)"""
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await keks.edit(":" + uio[i % 2])


@register(pattern="^.vur(?: |$)(.*)", outgoing=True)
async def who(event):
    replied_user = await get_user_from_event(event)
    if replied_user:
        replied_user = replied_user[0]
    else:
        return
    caption = await slap(replied_user, event)

    try:
        await event.edit(caption)

    except BaseException:
        await event.edit(
            "`Bu isidfadəçini vura bilmərəm, yanıma çubuq və daş almalıyam!!`"
        )


async def slap(replied_user, event):
    user_id = replied_user.id
    first_name = replied_user.first_name
    username = replied_user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = choice(SLAP_TEMPLATES)
    item = choice(ITEMS)
    hit = choice(HIT)
    throw = choice(THROW)

    caption = "@UserBotTG " + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw)

    return caption


@register(outgoing=True, pattern="^-_-$", ignore_unsafe=True)
async def lol(lel):
    """ Tm """
    okay = "-_-"
    for i in range(10):
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@register(outgoing=True, pattern="^;_;$", ignore_unsafe=True)
async def fun(e):
    t = ";_;"
    for j in range(10):
        t = t[:-1] + "_;"
        await e.edit(t)


@register(outgoing=True, pattern="^.utan$")
async def facepalm(e):
    await e.edit("🤦‍♂")


@register(outgoing=True, pattern="^.agla$")
async def cry(e):
    await e.edit(choice(CRI))


@register(outgoing=True, pattern="^.cp(?: |$)(.*)")
async def copypasta(cp_e):
    """ salam """
    textx = await cp_e.get_reply_message()
    message = cp_e.pattern_match.group(1)

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await cp_e.edit("`😂Mənə💯BIR✌️mE🅱️In👐Ver👏`")
        return

    reply_text = choice(EMOJIS)
    b_char = choice(message).lower()
    for owo in message:
        if owo == " ":
            reply_text += choice(EMOJIS)
        elif owo in EMOJIS:
            reply_text += owo
            reply_text += choice(EMOJIS)
        elif owo.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(getrandbits(1)):
                reply_text += owo.upper()
            else:
                reply_text += owo.lower()
    reply_text += choice(EMOJIS)
    await cp_e.edit(reply_text)


@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
async def vapor(vpr):
    reply_text = list()
    textx = await vpr.get_reply_message()
    message = vpr.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await vpr.edit("`Mənə Bir Mətn Ver!`")
        return

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await vpr.edit("".join(reply_text))


@register(outgoing=True, pattern="^.str(?: |$)(.*)")
async def stretch(stret):
    textx = await stret.get_reply_message()
    message = stret.text
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await stret.edit("`Mənəəəəə Biiiiiiirr Mətnnnnnnn Verrrr!`")
        return

    count = randint(3, 10)
    reply_text = sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                     message)
    await stret.edit(reply_text)


@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
async def zal(zgfy):
    """ Kaos """
    reply_text = list()
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await zgfy.edit(
            "`Ｂ̺ͬａ̠͑ｎ̵̉ａ̬͜ ｂ̶͔ｉ̼͚ｒ͈͞ ｍ̼͘ｅ̨̝ｔ͔͙ｉ̢ͮｎ̜͗ ｖ͢͜ｅ̗͐ｒ̴ͮ`"
        )
        return

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(0, 3):
            charac += choice(ZALG_LIST[randint(0,2)]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))
    

@register(outgoing=True, pattern="^.salam$")
async def hoi(hello):
    await hello.edit(choice(HELLOSTR))


@register(outgoing=True, pattern="^.owo(?: |$)(.*)")
async def faces(owo):
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await owo.edit("` UwU mənə bir mətn ver! `")
        return

    reply_text = sub(r"(r|l)", "w", message)
    reply_text = sub(r"(R|L)", "W", reply_text)
    reply_text = sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = sub(r"\!+", " " + choice(UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + choice(UWUS)
    await owo.edit(reply_text)


@register(outgoing=True, pattern="^.react$")
async def react_meme(react):
    await react.edit(choice(FACEREACTS))


@register(outgoing=True, pattern="^.shg$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    await shg.edit(choice(SHGS))


@register(outgoing=True, pattern="^.qa[çc]$")
async def runner_lol(run):
    await run.edit(choice(RUNS_STR))


@register(outgoing=True, pattern="^oof$")
async def oof(e):
    t = "oof"
    for j in range(16):
        t = t[:-1] + "of"
        await e.edit(t)

                      
@register(outgoing=True, pattern="^Pff$")
async def Oof(e):
    t = "Pff"
    for j in range(16):
        t = t[:-1] + "ff"
        await e.edit(t)

@register(outgoing=True, pattern="^.[üu]rek (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    deq = deque(list("️❤️🧡💛💚💙💜🖤"))
    for _ in range(32):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)
    await event.edit("❤️🧡💛" + input_str + "💚💙💜🖤")    


@register(outgoing=True, pattern="^.ay$")
async def moon(event):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.clock$")
async def clock(event):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
async def claptext(memereview):
    textx = await memereview.get_reply_message()
    message = memereview.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await memereview.edit("`Mənasız bir şəkildə alqışlayıram...`")
        return
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@register(outgoing=True, pattern=r"^.f (.*)")
async def payf(event):
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2)
    await event.edit(pay)

@register(outgoing=True, pattern=r"^.bo[sş]luq")
async def bosluk(event):
    await event.delete()
    await event.reply('ㅤ')

@register(outgoing=True, pattern="^.lfy (.*)")
async def let_me_google_that_for_you(lmgtfy_q):
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {'format': 'json', 'url': lfy_url}
    r = requests.get('http://is.gd/create.php', params=payload)
    await lmgtfy_q.edit(f"Al, kefinə bax.\
    \n[{query}]({r.json()['shorturl']})")


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
async def scam(event):
    options = [
        'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
        'photo', 'document', 'cancel'
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(30, 60)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(30, 60)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await event.edit("`Invalid Syntax !!`")
        return
    try:
        if (scam_time > 0):
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("`Mənə bir mətn ver!!`")
        return
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)

CmdHelp('memes').add_command(
    'heyvan', 'pişik/it/panda/quş/qurd', 'Təsadüfi bir heyvan şəkli.'
).add_command(
    'cowsay', None, 'Bir şeylər deyən inək🐮'
).add_command(
    ':/', None, 'Yoxla gör :)'
).add_command(
    'karar', None, 'Qərar verin.'
).add_command(
    '-_-', None, 'Tamamdır.\n-Birdənəm Usta'
).add_command(
    ';_;', None, '5 dəqiqədir qaynanını görmədiyini düşün.'
).add_command(
    'cp', '<yanıt>', 'Mətnə emoji əlavə edir.'
).add_command(
    'vapor', '<mesaj/cavab>', 'Vaporlaşdırın!'
).add_command(
    'str', '<yazı>', 'Yazını uzadın.'
).add_command(
    'zal', '<cavab/mətn>', 'Çox qəribədir :/'
).add_command(
    'pff', None, 'Pff'
).add_command(
    'urek', '<ad>', 'Sevginizi göstərin.'
).add_command(
    'fp', None, 'Utanmaq'
).add_command(
    'ag', None, 'Ay animasiyası.'
).add_command(
    'clock', None, 'Saat animasiyası'
).add_command(
    'salam', None, 'Salam verin.'
).add_command(
    'owo', None, 'UwU'
).add_command(
    'react', None, 'Hər şeyə reaksiya verər.'
).add_command(
    'slap', '<cavab>', 'Təsadüfi əşyalarla vurmaq üçün mesaja cavab verin.'
).add_command(
    'cry', None, 'Ağlamaq istəyirsən ?'
).add_command(
    'shg', None, '¯\_(ツ)_/¯'
).add_command(
    'run', None, 'Qaç!'
).add_command(
    'mock', '<cavab/mesaj>', 'Et və Əyləncəni tap.'
).add_command(
    'clap', None, 'Alqış :)'
).add_command(
    'f', '<mesaj>', 'F'
).add_command(
    'type', '<yazı>', 'Daktilo kimi yazın.'
).add_command(
    'lfy', '<sorğu>', 'Bırakın Google bunu sizin için araştırsın.'
).add_command(
    'scam', '<eylem> <süre>', 'Sahte eylemler oluşturun.\nMevcut eylemler: (typing, contact, game, location, voice, round, video, photo, document, cancel)'
).add_command(
    'lfy', '<sorgu>', 'Buxarın Google bunu sizin üçün araşdırsın.'
).add_command(
    'boşluq', None, 'Boş mesaj.'
).add()
