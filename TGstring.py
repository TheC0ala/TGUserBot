MESAJ="TGUSERBOT"
MESAJ+="\nTelegram: @UserBotTG"
pkg upgrade
clear
echo -e $MESAJ
echo "Python yüklenir"
pkg install python -y
clear
echo -e $MESAJ
echo "TeleThon yüklenir"
pip install telethon
echo "Requests/BS4 yüklenir"
pip install requests
pip install bs4
clear
echo -e $MESAJ
echo "Fayl yazılır"
curl "https://raw.githubusercontent.com/TheC0ala/TGUserBot/main/TGUserBotStringAlıcı.py" --output "TGUserBotStringAlıcı.py"
clear
echo -e $MESAJ
echo "Qurulum hazırdır, Artıq String ala bilersiz"
clear
python TGUserBotStringAlıcı.py
