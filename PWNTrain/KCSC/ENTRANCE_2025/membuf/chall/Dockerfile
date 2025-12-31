FROM ubuntu@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6
ARG BUILD_UID=1000
ARG BUILD_GID=1000

RUN apt-get update && apt-get install -y socat patchelf

RUN groupadd -g ${BUILD_GID} user
RUN useradd -u ${BUILD_UID} -g ${BUILD_GID} -s /sbin/nologin user
WORKDIR /home/user
COPY ./chall ./chall
COPY ./flag.txt ./flag.txt
COPY ./ld-linux-x86-64.so.2 ./ld-linux-x86-64.so.2
COPY ./libc.so.6 ./libc.so.6
RUN chown -R root:user /home/user
RUN chmod 550 ./chall ./ld-linux-x86-64.so.2 ./libc.so.6
RUN chmod 440 ./flag.txt
RUN patchelf --set-rpath /home/user /home/user/chall && patchelf --set-interpreter /home/user/ld-linux-x86-64.so.2 /home/user/chall
user root
expose 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"su -s /bin/sh - user -c /home/user/chall"
