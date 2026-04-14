FROM ubuntu:24.04

RUN apt update && apt install socat -y && apt clean
RUN useradd ctf && mkdir -p /app/data && chown ctf /app/data

ADD share/ /app/
RUN chmod +x /app/* && chmod 444 /app/flag.txt

WORKDIR /app
USER ctf

CMD ["socat", "tcp-listen:10001,fork,reuseaddr", "exec:/app/kmamail 2>/dev/null"]