#!/usr/bin/env python
# encoding: utf-8

import os
import unittest
import pexpect
from Naked.toolshed.system import file_exists, make_path

class CryptoASCIIFileEncryptTest(unittest.TestCase):

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

    # text file
    def test_asciifile_encrypt_txt(self):
        command = "crypto --armor testdir1/test1.txt"
        child = self.submit_same_passphrase(command)
        #stdout_string = child.logfile.getvalue()
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt"))) #test that new encrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir1","test1.txt.crypt"))


    # image file types
    def test_asciifile_encrypt_png(self):
        command = "crypto -a testdir1/star.png"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "star.png.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "star.png.crypt"))

    def test_asciifile_encrypt_jpg(self):
        command = "crypto --armor testdir1/tiger.jpg"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "tiger.jpg.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "tiger.jpg.crypt"))

    def test_asciifile_encrypt_gif(self):
        command = "crypto -a testdir1/banana.gif"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "banana.gif.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "banana.gif.crypt"))


    # previously encrypted file (.crypt suffix) - should fail
    def test_asciifile_encrypt_cryptfile(self):
        command = "crypto -a testdir1/testcrypt.txt.crypt"
        child = pexpect.spawn(command)
        child.expect("There were no files identified for encryption.  crypto does not encrypt dot files or previously encrypted '.crypt' files.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # dotfile - should pass when explicit request
    def test_asciifile_encrypt_dotfile(self):
        command = "crypto --armor testdir1/.testfile"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", ".testfile.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", ".testfile.crypt"))

    # multiple files explicitly passed on CL
    def test_asciifile_encrypt_multiple_files(self):
        command = "crypto --armor testdir1/.testfile testdir1/test1.txt"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", ".testfile.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt")))
        child.close()

        # cleanup
        os.remove(make_path("testdir1", ".testfile.crypt"))
        os.remove(make_path("testdir1", "test1.txt.crypt"))

    # single directory test
    def test_asciifile_single_directory(self):
        command = "crypto --armor testdir2"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir2", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir2", "test2.txt.crypt")))
        self.assertFalse(file_exists(make_path("testdir2", "testcrypt.txt.crypt.crypt"))) # test that did not encrypt previously encrypted file
        child.close()

        # cleanup
        os.remove(make_path("testdir2", "test1.txt.crypt"))
        os.remove(make_path("testdir2", "test2.txt.crypt"))

    # multiple directories test
    def test_asciifile_multiple_directory(self):
        command = "crypto --armor testdir1 testdir2"
        child = self.submit_same_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir1", "banana.gif.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "star.png.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir1", "tiger.jpg.crypt")))
        self.assertTrue(file_exists(make_path("testdir2", "test1.txt.crypt")))
        self.assertTrue(file_exists(make_path("testdir2", "test2.txt.crypt")))
        self.assertFalse(file_exists(make_path("testdir1", "testcrypt.txt.crypt.crypt")))
        self.assertFalse(file_exists(make_path("testdir2", ".testfile.crypt")))
        self.assertFalse(file_exists(make_path("testdir2", "testcrypt.txt.crypt.crypt"))) # test that did not encrypt previously encrypted file
        child.close()

        # cleanup
        os.remove(make_path("testdir1", "banana.gif.crypt"))
        os.remove(make_path("testdir1", "star.png.crypt"))
        os.remove(make_path("testdir1", "test1.txt.crypt"))
        os.remove(make_path("testdir1", "tiger.jpg.crypt"))
        os.remove(make_path("testdir2", "test1.txt.crypt"))
        os.remove(make_path("testdir2", "test2.txt.crypt"))

    # empty directory test
    def test_asciifile_empty_directory(self):
        command = "crypto -a testdir3"
        child = pexpect.spawn(command)
        child.expect("Unable to identify files for encryption")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # single directory with only dotfiles and already encrypted files
    def test_asciifile_dotcrypt_directory(self):
        command = "crypto --armor testdir4"
        child = pexpect.spawn(command)
        child.expect("There were no files identified for encryption.  crypto does not encrypt dot files or previously encrypted '.crypt' files.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # fail on non-matched passphrase
    def test_asciifile_diff_passphrase(self):
        command = "crypto --armor testdir1"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("bogus")
        child.expect("The passphrases did not match. Please enter your command again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)

    # fail on blank passphrase (i.e. hit enter without typing a passphrase)
    def test_asciifile_blank_passphrase(self):
        command = "crypto --armor testdir1"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("")
        child.expect("You did not enter a passphrase. Please repeat your command and try again.")
        child.close()
        self.assertEqual(child.exitstatus, 1)





