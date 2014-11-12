#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoSingleDirectoryDecryptTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    # decrypts .crypt, .gpg, .asc files
    # does not decrypt a file if overwrite of existing file is going to occur
    # does not implicitly decrypt a file without a .crypt, .gpg, .asc, or .pgp suffix
    def test_decrypt_singledir_multiplefiles(self):
        command = "decrypto testdir5"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("'testdir5/test1.txt.crypt' decrypted to 'testdir5/test1.txt'")
        child.expect("'testdir5/test2.txt.gpg' decrypted to 'testdir5/test2.txt'")
        child.expect("'testdir5/test3.txt.asc' decrypted to 'testdir5/test3.txt'")
        child.expect("The file path 'testdir5/test4.txt' already exists.  This file was not decrypted.")
        child.interact()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test2.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test3.txt")))
        self.assertFalse(file_exists(make_path("testdir5", "test5.decrypt"))) # should not decrypt this file
        child.close()

        #cleanup
        os.remove(make_path("testdir5", "test1.txt"))
        os.remove(make_path("testdir5", "test2.txt"))
        os.remove(make_path("testdir5", "test3.txt"))

    # empty directory test
    def test_decrypt_singledir_emptydir(self):
        command = "decrypto testdir3"
        child = pexpect.spawn(command)
        child.expect("There are no encrypted files in the directory")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # non-matched passphrases
    def test_decrypt_singledir_diff_passphrase(self):
        command = "decrypto testdir5"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match.  Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # missing directory test
    def test_decrypt_singledir_diff_passphrase(self):
        command = "decrypto fakedir"
        child = pexpect.spawn(command)
        child.expect("The path that you entered does not appear to be an existing file or directory.  Please try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)



