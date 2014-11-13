#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoMultiFileDecryptTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def submit_same_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        return child

    # multiple files of different filetypes directory
    def test_decrypt_multifile_same_directory(self):
        command = "decrypto testdir5/test1.txt.crypt testdir5/test2.txt.gpg testdir5/test3.txt.asc"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test2.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test3.txt")))

        child.close()

        #cleanup
        os.remove(make_path("testdir5", "test1.txt"))
        os.remove(make_path("testdir5", "test2.txt"))
        os.remove(make_path("testdir5", "test3.txt"))

    # multiple files with one file that would lead to overwrite - confirm that overwrite fails
    def test_decrypt_multifile_overwrite_file(self):
        command = "decrypto testdir5/test1.txt.crypt testdir6/test1.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("The file path 'testdir6/test1.txt' already exists.  This file was not decrypted")
        child.close()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm that there is no .tmp file

        #cleanup
        os.remove(make_path("testdir5", "test1.txt"))
         ## do not remove the test1.txt in the testdir6, needed for other tests

    # confirm that overwrite succeeds when user passes the --overwrite long option
    def test_decrypt_multifile_overwrite_longflag(self):
        command = "decrypto --overwrite testdir5/test1.txt.crypt testdir6/test1.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        child.close()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm that there is no .tmp file

        #cleanup
        os.remove(make_path("testdir5", "test1.txt"))
         ## do not remove the test1.txt in the testdir6, needed for other tests

    # confirm that overwrite succeeds when user passes the -o short option
    def test_decrypt_multifile_overwrite_shortflag(self):
        command = "decrypto -o testdir5/test1.txt.crypt testdir6/test1.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        child.close()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm that there is no .tmp file

        #cleanup
        os.remove(make_path("testdir5", "test1.txt"))
         ## do not remove the test1.txt in the testdir6, needed for other tests

    # stdout long flag with multiple files
    def test_decrypt_multifile_long_stdout(self):
        command = "decrypto --stdout testdir6/test1.txt.crypt testdir6/test2.txt.gpg"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("single line of text from test1.txt")
        child.expect("single line of text from test2.txt")
        child.close()

    # stdout short flag with multiple files
    def test_decrypt_multifile_short_stdout(self):
        command = "decrypto -s testdir6/test1.txt.crypt testdir6/test2.txt.gpg"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("single line of text from test1.txt")
        child.expect("single line of text from test2.txt")
        child.close()

    # multiple files with one bad file path
    def test_decrypt_multifile_bad_filepath(self):
        command = "decrypto testdir5/bogusfile.txt.crypt testdir5/test1.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("'testdir5/bogusfile.txt.crypt' does not appear to be an existing file or directory.  Aborting decryption attempt for this request.")
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        child.close()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))

        # cleanup
        os.remove(make_path("testdir5", "test1.txt"))

    # passphrase mismatch
    def test_decrypt_multifile_diff_passphrase(self):
        command = "decrypto testdir5/test1.txt.crypt testdir5/test2.txt.gpg"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match.  Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)








