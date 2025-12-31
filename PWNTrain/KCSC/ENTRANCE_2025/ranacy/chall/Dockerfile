FROM ubuntu:22.04

RUN apt update && apt install -y socat

RUN useradd -m user

COPY ./deploy/flag /home/user/flag
COPY ./deploy/ranacy /home/user/ranacy

RUN chown user:user /home/user/flag /home/user/ranacy && \
    chmod 755 /home/user/ranacy && \
    chmod 444 /home/user/flag

WORKDIR /home/user
USER user

EXPOSE 8386
CMD socat TCP-LISTEN:8386,reuseaddr,fork EXEC:/home/user/ranacy
