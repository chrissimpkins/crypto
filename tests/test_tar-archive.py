#!/usr/bin/env python
# encoding: utf-8

import unittest
import os
import pexpect
from Naked.toolshed.system import file_exists, dir_exists, stderr, make_path
from crypto.library.package import generate_tar_files, remove_tar_files


class CryptoTarArchiveTest(unittest.TestCase):

    def setUp(self):
        self.pre_tardir_path = "testdir9/tar_dir"
        self.post_tardir_path = "testdir9/tar_dir.tar"
        self.pre_tardir2_path = "testdir9/tar_dir_two"
        self.post_tardir2_path = "testdir9/tar_dir_two.tar"
        self.pre_tardir_file_path = "testdir9/tar_dir/test.txt"
        self.pre_tardir2_file_path = "testdir9/tar_dir_two/test.txt"
        self.testdir_good_list = [self.pre_tardir_path]
        self.testdir_good_multidir_list = [self.pre_tardir_path, self.pre_tardir2_path]

        if not dir_exists(self.pre_tardir_path):
            stderr("missing test directory for the CryptoTarArchiveTest in test_tar-archive.py test module", exit=1)

        if not file_exists(self.pre_tardir_file_path):
            stderr("missing test file for the CryptoTarArchiveTest in the test_tar-archive.py test module", exit=1)
        
        if not dir_exists(self.pre_tardir2_path):
            stderr("missing test directory for the CryptoTarArchiveTest in test_tar-archive.py test module", exit=1)

        if not file_exists(self.pre_tardir2_file_path):
            stderr("missing test file for the CryptoTarArchiveTest in the test_tar-archive.py test module", exit=1)        
            
        # cleanup files from old tests if still around
        if file_exists(self.post_tardir_path):
            os.remove(self.post_tardir_path)

        if file_exists(self.post_tardir2_path):
            os.remove(self.post_tardir2_path)

        if file_exists(self.post_tardir_path) or file_exists(self.post_tardir2_path):
            stderr("unable to delete testfile in setup for CryptoTarArchiveTest in the test_tar-archive.py test module", exit=1)

    # Tar archive file creation unit tests
    
    def test_crypto_tar_creation(self):
        # execute generate_tar_file function with directory that contains a file
        tar_list = generate_tar_files(self.testdir_good_list)
        self.assertTrue(file_exists(self.post_tardir_path))      # generates tar from existing directory
        self.assertEqual([self.post_tardir_path], tar_list)      # confirm the list returned by function
        
        # cleanup
        os.remove(self.post_tardir_path)
        
    def test_crypto_tar_remove(self):
        # execute generate_tar_file function with directory that contains a file
        generate_tar_files(self.testdir_good_list)
        self.assertTrue(file_exists(self.post_tardir_path))      # generates tar from existing directory
        
        remove_tar_files([self.post_tardir_path])                # use the module function to remove the tar file
        self.assertFalse(file_exists(self.post_tardir_path))

    def test_crypto_tar_multidirectory(self):
        tar_list = generate_tar_files(self.testdir_good_multidir_list)
        self.assertTrue(file_exists(self.post_tardir_path))
        self.assertTrue(file_exists(self.post_tardir2_path))
        self.assertEqual([self.post_tardir_path, self.post_tardir2_path], tar_list)   # confirm list returned by the function
        
        # cleanup
        os.remove(self.post_tardir_path)
        os.remove(self.post_tardir2_path)
        
    def test_crypto_tar_multidirectory_remove(self):
        generate_tar_files(self.testdir_good_multidir_list)
        self.assertTrue(file_exists(self.post_tardir_path))
        self.assertTrue(file_exists(self.post_tardir2_path))
        
        remove_tar_files([self.post_tardir_path, self.post_tardir2_path])
        self.assertFalse(file_exists(self.post_tardir_path))
        self.assertFalse(file_exists(self.post_tardir2_path))
        
    # Command line tests with the tar archive flag

    def test_crypto_tar_commandline_tararchive(self):
        command = "crypto --tar testdir9/tar_dir"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("\r\ntestdir9/tar_dir.tar.crypt was generated from testdir9/tar_dir.tar\r\n")
        self.assertTrue(file_exists(make_path('testdir9', 'tar_dir.tar.crypt')))   # confirm that the encrypted tar file is there
        self.assertFalse(file_exists(make_path('testdir9', 'tar_dir.tar')))        # confirm that the tar file is removed
        self.assertTrue(dir_exists(make_path('testdir9', 'tar_dir')))              # confirm that the test directory is not removed
        child.close()

        os.remove('testdir9/tar_dir.tar.crypt')

    def test_crypto_tar_commandline_multidir_tararchive(self):
        command = "crypto --tar testdir9/tar_dir testdir9/tar_dir_two"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("\r\ntestdir9/tar_dir.tar.crypt was generated from testdir9/tar_dir.tar\r\n")
        child.expect("testdir9/tar_dir_two.tar.crypt was generated from testdir9/tar_dir_two.tar\r\n")

        self.assertTrue(file_exists(make_path('testdir9', 'tar_dir.tar.crypt')))   # confirm that the encrypted tar file is there
        self.assertFalse(file_exists(make_path('testdir9', 'tar_dir.tar')))        # confirm that the tar file is removed
        self.assertTrue(dir_exists(make_path('testdir9', 'tar_dir')))              # confirm that the test directory is not removed

        self.assertTrue(file_exists(make_path('testdir9', 'tar_dir_two.tar.crypt')))   # confirm that the encrypted tar file is there
        self.assertFalse(file_exists(make_path('testdir9', 'tar_dir_two.tar')))        # confirm that the tar file is removed
        self.assertTrue(dir_exists(make_path('testdir9', 'tar_dir_two')))              # confirm that the test directory is not removed

        child.close()

        os.remove('testdir9/tar_dir.tar.crypt')
        os.remove('testdir9/tar_dir_two.tar.crypt')

    def test_crypto_tar_commandline_multidir_and_file(self):
        command = "crypto --tar testdir9/tar_dir testdir9/tar_dir_two testdir9/nontar.txt"
        child = pexpect.spawn(command)
        child.expect("Please enter your passphrase: ")
        child.sendline("test")
        child.expect("Please enter your passphrase again: ")
        child.sendline("test")
        child.expect("\r\ntestdir9/nontar.txt.crypt was generated from testdir9/nontar.txt\r\n")
        child.expect("testdir9/tar_dir.tar.crypt was generated from testdir9/tar_dir.tar\r\n")
        child.expect("testdir9/tar_dir_two.tar.crypt was generated from testdir9/tar_dir_two.tar\r\n")

        self.assertTrue(
            file_exists(make_path('testdir9', 'tar_dir.tar.crypt')))  # confirm that the encrypted tar file is there
        self.assertFalse(file_exists(make_path('testdir9', 'tar_dir.tar')))  # confirm that the tar file is removed
        self.assertTrue(dir_exists(make_path('testdir9', 'tar_dir')))  # confirm that the test directory is not removed

        self.assertTrue(
            file_exists(make_path('testdir9', 'tar_dir_two.tar.crypt')))  # confirm that the encrypted tar file is there
        self.assertFalse(file_exists(make_path('testdir9', 'tar_dir_two.tar')))  # confirm that the tar file is removed
        self.assertTrue(
            dir_exists(make_path('testdir9', 'tar_dir_two')))  # confirm that the test directory is not removed

        self.assertTrue(file_exists(make_path('testdir9', 'nontar.txt.crypt')))
        self.assertTrue(file_exists(make_path('testdir9', 'nontar.txt')))  # confirm that the file was not removed

        child.close()

        os.remove('testdir9/tar_dir.tar.crypt')
        os.remove('testdir9/tar_dir_two.tar.crypt')
        os.remove('testdir9/nontar.txt.crypt')

    # Error tests
    
    def test_crypto_tar_fails_with_missingdir(self):
        bogus_dir_list = ["testdir9/bogusdir"]
        with self.assertRaises(SystemExit):
            generate_tar_files(bogus_dir_list)
            
    def test_crypto_tar_fails_with_file_instead_dir(self):
        file_list = [self.pre_tardir_file_path]
        with self.assertRaises(SystemExit):
            generate_tar_files(file_list)
            
    def test_crypto_tar_noerror_when_remove_nofile(self):
        # attempt to remove a file that does not exist
        # should not raise exception
        remove_tar_files(['testdir9/abogusfile.tar'])
        
    def test_crypto_tar_do_not_remove_nontar_file(self):
        # should not remove files without .tar file extension
        nontar_file = "testdir9/nontar.txt"
        self.assertTrue(file_exists(nontar_file))
        remove_tar_files([nontar_file])
        self.assertTrue(file_exists(nontar_file))  # should still be present after the function executed b/c not tar file
