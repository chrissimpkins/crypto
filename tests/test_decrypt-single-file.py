#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoSingleFileDecryptTest(unittest.TestCase):

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



    # .crypt file decryption test
    def test_decrypt_singlefile_cryptfile(self):
        command = "decrypto testdir5/test1.txt.crypt"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir5", "test1.txt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir5", "test1.txt"))

    # .gpg file decryption test
    def test_decrypt_singlefile_gpgfile(self):
        command = "decrypto testdir5/test2.txt.gpg"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir5", "test2.txt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir5", "test2.txt"))

    # .asc file decryption test
    def test_decrypt_singlefile_ascfile(self):
        command = "decrypto testdir5/test3.txt.asc"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir5", "test3.txt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir5", "test3.txt"))

    # encrypted file without a file suffix test
    def test_decrypt_singlefile_nosuffix(self):
        command = "decrypto testdir5/test5"
        child = pexpect.spawn(command)
        child.expect("Could not confirm that the requested file is encrypted based upon the file type.  Attempting decryption.  Keep your fingers crossed...")
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.interact()
        self.assertTrue(file_exists(make_path("testdir5", "test5.decrypt")))
        child.close()
        # cleanup
        os.remove(make_path("testdir5", "test5.decrypt"))

    # incorrect file path (non-existent file)
    def test_decrypt_singlefile_missingfile(self):
        command = "decrypto testdir5/bogus.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("The path that you entered does not appear to be an existing file or directory.  Please try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # confirm existing file overwrite fails
    def test_decrypt_singlefile_overwrite(self):
        command = "decrypto testdir5/test4.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("Your file will be decrypted to 'testdir5/test4.txt' and this file path already exists.  Please move the file or use the --overwrite option with your command if you intend to replace the current file.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # passphrases do not match
    def test_decrypt_singlefile_diff_passphrase(self):
        command = "decrypto testdir5/test1.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match.  Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)









