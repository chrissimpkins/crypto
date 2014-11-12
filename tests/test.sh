#!/bin/sh

NOSE_FLAGS="--verbosity=2"
TEST_COMMAND="nosetests"

# Testing scripts
ASCII_FILE="test_ascii-armored.py"
DECRYPT_SINGLE_FILE="test_decrypt-single-file.py"
DECRYPT_SINGLE_DIR="test_decrypt-single-directory.py"
MULTI_FILE="test_multi-file.py"
MULTI_DIR="test_multi-directory.py"
SINGLE_FILE="test_single-file.py"
SINGLE_DIR="test_single-directory.py"

if [ "$1" = "all" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_FILE" "$SINGLE_DIR"
elif [ "$1" = "ascii" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$ASCII_FILE"
elif [ "$1" = "decrypt-dir" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$DECRYPT_SINGLE_DIR"
elif [ "$1" = "decrypt-file" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$DECRYPT_SINGLE_FILE"
elif [ "$1" = "multi-file" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$MULTI_FILE"
elif [ "$1" = "multi-dir" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$MULTI_DIR"
elif [ "$1" = "single-file" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_FILE"
elif [ "$1" = "single-dir" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_DIR"
else
	echo "Enter 'all' or a command suite to test."
	exit 1
fi
