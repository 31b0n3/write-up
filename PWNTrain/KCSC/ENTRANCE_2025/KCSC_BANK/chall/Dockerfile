FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

WORKDIR /home/ctf

COPY bank.c .

RUN gcc bank.c -o bank

COPY flag.txt /flag.txt

RUN chmod 444 /flag.txt && \
    chmod 555 ./bank

USER ctf

EXPOSE 1402

CMD ["socat", "-T60", "TCP-LISTEN:1402,reuseaddr,fork", "EXEC:./bank,stderr"]
