

FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/ThrC0ala/TGUserBot /root/TGUserBot
WORKDIR /root/TGUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
