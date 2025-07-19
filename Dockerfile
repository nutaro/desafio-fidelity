FROM python:3.13.5-slim-bookworm

WORKDIR /opt/app

RUN apt update
RUN apt upgrade -y
RUN apt install bzip2 libxtst6 libgtk-3-0 libx11-xcb-dev libdbus-glib-1-2 libxt6 libpci-dev -y
RUN apt install build-essential wget libpq-dev gcc libasound2 -y

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz
RUN tar -zxvf geckodriver-v0.36.0-linux64.tar.gz -C /opt/
RUN rm geckodriver-v0.36.0-linux64.tar.gz
RUN wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/140.0.4/linux-x86_64/pt-BR/firefox-140.0.4.tar.xz
RUN tar xvf firefox-140.0.4.tar.xz -C /opt
RUN rm firefox-140.0.4.tar.xz
RUN ln -s /opt/firefox/firefox /usr/bin/firefox

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD src .

ENTRYPOINT ["python", "app.py"]
