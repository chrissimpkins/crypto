#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoMultiDirectoryEncryptTest(unittest.TestCase):

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

    # multiple directories including some previously encrypted files and dotfiles
    def test_multdir_encrypt_files(self):
        command = "crypto testdir1 testdir2"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "banana.gif.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "star.png.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "tiger.jpg.crypt")))

        self.assertFalse(file_exists(make_path("testdir1", ".testfile.crypt"))) # does not encrypt dotfiles when not explicit
        self.assertFalse(file_exists(make_path("testdir1", "testcrypt.txt.crypt.crypt"))) # does not encrypt previously encrypted files

        self.assertTrue(file_exists(make_path("testdir2", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir2", "test2.txt.crypt")))

        self.assertFalse(file_exists(make_path("testdir2", "testcrypt.txt.crypt.crypt")))

        # cleanup
        os.remove(make_path("testdir1","test1.txt.crypt"))
        os.remove(make_path("testdir1","banana.gif.crypt"))
        os.remove(make_path("testdir1","star.png.crypt"))
        os.remove(make_path("testdir1","tiger.jpg.crypt"))
        os.remove(make_path("testdir2","test1.txt.crypt"))
        os.remove(make_path("testdir2","test2.txt.crypt"))

    # ignores single bad directory
    def test_multidir_bad_single_dir_path(self):
        command = "crypto bogusdir1 testdir2"
        child = self.submit_same_passphrase(command)

        self.assertTrue(file_exists(make_path("testdir2", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir2", "test2.txt.crypt")))

        self.assertFalse(file_exists(make_path("testdir2", "testcrypt.txt.crypt.crypt")))

        # cleanup
        os.remove(make_path("testdir2","test1.txt.crypt"))
        os.remove(make_path("testdir2","test2.txt.crypt"))

    # notifies user if all bad directory paths
    def test_multidir_bad_all_dir_paths(self):
        command = "crypto bogusdir1 bogusdir2"
        child = pexpect.spawn(command)
        child.expect("Unable to identify files for encryption")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # fail on non-matched passphrases
    def test_multidir_diff_passphrases(self):
        command = "crypto testdir1 testdir2"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match. Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)
