

FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/TheC0ala/UserLand /root/UserLand
WORKDIR /root/TGUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
