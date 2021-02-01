FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/thec0ala/userland /root/userland
WORKDIR /root/userland/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
