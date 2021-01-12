import asyncio
import html
import os
import sys
import time
import random

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError
from telethon.network import ConnectionTcpAbridged
from telethon.utils import get_display_name
from telethon.sessions import StringSession

try:
   import requests
   import bs4
except:
   print("[!] Requests Tapıla Bilmədi. Yüklənilir...")
   print("[!] Bs4 Tapılmadı. Yüklənilir...")

   if os.name == 'nt':
      os.system("python3.8 -m pip install requests")
      os.system("python3.8 -m pip install bs4")
   else:
      os.system("pip3 install requests")
      os.system("pip3 install bs4")


# Original Source https://github.com/LonamiWebs/Telethon/master/telethon_examples/interactive_telegram_client.py #
loop = asyncio.get_event_loop()

class InteractiveTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash,
                 telefon=None, proxy=None):
        super().__init__(
            session_user_id, api_id, api_hash,
            connection=ConnectionTcpAbridged,
            proxy=proxy
        )
        self.found_media = {}
        print('@UserBotTG String Alıcı')
        print('[i] Telegramın Serverlərinə Bağlanılır...')
        try:
            loop.run_until_complete(self.connect())
        except IOError:
            print('[!] Bağlanarkən Xəta Baş Verdi. Təkrad Cəhd Edilir...')
            loop.run_until_complete(self.connect())

        if not loop.run_until_complete(self.is_user_authorized()):
            if telefon == None:
               user_phone = input('[?] Telefon Nömrəniz (Məsələn: +994xxxxxxxxx): ')
            else:
               user_phone = telefon
            try:
                loop.run_until_complete(self.sign_in(user_phone))
                self_user = None
            except PhoneNumberInvalidError:
                print("[!] Səf Nömrə Yazdınız Düzgün Yazın. Məsələn: +994xxxxxxxxx")
                exit(1)
            except ValueError:
               print("[!] Səf Nömrə Yazdınız Düzgün Yazın. Məsələn: +994xxxxxxxxx")
               exit(1)

            while self_user is None:
                code = input('[?] Telegramdan Gələn 5 Rəqəmli Kodu Yazın: ')
                try:
                    self_user =\
                        loop.run_until_complete(self.sign_in(code=code))
                except PhoneCodeInvalidError:
                    print("[!] Kod Səfdir. Kodu Düzgün Yazın")
                except SessionPasswordNeededError:
                    pw = input('[i] İki Faktorlu Doğrulama  '
                                 '[?] Şifrənizi Yazın: ')
                    try:
                        self_user =\
                            loop.run_until_complete(self.sign_in(password=pw))
                    except PasswordHashInvalidError:
                        print("[!] Parol Səfdir. Zəhmət Olmasa Bir Daha Cəhd Edin. [Həddindən artıq cəhdlər hesabınızın qadağan olunmasına səbəb ola bilər]")


if __name__ == '__main__':
   print(" TGUSERBOT String v1\n @UserBotTG\n\n")
   print("[1] Avtomatik API ID/HASH Alıcı")
   print("[2] String Alıcı\n")
   
   try:
      secim = int(input("[?] Seçim Edin: "))
   except:
      print("[!] Zəhmət olmasa sadəcə rəqəm yazın!")

   if secim == 2:
      API_ID = input('[?] API ID\'iniz [Hazır Key\'leri İşlətmək Üçün Boş Buraxı ]: ')
      if API_ID == "":
         print("[i] Hazır Keyler İşlədilir...")
         API_ID = 4
         API_HASH = "014b35b6184100b085b0d0572f9b5103"
      else:
         API_HASH = input('[?] API HASH\'ınız: ')

      client = InteractiveTelegramClient(StringSession(), API_ID, API_HASH)
      print("[i] String Keyiniz Aşağıdakıdır!\n\n\n" + client.session.save())
   elif secim == 1:
      numara = input("[?] Telefon Nömrəniz: ")
      try:
         rastgele = requests.post("https://my.telegram.org/auth/send_password", data={"phone": numara}).json()["random_hash"]
      except:
         print("[!] Kod Göndərilmədi. Telefon Nömrənizi Yoxlayın.")
         exit(1)
      
      sifre = input("[?] Telegram'dan GƏlən Kodu Yazın: ")
      try:
         cookie = requests.post("https://my.telegram.org/auth/login", data={"phone": numara, "random_hash": rastgele, "password": sifre}).cookies.get_dict()
      except:
         print("[!] Böyük Ehtimal Kodu Səf Yazdız. Zəhmət olmasa Scripti Yenidən Başladın.")
         exit(1)
      app = requests.post("https://my.telegram.org/apps", cookies=cookie).text
      soup = bs4.BeautifulSoup(app, features="html.parser")

      if soup.title.string == "Create new application":
         print("[i] Tətbiqiniz Yoxdur. Tətbiq Yaradılır...")
         hashh = soup.find("input", {"name": "hash"}).get("value")
         AppInfo = {
            "hash": hashh,
            "app_title":"TGUSERBOT",
            "app_shortname": "tguserbot" + str(random.randint(9, 99)) + str(time.time()).replace(".", ""),
            "app_url": "",
            "app_platform": "android",
            "app_desc": ""
         }
         app = requests.post("https://my.telegram.org/apps/create", data=AppInfo, cookies=cookie).text
         print(app)
         print("[i] Tətbiq Uğurla Yaradıldı!")
         print("[i] API ID/HASH alınır...")
         newapp = requests.get("https://my.telegram.org/apps", cookies=cookie).text
         newsoup = bs4.BeautifulSoup(newapp, features="html.parser")

         g_inputs = newsoup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         print("[i] Məlumatlar Gətirildi! Zəhmət Olmasa Bunladı Bir Yerə Qeyd Edin..\n\n")
         print(f"[i] API ID: {app_id}")
         print(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almaq İstəyirsiniz? [Hə üçün 1 yazın]: "))
         except:
            print("[!] Zəhmət Olmasa Sadəcə Rəqəm Yazın!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            print("[i] String Keyiniz Aşağıdakıdır!\n\n\n" + client.session.save())
         else:
            print("[i] Script Dayandırılır...")
            exit(1)
      elif  soup.title.string == "App configuration":
         print("[i] Tətbiqiniz var. API ID/HASH Çəkilir...")
         g_inputs = soup.find_all("span", {"class": "form-control input-xlarge uneditable-input"})
         app_id = g_inputs[0].string
         api_hash = g_inputs[1].string
         print("[i] Məlumatlar Gətirildi! Zəhmət Olmasa Bunları 1 Yerə Qeyd Edin.\n\n")
         print(f"[i] API ID: {app_id}")
         print(f"[i] API HASH: {api_hash}")
         try:
            stringonay = int(input("[?] String Almaq İstəyirsiniz? [Hə üçün 1 yazın]: "))
         except:
            print("[!] Zəhmət Olmasa Sadəcə Rəqəm Yazın!")

         if stringonay == 1:
            client = InteractiveTelegramClient(StringSession(), app_id, api_hash, numara)
            print("[i] String Keyiniz Aşağıdakıdır!\n\n\n" + client.session.save())
         else:
            print("[i] Script Dayandırılır...")
            exit(1)
      else:
         print("[!] Bir Xəta Baş Verdi.")
         exit(1)
   else:
      print("[!] Məlum Olmayan Seçim.")
