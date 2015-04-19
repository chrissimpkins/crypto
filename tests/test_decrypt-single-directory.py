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


# SINGLE ARGUMENT TESTS
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

    # test that fails on blank passphrase entry
    def test_decrypt_singledir_blank_passphrase(self):
        command = "decrypto testdir5"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("")
        child.expect("You did not enter a passphrase. Please repeat your command and try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # missing directory test
    def test_decrypt_singledir_missing_dir(self):
        command = "decrypto fakedir"
        child = pexpect.spawn(command)
        child.expect("The path that you entered does not appear to be an existing file or directory.  Please try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

# MULTIPLE ARGUMENT TESTS

    # test single directory with overwrite of existing .crypt and .gpg files using long option
    def test_decrypt_singledir_overwrite_longflag(self):
        command = "decrypto --overwrite testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("'testdir6/test1.txt.crypt' decrypted to 'testdir6/test1.txt'")
        child.expect("'testdir6/test2.txt.gpg' decrypted to 'testdir6/test2.txt'")
        child.close()
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt"))) # confirm decrypted file present
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm tmp file erased
        self.assertTrue(file_exists(make_path("testdir6", "test2.txt"))) # confirm decrypted file present
        self.assertFalse(file_exists(make_path("testdir6", "test2.txt.tmp"))) # confirm tmp file erased

    # test single directory with overwrite of existing .crypt and .gpg files using short option
    def test_decrypt_singledir_overwrite_shortflag(self):
        command = "decrypto -o testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("'testdir6/test1.txt.crypt' decrypted to 'testdir6/test1.txt'")
        child.expect("'testdir6/test2.txt.gpg' decrypted to 'testdir6/test2.txt'")
        child.close()
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt"))) # confirm decrypted file present
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm tmp file erased
        self.assertTrue(file_exists(make_path("testdir6", "test2.txt"))) # confirm decrypted file present
        self.assertFalse(file_exists(make_path("testdir6", "test2.txt.tmp"))) # confirm tmp file erased

    # test print to stdout from multiple encrypted files contained in a single directory using long option
    def test_decrypt_singledir_stdout_longflag(self):
        command = "decrypto --stdout testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("single line of text from test1.txt")
        child.expect("single line of text from test2.txt")
        child.close()
        self.assertEqual(child.exitstatus, 0)

    # test print to stdout from multiple encrypted files contained in a single directory using short option
    def test_decrypt_singledir_stdout_shortflag(self):
        command = "decrypto -s testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("single line of text from test1.txt")
        child.expect("single line of text from test2.txt")
        child.close()
        self.assertEqual(child.exitstatus, 0)

    # mismatched passphrase test
    def test_decrypt_singledir_stdout_badpassphrase(self):
        command = "decrypto -s testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match.  Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # test that fails on blank passphrase entry
    def test_decrypt_singledir_stdout_blank_passphrase(self):
        command = "decrypto -s testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("")
        child.expect("You did not enter a passphrase. Please repeat your command and try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # test missing requested directory
    def test_decrypt_singledir_stdout_missingdir(self):
        command = "decrypto -s bogusdir"
        child = pexpect.spawn(command)
        child.expect("'bogusdir' does not appear to be an existing file or directory.  Aborting decryption attempt for this request.")
        child.expect("Could not identify files for decryption")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # test empty directory
    def test_decrypt_singledir_stdout_emptydir(self):
        command = "decrypto -s testdir3"
        child = pexpect.spawn(command)
        child.expect("Could not identify files for decryption")
        child.close()
        self.assertEqual(child.exitstatus, 1)

