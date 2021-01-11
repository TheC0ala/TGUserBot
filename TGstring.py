MESAJ="TGUSERBOT"
MESAJ+="\nTelegram: @UserBotTG"
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
curl "https://raw.githubusercontent.com/TheC0ala/TGUserBot/main/TGstring.py" --output "TGstring.py"
clear
echo -e $MESAJ
echo "Qurulum Tamamlandı!, String Ala Bilərsiz."
clear
python TGstring.py
