#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import unittest
import pexpect
import shutil
from Naked.toolshed.shell import execute
from Naked.toolshed.system import file_exists, make_path, dir_exists

class CryptoEscapePassphraseTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()

    def tearDown(self):
        pass

    def submit_same_esc_passphrase(self, system_command):
        child = pexpect.spawn(system_command)
        # child.logfile = sys.stdout
        child.expect("Please enter your passphrase: ")
        child.sendline("$@`!\%^&*()_-+=3'A\\\'M'\W<>?,./|[]{}")
        child.expect("Please enter your passphrase again: ")
        child.sendline("$@`!\%^&*()_-+=3'A\\\'M'\W<>?,./|[]{}")
        child.interact()
        return child

    def test_escape_passphrase_single_file_encrypt_decrypt(self):
        command = "crypto testdir11/esc_test.txt"
        child = self.submit_same_esc_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt")))  # test new encrypted file exists
        child.close()

        os.rename("testdir11/esc_test.txt.crypt", "testdir11/SUBTEST.txt.crypt")

        decrypt_command = "decrypto testdir11/SUBTEST.txt.crypt"
        child = self.submit_same_esc_passphrase(decrypt_command)
        self.assertTrue(file_exists(make_path("testdir11", "SUBTEST.txt")))  # test decrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11", "SUBTEST.txt"))
        os.remove(make_path("testdir11", "SUBTEST.txt.crypt"))

    def test_escape_passphrase_multi_file_encrypt_decrypt(self):
        command = "crypto testdir11/esc_test.txt testdir11/esc_test2.txt"
        child = self.submit_same_esc_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt")))  # test new encrypted file exists
        self.assertTrue(file_exists(make_path("testdir11", "esc_test2.txt.crypt")))  # test new encrypted file exists
        child.close()

        os.rename("testdir11/esc_test.txt.crypt", "testdir11/SUBTEST1.txt.crypt")
        os.rename("testdir11/esc_test2.txt.crypt", "testdir11/SUBTEST2.txt.crypt")

        decrypt_command = "decrypto testdir11/SUBTEST1.txt.crypt testdir11/SUBTEST2.txt.crypt"
        child = self.submit_same_esc_passphrase(decrypt_command)
        self.assertTrue(file_exists(make_path("testdir11", "SUBTEST1.txt")))  # test decrypted file exists
        self.assertTrue(file_exists(make_path("testdir11", "SUBTEST2.txt")))  # test decrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11", "SUBTEST1.txt"))
        os.remove(make_path("testdir11", "SUBTEST1.txt.crypt"))
        os.remove(make_path("testdir11", "SUBTEST2.txt"))
        os.remove(make_path("testdir11", "SUBTEST2.txt.crypt"))

    def test_escape_directory_encrypt_decrypt(self):
        command = "crypto testdir11"
        child = self.submit_same_esc_passphrase(command)
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt")))  # test new encrypted file exists
        self.assertTrue(file_exists(make_path("testdir11", "esc_test2.txt.crypt")))  # test new encrypted file exists
        child.close()

        os.rename("testdir11/esc_test.txt.crypt", "testdir11/SUBTEST1.txt.crypt")
        os.rename("testdir11/esc_test2.txt.crypt", "testdir11/SUBTEST2.txt.crypt")

        decrypt_command = "decrypto testdir11"
        child = self.submit_same_esc_passphrase(decrypt_command)
        self.assertTrue(file_exists(make_path("testdir11", "SUBTEST1.txt")))  # test decrypted file exists
        self.assertTrue(file_exists(make_path("testdir11", "SUBTEST2.txt")))  # test decrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11", "SUBTEST1.txt"))
        os.remove(make_path("testdir11", "SUBTEST1.txt.crypt"))
        os.remove(make_path("testdir11", "SUBTEST2.txt"))
        os.remove(make_path("testdir11", "SUBTEST2.txt.crypt"))

    def test_escape_tar_encrypt(self):
        try:
            # change to the sub test directory for tar tests
            os.chdir("testdir11")
            command = "crypto --tar testtar"
            child = self.submit_same_esc_passphrase(command)
            self.assertTrue(file_exists("testtar.tar.crypt"))  # test new encrypted archive exists
            child.close()

            shutil.move('testtar', 'testtar_temp')

            decrypt_command = "decrypto testtar.tar.crypt"
            child = self.submit_same_esc_passphrase(decrypt_command)
            self.assertTrue(dir_exists(make_path("testtar")))  # test decrypted tar archive exists
            self.assertTrue(file_exists(make_path("testtar", "esc_test.txt")))
            self.assertTrue(file_exists(make_path("testtar", "esc_test2.txt")))
            child.close()

            # cleanup
            os.remove(make_path("testtar.tar.crypt"))  # remove encrypted archive
            shutil.rmtree(make_path("testtar"))        # remove the decrypted, unpacked directory
            shutil.move('testtar_temp', 'testtar')  # move the original tar testing dir back to original path
        except Exception as e:
            # return to top level testing directory
            os.chdir(self.cwd)
            raise e
        finally:
            # return to top level testing directory
            os.chdir(self.cwd)


    def test_escape_passphrase_with_spaces(self):
        command = "crypto testdir11/esc_test.txt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("$@`!\%^&*()_ -+=3'A\\\ 'M'\W<>?,./|[]{}")
        child.expect("Please enter your passphrase again: ")
        child.sendline("$@`!\%^&*()_ -+=3'A\\\ 'M'\W<>?,./|[]{}")
        child.interact()
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt")))  # test new encrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11", "esc_test.txt.crypt"))

    def test_escape_passphrase_with_unicode_chars_and_spaces(self):
        command = "crypto testdir11/esc_test.txt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("$@`!\%^&*()_ -+=3'A\\\ 'M'\W<>?,./|[]{}œœ")
        child.expect("Please enter your passphrase again: ")
        child.sendline("$@`!\%^&*()_ -+=3'A\\\ 'M'\W<>?,./|[]{}œœ")
        child.interact()
        self.assertTrue(file_exists(make_path("testdir11", "esc_test.txt.crypt")))  # test new encrypted file exists
        child.close()

        # cleanup
        os.remove(make_path("testdir11", "esc_test.txt.crypt"))





