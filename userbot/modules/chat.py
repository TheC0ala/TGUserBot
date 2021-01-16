# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# TGUSERBOT - by Nurlan

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("chat")

# ████████████████████████████████ #

""" Userid, chatid ve log Əmrləri olan UserBot modulu """

from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot.main import PLUGIN_MESAJLAR

@register(outgoing=True, pattern="^.userid$")
async def useridgetter(target):
    """ .userid komanda göstərilən istifadəçinin İD nömrəsini verir"""
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**{}** {} \n**{}** `{}`".format(
            LANG['USERNAME'], name, LANG['ID'], user_id))


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def permalink(mention):
    """ .link Əmri göstərilən istifadəçinin profil bağlantısını mətn şəklində əlçatan edir  """
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = user.first_name.replace("\u2060",
                                      "") if user.first_name else user.username
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ .chatid komandası göstərilən ərupun İD-sini verir """
    await chat.edit(f"{LANG['GROUP']} `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):
    """ .log komandası seçilən mesajı günlük grupuna göndərir """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Grup ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`Bununla nə edə bilərəm  ?`")
            return
        await log_text.edit("`Günlükdə yaddaşa yazıldı`")
    else:
        await log_text.edit(LANG['NEED_LOG'])
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ .kickme komandası qrupdan çıkmağa yarayır"""
    chat = await leave.get_chat()
    await leave.edit(f"{PLUGIN_MESAJLAR['kickme']}".format(
        id=chat.id,
        title=chat.title,
        member_count="Bilinmiyor" if chat.participants_count == None else (chat.participants_count - 1)
    ))
    await leave.client.kick_participant(leave.chat_id, 'me')


@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ .unmutechat komandası susdurulmuş ərupun səsini açar """
    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        await unm_e.edit('`SQL off-mode rejimində işləyir!`')
        return
    unkread(str(unm_e.chat_id))
    await unm_e.edit(LANG['UNMUTED'])
    await sleep(2)
    await unm_e.delete()


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(mute_e):
    """ .mutechat komandası qrupu səssizləşdirir """
    try:
        from userbot.modules.sql_helper.keep_read_sql import kread
    except AttributeError:
        await mute_e.edit("`SQL off-mode rejimində işləyir!`")
        return
    await mute_e.edit(str(mute_e.chat_id))
    kread(str(mute_e.chat_id))
    await mute_e.edit(LANG['MUTED'])
    await sleep(2)
    await mute_e.delete()
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID,
            str(mute_e.chat_id) + " səssizləşdirildi.")


@register(incoming=True, disable_errors=True)
async def keep_read(message):
    """ Mute mantığı. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)


# Regex-Ninja modülü için teşekkürler @Kandnub
regexNinja = False


@register(outgoing=True, pattern="^s/")
async def sedNinja(event):
    """Regex-ninja modulu üçün, s/ ilə başlayan avtomatik silmə komandası"""
    if regexNinja:
        await sleep(.5)
        await event.delete()


@register(outgoing=True, pattern="^.regexninja (on|off)$")
async def sedNinjaToggle(event):
    """ Regex ninja modulunu həyata keçirir veyə deaktiv edir. """
    global regexNinja
    if event.pattern_match.group(1) == "on":
        regexNinja = True
        await event.edit("`Regexbot üçün ninja modulu aktivləşdirildi.`")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "off":
        regexNinja = False
        await event.edit("`Regexbot için ninja modulu deaktiv edildi.`")
        await sleep(1)
        await event.delete()


CMD_HELP.update({
    "chat":
    ".chatid\
\nKullanım: Göstərilən qrupunn ID nömrəsini verir\
\n\n.userid\
\nKullanım: Göstərilən istifadəçinin ID nömrəsini verir.\
\n\n.log\
\nKullanım: Cavablanan mesajı günlük grupuna göndərir.\
\n\n.kickme\
\nKullanım: Göstərilən qruptan çıxmağınızı həyata keçirər.\
\n\n.unmutechat\
\nKullanım: Səssizləşdirilmiş bir söhbətin səsini açar.\
\n\n.mutechat\
\nKullanım: Göstərilən grupu səssizləşdirər.\
\n\n.link <istifadəçi adı/İstifadəçi id> : <istəyə uyğun mesaj> (vəya) her hansı birinin mesajına .link ilə cavab verərək <istəyə bağlı mətin>\
\nKullanım: İstəyə bağlı şəxsi mətin ilə istifadəçinin  profilinə qalıcı bir link yaradın.\
\n\n.regexninja on/off\
\nKullanım: Dünya miqyasında olaraq regex ninja modulunu aktivləşdirir / deaktiv edər.\
\nRegex ninja modulu regex bot tərəfindən seçilən mesajları silmək üçün kömək edər."
})
