#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoMultiDirectoryDecryptTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test multi-directory without overwrite switch
    def test_decrypt_multidir_blockoverwrite(self):
        command = "decrypto testdir5 testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("The file path 'testdir5/test4.txt' already exists.  This file was not decrypted")
        child.expect("The file path 'testdir6/test1.txt' already exists.  This file was not decrypted")
        child.expect("The file path 'testdir6/test2.txt' already exists.  This file was not decrypted")
        child.close()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test2.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test3.txt")))
        self.assertFalse(file_exists(make_path("testdir5", "test5.decrypt")))
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm that there is no .tmp file
        self.assertTrue(file_exists(make_path("testdir6", "test2.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test2.txt.tmp"))) # confirm that there is no .tmp file

        # cleanup
        os.remove(make_path("testdir5", "test1.txt"))
        os.remove(make_path("testdir5", "test2.txt"))
        os.remove(make_path("testdir5", "test3.txt"))


    # test multi-directory with long overwrite switch
    def test_decrypt_multidir_longoverwrite(self):
        command = "decrypto --overwrite testdir5 testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        child.close()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test2.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test3.txt")))
        self.assertFalse(file_exists(make_path("testdir5", "test5.decrypt")))
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm that there is no .tmp file
        self.assertTrue(file_exists(make_path("testdir6", "test2.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test2.txt.tmp"))) # confirm that there is no .tmp file

        # cleanup
        os.remove(make_path("testdir5", "test1.txt"))
        os.remove(make_path("testdir5", "test2.txt"))
        os.remove(make_path("testdir5", "test3.txt"))


    # test multi-directory with short overwrite switch
    def test_decrypt_multidir_shortoverwrite(self):
        command = "decrypto -o testdir5 testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        child.close()
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test2.txt")))
        self.assertTrue(file_exists(make_path("testdir5", "test3.txt")))
        self.assertFalse(file_exists(make_path("testdir5", "test5.decrypt")))
        self.assertTrue(file_exists(make_path("testdir6", "test1.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test1.txt.tmp"))) # confirm that there is no .tmp file
        self.assertTrue(file_exists(make_path("testdir6", "test2.txt")))
        self.assertFalse(file_exists(make_path("testdir6", "test2.txt.tmp"))) # confirm that there is no .tmp file

        # cleanup
        os.remove(make_path("testdir5", "test1.txt"))
        os.remove(make_path("testdir5", "test2.txt"))
        os.remove(make_path("testdir5", "test3.txt"))

    # test multi-directory stdout long switch
    def test_decrypt_multidir_longstdout(self):
        command = "decrypto --stdout testdir5 testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        child.close()
        self.assertEqual(child.exitstatus, 0)

    # test multi-directory stdout short switch
    def test_decrypt_multidir_shortstdout(self):
        command = "decrypto -s testdir5 testdir6"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        child.close()
        self.assertEqual(child.exitstatus, 0)

    # test multi-directory with one bad directory path
    def test_decrypt_multidir_bad_dirpath(self):
        command = "decrypto -s testdir6 bogusdir"
        child = pexpect.spawn(command)
        child.expect("'bogusdir' does not appear to be an existing file or directory.  Aborting decryption attempt for this request.")
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("single line of text from test1.txt")
        child.expect("single line of text from test2.txt")
        child.close()
        self.assertEqual(child.exitstatus, 0)

    # test multi-directory with two bad directory paths
    def test_decrypt_multidir_two_bad_dirpath(self):
        command = "decrypto -s bogusdir bogus2dir"
        child = pexpect.spawn(command)
        child.expect("'bogusdir' does not appear to be an existing file or directory.  Aborting decryption attempt for this request.")
        child.expect("'bogus2dir' does not appear to be an existing file or directory.  Aborting decryption attempt for this request.")
        child.expect("Could not identify files for decryption")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # test multi-directory with an empty directory included
    def test_decrypt_multidir_empty_directory(self):
        command = "decrypto -s testdir6 testdir3"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("single line of text from test1.txt")
        child.expect("single line of text from test2.txt")
        child.close()
        self.assertEqual(child.exitstatus, 0)

    # test non-matching passphrases on multi-directory command
    def test_decrypt_multidir_diff_passphrase(self):
        command = "decrypto -s testdir6 testdir3"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match.  Please enter your command again.")
        child.close()

    # test fails on blank passphrase (i.e. user hit enter without typing passphrase)
    def test_decrypt_multidir_blank_passphrase(self):
        command = "decrypto testdir6 testdir3"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("")
        child.expect("You did not enter a passphrase. Please repeat your command and try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)




