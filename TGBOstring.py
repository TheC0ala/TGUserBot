MESAJ="TGUSERBOT String"
MESAJ+="\nTelegram: @UserBotTG"
pkg upgrade
clear
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
curl "https://raw.githubusercontent.com/umudmmmdov1/DTOUserBot/master/dto.py" --output "TGBOT.py"
clear
echo -e $MESAJ
echo "Qurulum Tamamlandı!, İndi String Ala Bilərsiz."
clear
python TGBOT.py
