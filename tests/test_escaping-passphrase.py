#!/usr/bin/env python3
# encoding: utf-8

import sys
import os
import unittest
import pexpect
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path

class CryptoEscapePassphraseTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def submit_same_esc_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        #child.logfile = sys.stdout
        child.expect("Please enter your passphrase: ")
        child.sendline("$@`!\%^&*()_-+=3'A\\\'M'\W<>?,./|[]{}")
        child.expect("Please enter your passphrase again: ")
        child.sendline("$@`!\%^&*()_-+=3'A\\\'M'\W<>?,./|[]{}")
        child.interact()
        return child

    def test_escape_passphrase_single_file_encrypt(self):
        command = "crypto testdir11/esc_test.txt"
        child = self.submit_same_esc_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt"))) #test that new encrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11","esc_test.txt.crypt"))

    def test_escape_passphrase_multi_file_encrypt(self):
        command = "crypto testdir11/esc_test.txt testdir11/esc_test2.txt"
        child = self.submit_same_esc_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt"))) #test that new encrypted file exists
        self.assertTrue(file_exists(make_path("testdir11", "esc_test2.txt.crypt"))) #test that new encrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11","esc_test.txt.crypt"))
        os.remove(make_path("testdir11","esc_test2.txt.crypt"))

    def test_escape_directory_encrypt(self):
        command = "crypto testdir11"
        child = self.submit_same_esc_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt"))) #test that new encrypted file exists
        self.assertTrue(file_exists(make_path("testdir11", "esc_test2.txt.crypt"))) #test that new encrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11","esc_test.txt.crypt"))
        os.remove(make_path("testdir11","esc_test2.txt.crypt"))


