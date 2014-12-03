#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# Cryptor class
#   performs gpg encryption of one or more files
#------------------------------------------------------------------------------
class Cryptor(object):
    def __init__(self, passphrase):
        self.command-default = "gpg --batch --force-mdc --cipher-algo AES256 -o "
        self.command-nocompress = "gpg -z 0 --batch --force-mdc --cipher-algo AES256 -o "
        self.command-maxcompress = "gpg -z 9 --batch --force-mdc --cipher-algo AES256 -o "

    def encrypt_file(self, file_path):
        pass

    def encrypt_files(self, file_list):
        pass

    def encrypt_directory(self, dir_path):
        pass

    def encrypt_directories(self, dir_list):
        pass



#------------------------------------------------------------------------------
# Decryptor class
#   performs gpg decryption of one or more files
#------------------------------------------------------------------------------
class Decryptor(object):
    def __init__(self):
        pass

    def decrypt_file(self, file_path):
        pass

    def decrypt_files(self, file_list):
        pass

    def decrypt_directory(self, dir_path):
        pass

    def decrypt_directories(self, dir_list):
        pass
