mesaj = "TGUSERBOT"
mesaj += "Telegram: @UserBotTG"
mesaj += "Çıxan hər şeyə Y enter."
clear
echo $mesaj
echo "Python yüklənir..."
apk add python3
clear
echo $mesaj
echo "TeleThon yüklənir..."
pip3 install telethon
pip3 install bs4
pip3 install requests
clear
echo $mesaj
echo "Fayl yazılır..."
curl "https://raw.githubusercontent.com/TheC0ala/TGUserBot/main/ddq.py" --output "ddq.py"
echo $mesaj
echo "Qurulum hazırdır! İndi String ala bilərsiz."
python3 ddq.py
