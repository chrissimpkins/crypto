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
minor_version = "1"
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


Encrypt by directory path:
--------------------------
  crypto [directory path] <directory path...>

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
  crypto [file path] <file path...>
  crypto [directory path] <directory path...>

OPTIONS
   --armor | -a       Use a portable ASCII armored encryption format

DESCRIPTION
  Use one or more explicit file paths to encrypt the file(s).  Use one or more directory arguments to encrypt all files in the top level of the directory with the same passphrase.  Encrypted files are named '<filename>.crypt' and will be located in the same directory as the original file.  crypto does not remove or otherwise modify the original file.

  Encryption is performed with the AES256 cipher algorithm.
"""
