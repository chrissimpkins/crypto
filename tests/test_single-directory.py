#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoDirectoryEncryptTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def submit_same_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        #child.logfile = sys.stdout
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        return child


    # EMPTY DIRECTORY TEST
    def test_singledir_empty_directory(self):
        command = "crypto testdir3"
        child = pexpect.spawn(command)
        child.expect("There are no unencrypted files in the directory.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # ONLY DOTFILE AND CRYPT FILE TEST
    def test_singledir_dotcryptfiles_only(self):
        command = "crypto testdir4"
        child = pexpect.spawn(command)
        child.expect("There are no unencrypted files in the directory.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # MISSING DIRECTORY TEST
    def test_singledir_missing_directory(self):
        command = "crypto completelybogusdir"
        child = pexpect.spawn(command)
        child.expect("The path that you entered does not appear to be an existing file or directory.  Please try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # NON-MATCH ON PASSPHRASE
    def test_singledir_bad_passphrase(self):
        command = "crypto testdir1"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match.  Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # fail on blank passphrase entry
    def test_singledir_blank_passphrase(self):
        command = "crypto testdir1"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("")
        child.expect("You did not enter a passphrase. Please repeat your command and try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # DIRECTORY FILE ENCRYPTION TESTS
    def test_singledir_file_encrypt(self):
        command = "crypto testdir2"
        child = self.submit_same_passphrase(command)
        child.close()
        self.assertTrue(file_exists(make_path("testdir2", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir2", "test2.txt.crypt")))
        self.assertFalse(file_exists(make_path("testdir2", "testcrypt.txt.crypt.crypt")))

        os.remove(make_path("testdir2","test1.txt.crypt"))
        os.remove(make_path("testdir2","test2.txt.crypt"))
