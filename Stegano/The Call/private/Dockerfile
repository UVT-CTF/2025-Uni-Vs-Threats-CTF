FROM python:3.11-slim

RUN apt-get update && apt-get install -y xinetd

RUN useradd -m ctf

WORKDIR /home/ctf/app

COPY app/ /home/ctf/app

RUN pip install flask

COPY xinetd /etc/xinetd.d/webchallenge
RUN chmod 755 /etc/xinetd.d/webchallenge

EXPOSE 60002

CMD ["/usr/sbin/xinetd", "-dontfork"]
