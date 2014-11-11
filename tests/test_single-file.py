#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoSingleFileEncryptTest(unittest.TestCase):

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

    def submit_different_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        #child.logfile = sys.stdout
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.interact()
        return child



    # TESTS FOR EXISTING FILES

    # text file
    def test_singlefile_encrypt_txt(self):
        command = "crypto testdir1/test1.txt"
        child = self.submit_same_passphrase(command)
        #stdout_string = child.logfile.getvalue()
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt"))) #test that new encrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir1","test1.txt.crypt"))


    # image file types
    def test_singlefile_encrypt_png(self):
        command = "crypto testdir1/star.png"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "star.png.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "star.png.crypt"))

    def test_singlefile_encrypt_jpg(self):
        command = "crypto testdir1/tiger.jpg"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "tiger.jpg.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "tiger.jpg.crypt"))

    def test_singlefile_encrypt_gif(self):
        command = "crypto testdir1/banana.gif"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "banana.gif.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "banana.gif.crypt"))



    # private files (should succeed on this explicit call)
    def test_singlefile_encrypt_dotfile(self):
        command = "crypto testdir1/.testfile"
        child = self.submit_same_passphrase(command)
        child.close()
        self.assertTrue(file_exists(make_path("testdir1", ".testfile.crypt")))

        # cleanup
        os.remove(make_path("testdir1", ".testfile.crypt"))


    # previously encrypted file (should fail)
    def test_singlefile_encrypt_cryptfile(self):
        command = "crypto testdir1/testcrypt.txt.crypt"

        # confirm error message and non-zero exit status code
        child = pexpect.spawn(command)
        child.expect("You are attempting to encrypt an encrypted file.  Please delete the .crypt file and repeat encryption with the original file if this is your intent.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # TESTS FOR NON-EXISTENT FILES

    def test_singlefile_encrypt_missing_file(self):
        command = "crypto testdir1/bogusfile.txt"

        # confirm error message and non-zero exit status code
        child = pexpect.spawn(command)
        child.expect("The path that you entered does not appear to be an existing file or directory.  Please try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)


    # TESTS FOR NON-MATCH ON PASSPHRASE

    def test_singlefile_encrypt_bad_passphrase(self):
        command = "crypto testdir1/test1.txt"

        # confirm non-zero exit status
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match.  Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)


