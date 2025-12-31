FROM ubuntu:24.04

COPY ./pingpong ./pingpong
COPY ./flag.txt /flag.txt
RUN apt-get update
RUN yes | apt-get install socat

RUN chmod +x pingpong
RUN chmod 400 /flag.txt

CMD ["socat", "tcp-l:1339,reuseaddr,fork", "EXEC:'./pingpong'"]

