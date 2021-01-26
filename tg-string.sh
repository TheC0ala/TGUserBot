MESAJ="TGUSERBOT STRING"
MESAJ+="\nTelegram: @UserBotTG"
pkg upgrade
clear
echo -e $MESAJ
echo "Python yüklənir..."
pkg install python3 -y
pkg install git
clear
echo -e $MESAJ
echo "Telethon yüklənir..."
pip install telethon
echo "Requests/BS4 yüklənir..."
pip install requests
pip install bs4
clear
echo -e $MESAJ
echo "Fayl yazılır..."
curl "https://raw.githubusercontent.com/TheC0ala/TGUserBot/main/ddq.py" --output "ddq.py"
clear
echo -e $MESAJ
echo "Qurulum hazırdır! İndi String Session ala bilərsiz"
clear
python ddq.py
