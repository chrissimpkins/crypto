#!/usr/bin/env python
# encoding: utf-8

import unittest
import shutil
import os
import pexpect
from Naked.toolshed.system import file_exists, dir_exists


class CryptoUntarArchiveTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.testdir = 'testdir10'
        self.sourcedir = os.path.join(self.testdir, 'sourcedir')
        self.nofile_encrypted_archive_sourcepath = os.path.join(self.sourcedir, 'nofile.tar.crypt')
        self.nofile_encrypted_archive_destpath = os.path.join(self.testdir, 'nofile.tar.crypt')
        self.singlefile_encrypted_archive_sourcepath = os.path.join(self.sourcedir, 'singlefile.tar.crypt')
        self.singlefile_encrypted_archive_destpath = os.path.join(self.testdir, 'singlefile.tar.crypt')
        self.multifile_encrypted_archive_sourcepath = os.path.join(self.sourcedir, 'multifile.tar.crypt')
        self.multifile_encrypted_archive_destpath = os.path.join(self.testdir, 'multifile.tar.crypt')

        # cleanup old test files if they are present
        if file_exists(self.nofile_encrypted_archive_destpath):
            os.remove(self.nofile_encrypted_archive_destpath)

        if file_exists(self.singlefile_encrypted_archive_destpath):
            os.remove(self.singlefile_encrypted_archive_destpath)

        if file_exists(self.multifile_encrypted_archive_destpath):
            os.remove(self.multifile_encrypted_archive_destpath)

        if file_exists(os.path.join(self.testdir, 'nofile.tar')):
            os.remove(os.path.join(self.testdir, 'nofile.tar'))

        if file_exists(os.path.join(self.testdir, 'nofile.tar.crypt')):
            os.remove(os.path.join(self.testdir, 'nofile.tar.crypt'))

        if dir_exists(os.path.join(self.testdir, 'nofile')):
            shutil.rmtree(os.path.join(self.testdir, 'nofile'))

    def submit_same_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        return child

    def test_crypto_untar_no_file_archive_cwd(self):
        shutil.copyfile(self.nofile_encrypted_archive_sourcepath, self.nofile_encrypted_archive_destpath)
        # execute with testdir as the working directory
        try:
            os.chdir(self.testdir)
            command = "decrypto nofile.tar.crypt"
            child = self.submit_same_passphrase(command)
            # directory write occurs in the proper spot
            self.assertTrue(dir_exists('nofile'))
            # the tar archive is deleted, encrypted file is not
            self.assertFalse(file_exists('nofile.tar'))
            self.assertTrue(file_exists('nofile.tar.crypt'))
            child.close()

            # cleanup
            shutil.rmtree('nofile')
            os.remove('nofile.tar.crypt')
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e

    def test_crypto_untar_nofile_archive_notcwd(self):
        shutil.copyfile(self.nofile_encrypted_archive_sourcepath, self.nofile_encrypted_archive_destpath)
        # execute with testdir not working directory
        command = "decrypto testdir10/nofile.tar.crypt"
        child = self.submit_same_passphrase(command)
        # directory write occurs in the proper spot
        self.assertTrue(dir_exists('testdir10/nofile'))
        # the tar archive is deleted, encrypted file is not
        self.assertFalse(file_exists('testdir10/nofile.tar'))
        self.assertTrue(file_exists('testdir10/nofile.tar.crypt'))
        # there is no directory written to the current working directory
        self.assertFalse(dir_exists('nofile'))
        child.close()

        # cleanup
        shutil.rmtree('testdir10/nofile')
        os.remove(os.path.join('testdir10', 'nofile.tar.crypt'))





