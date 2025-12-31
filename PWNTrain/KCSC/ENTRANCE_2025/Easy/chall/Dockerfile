FROM ubuntu:22.04
RUN apt-get update && apt-get install -y socat

RUN useradd -m ctf

WORKDIR /home/ctf

COPY ./vuln /home/ctf/vuln
RUN echo "KCSC{test_flag_bro}" > /home/ctf/flag.txt


RUN chown -R root:ctf /home/ctf && \
    chmod 750 /home/ctf/vuln && \
    chmod 440 /home/ctf/flag.txt

USER ctf

EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./vuln,stderr"]