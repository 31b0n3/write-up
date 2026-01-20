FROM ubuntu:latest

# Update and install dependencies
RUN apt-get update && apt-get install -y socat libcjson-dev

# FIX: Delete default 'ubuntu' user (UID 1000) so we can create 'ctf' with UID 1000
RUN userdel -r ubuntu && useradd --no-create-home -u 1000 ctf

# Copy challenge files
COPY flag.txt /home/ctf/flag.txt
COPY shellcode /home/ctf/shellcode

WORKDIR /home/ctf/

# Set permissions
RUN chmod 444 /home/ctf/flag.txt
RUN chmod +x /home/ctf/shellcode

USER ctf

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:\"/home/ctf/shellcode\""]