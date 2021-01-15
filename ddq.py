MESAJ="TGUSERBOT String"
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
echo "Fayl yazılır..."
curl "https://raw.githubusercontent.com/thec0ala/tguserbot/main/tgstring.py" --output "tgstring.py"
clear
echo -e $MESAJ
echo "Qurulum hazırdır, İndi StringSessionu ala bilersiz"
clear
python tgstring.py
