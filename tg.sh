MESAJ="TGUSERBOT Avto Deployuna Xoş Gəldiniz!"
MESAJ+="\nTelegram: @UserBotTG"
pkg update -y
clear
echo -e $MESAJ
echo "Python yüklənir"
pkg install python -y
clear
echo -e $MESAJ
echo "Git yüklenir"
pkg install git -y
clear
echo -e $MESAJ
echo "Telethon yüklənir"
pip install telethon
echo "Repo klonlanır..."
git clone https://github.com/thec0ala/tguserbotdeploy
clear
echo -e $MESAJ
cd TGUserBotDeploy
clear
echo "Kitabxana yüklənir"
echo -e $MESAJ
pip install wheel
pip install -r requirements.txt
python -m tg_installer
