FROM ubuntu:22.04

# setup
ENV user user
ENV prob_port 1337

# install
RUN apt-get update && apt-get install -y socat

RUN chmod 1733 /tmp /var/tmp /dev/shm 

RUN adduser --disabled-password --gecos "" $user
ADD ./001 /home/$user/chall
ADD ./flag.txt /home/$user/flag.txt

RUN chown -R root:$user /home/$user/
RUN chown root:$user /home/$user/chall
RUN chown root:$user /home/$user/flag.txt

RUN chmod g+w /home/$user
RUN chmod 1755 /home/$user/chall
RUN chmod 440 /home/$user/flag.txt

WORKDIR /home/$user
CMD socat -T 30 TCP-LISTEN:$prob_port,reuseaddr,fork EXEC:/home/$user/chall,su=$user
EXPOSE 1337