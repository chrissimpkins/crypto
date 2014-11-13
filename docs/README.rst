================
 crypto
================
------------------------------------------------------
 Simple symmetric GPG file encryption and decryption
------------------------------------------------------

About
=============
`crypto <https://github.com/chrissimpkins/crypto>`_ provides a simple interface to symmetric `Gnu Privacy Guard <https://www.gnupg.org/>`_ encryption and decryption for one or more files on Unix and Linux platforms.  It runs on top of the Gnu Privacy Guard executable (gpg) and requires a gpg install on your system.  Encryption is performed with the AES256 cipher algorithm.

Tested in Python 2.7, 3.4, and pypy.

Quickstart
=============

Encrypt a File
----------------

	crypto sometext.txt


Encrypt with Portable ASCII Armored Format
---------------------------------------------

	crypto --armor sometext.txt


Encrypt Multiple Files with Same Passphrase
---------------------------------------------

	crypto sometext.txt anotherimage.jpg


Encrypt All Top Level Files in Multiple Directories with Same Passphrase
---------------------------------------------------------------------------

	crypto imagedir privatedir


Decrypt a File
----------------

	decrypto sometext.txt.crypt


Decrypt All Encrypted Files in Top Level of Directory
--------------------------------------------------------

	decrypto privatedir


Decrypt Text to Standard Output Stream
----------------------------------------

	decrypto --stdout sometext.txt.gpg


Install
==========

1) Install GPG
-------------------

Mac OSX
^^^^^^^^^
Mac OSX users can install gpg from `source <https://www.gnupg.org/download/index.html>`_, with `Homebrew <http://brew.sh/>`_, or by installing the `Mac GPG Tools Suite <https://gpgtools.org/gpgsuite.html>`_.

The Homebrew install command is:

	brew intall gpg

Please refer to the detailed documentation on the Gnu Privacy Guard and Mac GPG Tools suite sites for more information if you choose the source or GPG Tools approaches.

Linux
^^^^^^^^
If gpg is not installed on your Linux distro, you can use your package manager to install it or compile and install it from the `source <https://www.gnupg.org/download/index.html>`_.

2) Install crypto
-------------------
You can install crypto with `pip <https://pypi.python.org/pypi/pip/>`_:

	pip install crypto

or download the `crypto source <https://github.com/chrissimpkins/crypto/archive/master.zip>`_, unpack it, navigate to the top level directory, and install with the command:

	python setup.py install


Options
=========

crypto Options
-----------------

--armor | -a         Encrypt in a portable ASCII armored format


decrypto Options
------------------

--overwrite | -o     Overwrite an existing file with the decrypted file
--stdout    | -s     Push the file data to the standard output stream


Other Options
--------------

--help    | -h       View help documentation
--usage              View usage documentation
--version | -v       View crypto version


Issues
=========
Please submit a `new issue report on the GitHub repository <https://github.com/chrissimpkins/crypto/issues>`_ with a detailed overview of the problem that you are having.

------

`MIT License <https://github.com/chrissimpkins/crypto/blob/master/docs/LICENSE>`_ | Built with `Naked <http://naked-py.com>`_
