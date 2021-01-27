from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import telethon
APP_ID = int(input("APP ID yazın: "))
API_HASH = input("API HASH yazın: ")
with TelegramClient(
    StringSession(), 
    APP_ID, 
    API_HASH
) as client:
    session_str = client.session.save()
    s_m = client.send_message("me", session_str)
    print('String Session kayıtlı mesajlara qeyd edildi.')
    print('Herokuya keçerək deploya davam edin.\n\n@UserBotTG ❗')
