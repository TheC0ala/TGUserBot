MESAJ="TGUSERBOT String"
MESAJ+="\nTelegram: @UserBotTG"
echo -e $MESAJ
echo "Python yüklənir"
pkg install python -y
clear
echo -e $MESAJ
echo "TeleThon yüklənir"
pip install telethon
echo "Requests/BS4 yüklənir"
pip install requests
pip install bs4
clear
echo -e $MESAJ
echo "Fayl yazılır..."
curl "https://raw.githubusercontent.com/TheC0ala/TGUserBot/main/tgb.py" --output "tgb.py"
clear
echo -e $MESAJ
echo "Qurulum Tamamlandı!, İndi String Ala Bilərsiz."
clear
python -m tgb.py
