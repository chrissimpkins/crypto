#!/bin/sh

NOSE_FLAGS="--verbosity=2"
TEST_COMMAND="nosetests"

# Testing scripts
ASCII_FILE="test_ascii-armored.py"
SINGLE_FILE="test_single-file.py"
SINGLE_DIR="test_single-directory.py"

if [ "$1" = "all" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_FILE" "$SINGLE_DIR"
elif [ "$1" = "single-file" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_FILE"
elif [ "$1" = "single-dir" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_DIR"
elif [ "$1" = "ascii" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$ASCII_FILE"
else
	echo "Enter 'all' or a command suite to test."
	exit 1
fi
