# @C0alaa #
# Burdan nəysə əkən ermənidi #

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp


@register(outgoing=True, pattern="^.ses kisi")
async def userland(event):
  reply = await event.get_reply_message()
  if not reply:
    await event.edit("Bir mesaja cavab verin.")
  else:
    chat = "@TextTSBot"
    await event.edit("Səsə çevrilir...⚡")
    async with event.client.conversation(chat) as conv:
      try:
        await conv.send_message("/start")
        await conv.get_response()
        # bota start veririk
        
        await conv.send_message("Turkish")
        await conv.get_response()
        # dil seçirik
        
        await conv.send_message("Kerem")
        await conv.get_response()
        # kişi sesi yoxsa qadın sesi olsun onu seçirik
        
        await conv.send_message(reply)
        x = await conv.get_response()
        
        await event.client.send_message(event.chat_id, x)
        await event.delete()
      except YouBlockedUserError:
        await event.edit("@TextTSBot'u blokdan çıxarıb yenidən cəhd edin.")
        
        
        
@register(outgoing=True, pattern="^.ses qadin")
async def userland(event):
  reply = await event.get_reply_message()
  if not reply:
    await event.edit("Bir mesaja cavab verin.")
  else:
    chat = "@TextTSBot"
    await event.edit("Səsə çevrilir...⚡")
    async with event.client.conversation(chat) as conv:
      try:
        await conv.send_message("/start")
        await conv.get_response()
        # bota start veririk
        
        await conv.send_message("Turkish")
        await conv.get_response()
        # dil seçirik
        
        await conv.send_message("Aylin")
        await conv.get_response()
        # kişi sesi yoxsa qadın sesi olsun onu seçirik
        
        await conv.send_message(reply)
        x = await conv.get_response()
        
        await event.client.send_message(event.chat_id, x)
        await event.delete()
      except YouBlockedUserError:
        await event.edit("@TextTSBot'u blokdan çıxarıb yenidən cəhd edin.")