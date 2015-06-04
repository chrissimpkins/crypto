#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import itertools
from multiprocessing import Pool, cpu_count

from crypto.library.response import EncryptionResponse
from Naked.toolshed.shell import muterun
from Naked.toolshed.system import file_size, stdout, stderr
from shellescape import quote


# TODO: add --singleprocess flag to optionally skip concurrent encryption approach

def multiprocess_encrypt(file_list, force_nocompress=False, force_compress=False, armored=False, checksum=False):
    filelist_length = len(file_list)
    if filelist_length > 1:
        try:
            number_processes = cpu_count()  # set number of spawned processes to cpu number
        except NotImplementedError:
            number_processes = 4   # default to 4 processes if cpu_count not implemented on OS

        # restrict number of spawned processes to number of requested files if < number_processes set above
        if number_processes > filelist_length:
            number_processes = filelist_length

        # determine number of file 'chunks' to send to each subprocess
        chunk_number = int(round(filelist_length / float(number_processes)))  # Note: keep number_processes a float

        # get the lots of filepaths for each process
        list_of_filelists = _get_process_filelists(file_list, chunk_number, number_processes)

        # create worker pool
        pool = Pool(number_processes)

        # start the encryption workers
        list_of_response_lists = pool.map(_singleproc_encryption_runner,
                                          itertools.izip(list_of_filelists,
                                                         itertools.repeat(force_nocompress),
                                                         itertools.repeat(force_compress),
                                                         itertools.repeat(armored),
                                                         itertools.repeat(checksum)))

        # create flattened list generator expression from list of lists
        response_list = (response for sublist in list_of_response_lists for response in sublist)

        for res in response_list:
            pass  # TODO: write out stdout and stderr messages from the responses

    # single file encryption requests
    else:
        response_list = _singleproc_encryption_runner(file_list, force_nocompress, force_compress, armored, checksum)

        for res in response_list:
            pass # TODO: write out stdout and stderr messages from the responses


def _singleproc_encryption_runner(file_list, force_nocompress, force_compress, armored, checksum):
    pass


def _get_process_filelists(file_list, chunk_number, process_number):
    list_of_filelists = []

    for x in xrange(process_number):
        process = x + 1   # starts at 0 so increment process counter for the process count
        if process == process_number:  # this is the final process that needs to be allotted files, add remaining files
            pre_offset = x * chunk_number
            temp_filelist = file_list[pre_offset:]
            list_of_filelists.append(temp_filelist)
        else:   # this is not final process, and it needs to be allotted chunk_number of files
            pre_offset = (x * chunk_number)
            post_offset = ((x + 1) * chunk_number)
            temp_filelist = file_list[pre_offset: post_offset]
            list_of_filelists.append(temp_filelist)

    return list_of_filelists


# TODO: add code for multiprocess decryption


# ------------------------------------------------------------------------------
# Cryptor class
#   performs gpg encryption of one or more files
# ------------------------------------------------------------------------------


class Cryptor(object):
    """performs gpg encryption of one or more files"""
    def __init__(self, passphrase):
        self.command_default = "gpg -z 1 --batch --force-mdc --cipher-algo AES256 -o "
        self.command_nocompress = "gpg -z 0 --batch --force-mdc --cipher-algo AES256 -o "
        self.command_maxcompress = "gpg -z 7 --batch --force-mdc --cipher-algo AES256 -o "
        self.command_default_armored = "gpg -z 1 --armor --batch --force-mdc --cipher-algo AES256 -o "
        self.command_nocompress_armored = "gpg -z 0 --armor --batch --force-mdc --cipher-algo AES256 -o "
        self.command_maxcompress_armored = "gpg -z 7 --armor --batch --force-mdc --cipher-algo AES256 -o "
        self.passphrase = passphrase
        self.common_binaries = set(['.7z', '.gz', '.aac', '.app', '.avi', '.azw', '.bz2', '.deb', '.doc', '.dmg', '.exe', '.flv', '.gif', '.jar', '.jpg', '.mov', '.mp3', '.mp4', '.odt', '.oga', '.ogg', '.ogm', '.pdf', '.pkg', '.png', '.ppt', '.pps', '.psd', '.rar', '.rpm', '.tar', '.tif', '.wav', '.wma', '.wmv', '.xls', '.zip', '.aiff', '.docx', '.epub', '.flac', '.mpeg', '.jpeg', '.pptx', '.xlsx'])
        self.common_text = set(['.c', '.h', '.m', '.cc', '.js', '.pl', '.py', '.rb', '.sh', '.cpp', '.css', '.csv', '.php', '.rss', '.txt', '.xml', '.yml', '.java', '.json', '.html', '.yaml'])

    # ------------------------------------------------------------------------------
    # PUBLIC methods
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # encrypt_file : file encryption method
    # ------------------------------------------------------------------------------
    def encrypt_file(self, inpath, force_nocompress=False, force_compress=False, armored=False, checksum=False):
        """public method for single file encryption with optional compression, ASCII armored formatting, and file hash digest generation"""

        file_response = EncryptionResponse()  # per file response object that is returned to calling code

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

        # set in and out file paths in response
        file_response.file_inpath = inpath
        file_response.file_outpath = encrypted_outpath

        system_command = command_stub + encrypted_outpath + " --passphrase " + quote(self.passphrase) + " --symmetric " + quote(inpath)

        try:
            response = muterun(system_command)
            # check returned status code
            if response.exitcode == 0:
                # set success flag in response
                file_response.encryption_success = True
                # set user response message
                file_response.encryption_message = encrypted_outpath + " was generated from " + inpath

                if checksum:  # add a SHA256 hash digest of the encrypted file - requested by --hash flag in command
                    # set hash digest request indicator on response
                    file_response.hash_request = True
                    # create hash digest
                    from crypto.library import hash
                    encrypted_file_hash = hash.generate_hash(encrypted_outpath)
                    if len(encrypted_file_hash) == 64:
                        # set hash digest success indicator on response
                        file_response.hash_success = True
                        file_response.hash_digest = encrypted_file_hash
                    else:
                        file_response.hash_success = False
            else:
                file_response.encryption_success = False
                file_response.error_occurred = True
                file_response.error_message = response.stderr
        except Exception as e:
            file_response.encryption_success = False
            file_response.error_occurred = True
            file_response.error_message = str(e)

        # return the file_response object to the calling code
        return file_response

    # ------------------------------------------------------------------------------
    # encrypt_files : multiple file encryption
    # ------------------------------------------------------------------------------
    def encrypt_files(self, file_list, force_nocompress=False, force_compress=False, armored=False, checksum=False):
        """public method for multiple file encryption with optional compression, ASCII armored formatting, and file hash digest generation"""
        for the_file in file_list:
            self.encrypt_file(the_file, force_nocompress, force_compress, armored, checksum)

    # ------------------------------------------------------------------------------
    # cleanup : overwrite the passphrase in memory
    # ------------------------------------------------------------------------------
    def cleanup(self):
        """public method that overwrites user passphrase in memory"""
        self.passphrase = ""

    # ------------------------------------------------------------------------------
    # PRIVATE methods
    # ------------------------------------------------------------------------------

    def _create_outfilepath(self, inpath):
        """private method that generates the crypto saved file path string with a .crypt file type"""
        return inpath + '.crypt'

    def _is_compress_filetype(self, inpath):
        """private method that performs magic number and size check on file to determine whether to compress the file"""
        # check for common file type suffixes in order to avoid the need for file reads to check magic number for binary vs. text file
        if self._is_common_binary(inpath):
            return False
        elif self._is_common_text(inpath):
            return True
        else:
            # files > 10kB get checked for compression (arbitrary decision to skip compression on small files)
            the_file_size = file_size(inpath)
            if the_file_size > 10240:
                if the_file_size > 512000:  # seems to be a break point at ~ 500kb where file compression offset by additional file read, so limit tests to files > 500kB
                    try:
                        system_command = "file --mime-type -b " + quote(inpath)
                        response = muterun(system_command)
                        if response.stdout[0:5] == "text/":  # check for a text file mime type
                            return True   # appropriate size, appropriate file mime type
                        else:
                            return False  # appropriate size, inappropriate file mime type
                    except Exception:
                        return False
                else:
                    return True  # if file size is < 500kB, skip the additional file read and just go with compression
            else:
                return False  # below minimum size to consider compression, do not compress

    def _is_common_binary(self, inpath):
        """private method to compare file path mime type to common binary file types"""
        # make local variables for the available char numbers in the suffix types to be tested
        two_suffix = inpath[-3:]
        three_suffix = inpath[-4:]
        four_suffix = inpath[-5:]
        
        # test for inclusion in the instance variable common_binaries (defined in __init__)
        if two_suffix in self.common_binaries:
            return True
        elif three_suffix in self.common_binaries:
            return True
        elif four_suffix in self.common_binaries:
            return True
        else:
            return False

    def _is_common_text(self, inpath):
        """private method to compare file path mime type to common text file types"""
        # make local variables for the available char numbers in the suffix types to be tested
        one_suffix = inpath[-2:]
        two_suffix = inpath[-3:]
        three_suffix = inpath[-4:]
        four_suffix = inpath[-5:]
        
        # test for inclusion in the instance variable common_text (defined in __init__)
        if one_suffix in self.common_text:
            return True
        elif two_suffix in self.common_text:
            return True
        elif three_suffix in self.common_text:
            return True
        elif four_suffix in self.common_text:
            return True
        else:
            return False
