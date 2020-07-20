From ubuntu:20.04
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
COPY localtime /etc/localtime
RUN apt-get install -y firefox
RUN pip3 install selenium
RUN cd /tmp
RUN apt-get install -y wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN sh -c 'tar -x geckodriver -zf geckodriver-v0.26.0-linux64.tar.gz -O > /usr/local/bin/geckodriver'
RUN chmod +x /usr/local/bin/geckodriver
RUN rm geckodriver-v0.26.0-linux64.tar.gz
RUN pip3 install pyexcel-ods
RUN pip3 install XlsxWriter

