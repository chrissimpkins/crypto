#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# Application Name
#------------------------------------------------------------------------------
app_name = 'crypto'

#------------------------------------------------------------------------------
# Version Number
#------------------------------------------------------------------------------
major_version = "0"
minor_version = "2"
patch_version = "0"

#------------------------------------------------------------------------------
# Debug Flag (switch to False for production release code)
#------------------------------------------------------------------------------
debug = True

#------------------------------------------------------------------------------
# Usage String
#------------------------------------------------------------------------------
usage = """
Encrypt by explicit file path:
------------------------------
  crypto [file path] <file path...>


Encrypt all top level files in directory:
-----------------------------------------
  crypto [directory path] <directory path...>


Decrypt by explicit file path:
------------------------------
  decrypto [file path] <file path...>


Decrypt all top level encrypted files in directory:
---------------------------------------------------
  decrypto [directory path] <directory path...>

"""

#------------------------------------------------------------------------------
# Help String
#------------------------------------------------------------------------------
help = """
---------------------------------------
crypto
Simple symmetric GPG file encryption
Copyright 2014 Christopher Simpkins
MIT license
https://github.com/chrissimpkins/crypto
---------------------------------------

ABOUT
crypto provides a simple interface to Gnu Privacy Guard (gpg) encryption for one or more files.  gpg must be installed on your system in order to use crypto.

USAGE
  ENCRYPTION
    crypto [file path] <file path...>
    crypto [directory path] <directory path...>

  DECRYPTION
    decrypto [file path] <file path...>
    decrypto [directory path] <directory path...>

CRYPTO OPTIONS
   --armor | -a       Use a portable ASCII armored encryption format

DECRYPTO OPTIONS
   --overwrite | -o      Overwrite an existing file with the decrypted file
   --stdout    | -s      Print the contents of the file to the standard output stream

DESCRIPTION
Use one or more explicit file path arguments to encrypt or decrypt the file(s).  Use one or more directory arguments to encrypt all files in the top level of the directory with the same passphrase or decrypt all .crypt files in the top level of the directory.  Encrypted files are named '<filename>.crypt' and will be located in the same directory as the original file.  crypto does not remove or otherwise modify the original file.

Encryption is performed with the AES256 cipher algorithm.
"""
