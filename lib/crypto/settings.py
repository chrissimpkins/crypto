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
By explicit file path:
----------------------
  crypto [file path] <file path>


By directory path:
------------------
  crypto [directory path]

"""

#------------------------------------------------------------------------------
# Help String
#------------------------------------------------------------------------------
help = """
-------------------------------------
crypto
Simple symmetric GPG file encryption
Copyright 2014 Christopher Simpkins
MIT license
-------------------------------------

ABOUT
  crypto provides a simple interface to the Gnu Privacy Guard (gpg) application for symmetric encryption of one or more files.  gpg is a project dependency and must be installed on your system in order to use crypto.

USAGE
  crypto [file path] <file path>
  crypto [directory path]

OPTIONS
   --twofish      Use the Twofish cipher
   --camellia     Use the CAMELLIA256 cipher
   --armor        Use a portable ASCII armored format

DESCRIPTION
  Use one or more explicit file paths to encrypt the file(s).  Use a directory argument to encrypt all files in the top level of the directory with the same passphrase.  The encrypted file is named '<filename>.crypt' and will be located in the same directory as the original file.  crypto does not remove or otherwise modify the original file.

  Encryption is performed with the AES256 cipher by default.
"""
