#!/bin/sh
# crypto-single.sh
# Single file encryption with gpg
# Copyright 2014 Christopher Simpkins
# MIT License

if [ $# -eq 0 ]; then
	echo "Error: The crypto-single script did not receive a file path for encryption." 1>&2
	exit 1
fi

echo "Please enter your passphrase: "
read -s passphrase

echo "Please enter your passphrase again: "
read -s passphrase_confirm

if [ "$passphrase" != "$passphrase_confirm" ]; then
	echo "The passphrases did not match.  Please re-enter your encryption command and try again."
	exit 1
fi

if [ -f "$file" ]; then
	gpg --batch --force-mdc --cipher-algo AES256 -o ${file%%.*}.crypt --passphrase "$passphrase" --symmetric $file
else
	echo "'$file' does not appear to be a file and cannot be encrypted." >&2
fi

# remove the temporary passphrase variables
unset passphrase
unset passphrase_confirm

echo "Encryption complete."
exit 0
