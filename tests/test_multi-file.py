#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoMultiFileEncryptTest(unittest.TestCase):

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


    # text files
    def test_multifile_encrypt_txt(self):
        command = "crypto testdir1/test1.txt testdir2/test1.txt"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt"))) #test that new encrypted file exists
        self.assertTrue(file_exists(make_path("testdir2", "test1.txt.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1","test1.txt.crypt"))
        os.remove(make_path("testdir2","test1.txt.crypt"))

    # image files
    def test_multifile_encrypt_image(self):
        command = "crypto testdir1/star.png testdir1/tiger.jpg"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "star.png.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "tiger.jpg.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "star.png.crypt"))
        os.remove(make_path("testdir1", "tiger.jpg.crypt"))

    # multiple files with included encrypted file
    def test_multifile_encrypt_withencryptedfile(self):
        command = "crypto testdir2/test1.txt testdir2/test2.txt testdir2/testcrypt.txt.crypt"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir2", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir2", "test2.txt.crypt")))
        self.assertFalse(file_exists(make_path("testdir2", "testcrypt.txt.crypt.crypt"))) # assert that did not encrypt previously encrypted file
        child.close()

        # cleanup
        os.remove(make_path("testdir2", "test1.txt.crypt"))
        os.remove(make_path("testdir2", "test2.txt.crypt"))

    # multiple files with included dotfile
    def test_multifile_encrypt_withdotfile(self):
        command = "crypto testdir1/test1.txt testdir1/.testfile"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", ".testfile.crypt"))) #should encrypt an explicitly included dotfile
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "test1.txt.crypt"))
        os.remove(make_path("testdir1", ".testfile.crypt"))

    # multiple files with combination of good and bad filepaths
    def test_multifile_goodbad_filepath(self):
        command = "crypto testdir1/test1.txt testdir1/bogusfile.txt"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt")))
        self.assertFalse(file_exists(make_path("testdir1", "bogusfile.txt.crypt"))) #should not be present when original does not exist
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "test1.txt.crypt"))

    # multiple files with all bad filepaths
    def test_multifile_bad_filepaths(self):
        command = "crypto testdir1/bogus.txt testdir1/anotherbogus.txt"
        child = pexpect.spawn(command)
        child.expect("Unable to identify files for encryption")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # fail on non-matched passphrase
    def test_multifile_diff_passphrase(self):
        command = "crypto testdir1/test1.txt testdir1/test2.txt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match. Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)
