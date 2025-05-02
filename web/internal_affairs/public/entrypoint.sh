#!/bin/bash

# Create random folder
RAND_DIR=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)
mkdir -p /tmp/$RAND_DIR

# Move server and public inside the random folder
# So nobody can guess the path
mv /server /tmp/$RAND_DIR/
mv /public /tmp/$RAND_DIR/
mv /flag.txt /tmp/$RAND_DIR/flag_$RAND_DIR.txt

# Move into that random directory
cd /tmp/$RAND_DIR

# Print where server is running
echo "[+] Server running inside /tmp/$RAND_DIR"

# Start the server
./server
