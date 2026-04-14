while true; do 
    echo 'Hello, world!' > file
    rm file
    ln -s /flag file
    rm file
done