#!/usr/bin/env python
# encoding: utf-8

import sys
from Naked.toolshed.shell import muterun
from Naked.toolshed.system import dir_exists, directory, filename, file_exists, file_size, list_all_files, make_path, stdout, stderr

#------------------------------------------------------------------------------
# Cryptor class
#   performs gpg encryption of one or more files
#------------------------------------------------------------------------------
class Cryptor(object):
    def __init__(self, passphrase):
        self.command_default = "gpg -z 1 --batch --force-mdc --cipher-algo AES256 -o "
        self.command_nocompress = "gpg -z 0 --batch --force-mdc --cipher-algo AES256 -o "
        self.command_maxcompress = "gpg -z 7 --batch --force-mdc --cipher-algo AES256 -o "
        self.command_default_armored = "gpg -z 1 --armor --batch --force-mdc --cipher-algo AES256 -o "
        self.command_nocompress_armored = "gpg -z 0 --armor --batch --force-mdc --cipher-algo AES256 -o "
        self.command_maxcompress_armored = "gpg -z 7 --armor --batch --force-mdc --cipher-algo AES256 -o "
        self.passphrase = passphrase

    #------------------------------------------------------------------------------
    # PUBLIC methods
    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    # encrypt_file : file encryption method
    #------------------------------------------------------------------------------
    def encrypt_file(self, inpath, force_nocompress=False, force_compress=False, armored=False, checksum=False):
        if armored:
            if force_compress:
                command_stub = self.command_maxcompress_armored
            elif force_nocompress:
                command_stub = self.command_nocompress_armored
            else:
                if self._is_compress_filetype(inpath):
                    command_stub = self.command_default_armored
                else:
                    command_stub = self.command_nocompress_armored
        else:
            if force_compress:
                command_stub = self.command_maxcompress
            elif force_nocompress:
                command_stub = self.command_nocompress
            else:
                if self._is_compress_filetype(inpath):
                    command_stub = self.command_default
                else:
                    command_stub = self.command_nocompress

        encrypted_outpath = self._create_outfilepath(inpath)
        system_command = command_stub + encrypted_outpath + " --passphrase '" + self.passphrase + "' --symmetric " + inpath

        try:
            response = muterun(system_command)
            # check returned status code
            if response.exitcode == 0:
                stdout(encrypted_outpath + " was generated from " + inpath)
                if checksum: # add a SHA256 hash digest of the encrypted file - requested by user --hash flag in command
                    from crypto.library import hash
                    encrypted_file_hash = hash.generate_hash(encrypted_outpath)
                    if len(encrypted_file_hash) == 64:
                        stdout("SHA256 hash digest for " + encrypted_outpath + " :")
                        stdout(encrypted_file_hash)
                    else:
                        stdout("Unable to generate a SHA256 hash digest for the file " + encrypted_outpath)
            else:
                stderr(response.stderr, 0)
                stderr("Encryption failed")
                sys.exit(1)
        except Exception:
            stderr("There was a problem with the execution of gpg. Encryption failed")
            sys.exit(1)

    #------------------------------------------------------------------------------
    # encrypt_files : multiple file encryption
    #------------------------------------------------------------------------------
    def encrypt_files(self, file_list, force_nocompress=False, force_compress=False, armored=False, checksum=False):
        for the_file in file_list:
            self.encrypt_file(the_file, force_nocompress, force_compress, armored, checksum)

    #------------------------------------------------------------------------------
    # cleanup : overwrite the passphrase in memory
    #------------------------------------------------------------------------------
    def cleanup(self):
        self.passphrase = ""

    #------------------------------------------------------------------------------
    # PRIVATE methods
    #------------------------------------------------------------------------------

    def _create_outfilepath(self, inpath):
        return inpath + '.crypt'

    def _is_compress_filetype(self, inpath):
        # files > 10kB get checked for compression
        if file_size(inpath) > 10240:
            try:
                response = muterun("file --mime-type -b " + inpath)
                if response.stdout[0:5] == "text/": # check for a text file mime type
                    return True  # appropriate size, appropriate file mime type
                else:
                    return False # appropriate size, inappropriate file mime type
            except Exception:
                return False
        else:
            return False # inappropriate size, skip mime type check

