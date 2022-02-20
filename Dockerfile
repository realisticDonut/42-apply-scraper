FROM debian:buster

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install apt-utils -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y --upgrade

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install webdriver-manager

#Install prerequisites for Selenium and Chrome Headless
RUN apt-get -y install openssl
RUN apt-get -y install libffi-dev
RUN apt-get -y install ca-certificates
RUN apt-get install -y wget
RUN apt-get install -y libasound2 libnspr4 libnss3 libxss1 xdg-utils unzip
RUN apt-get install -y libappindicator1 fonts-liberation
RUN apt-get install -y libappindicator3-1 libatk-bridge2.0-0 libatspi2.0-0 libgbm1 libgtk-3-0
RUN apt-get install libcurl3-nss -y
RUN apt-get install libcurl4 -y
RUN apt-get install libcurl3-gnutls -y
RUN apt-get install -f
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome*.deb

ADD /Scraper/. .

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "getdata.py"]
