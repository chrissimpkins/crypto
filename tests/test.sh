#!/bin/sh

NOSE_FLAGS="--verbosity=2"
TEST_COMMAND="nosetests"

# Testing scripts
SINGLE_FILE="test_single-file.py"

if [ "$1" = "all" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_FILE"
elif [ "$1" = "single-file" ];then
	"$TEST_COMMAND" "$NOSE_FLAGS" "$SINGLE_FILE"
else
	echo "Enter 'all' or a command suite to test."
	exit 1
fi
