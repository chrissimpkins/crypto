# crypto

## Simple symmetric GPG file encryption

### About
crypto provides a simple interface to symmetric Gnu Privacy Guard (gpg) encryption and decryption for one or more files on Unix and Linux platforms.  It runs on top of gpg and requires a gpg install on your system.  Encryption is performed with the AES256 cipher algorithm by default.

### Quickstart

#### Encrypt a File
```
crypto sometext.txt
```

#### Encrypt with ASCII Armored Output
```
crypto --armor sometext.txt
```

#### Encrypt Multiple Files with Same Passphrase
```
crypto sometext.txt anotherimage.jpg
```

#### Encrypt All Top Level Files in Multiple Directories with Same Passphrase
```
crypto imagedir privatedir
```

#### Decrypt a File
```
decrypto sometext.txt.crypt
```

#### Decrypt All Encrypted Files in Top Level of Directory
```
decrypto privatedir
```

#### Decrypt Text to Standard Output Stream
```
decrypto --stdout sometext.txt.crypt
```

### Install
#### Install GPG

##### Mac OSX Users
Mac OSX users can install GPG from [source](https://www.gnupg.org/download/index.html), with Homebrew, or by installing the [Mac GPG Tools Suite](https://gpgtools.org/gpgsuite.html).

The Homebrew install command is:

```
brew install gpg
```

Please refer to the detailed documentation on the Gnu Privacy Guard and Mac GPG Tools suite sites for more information if you choose the source or GPG Tools approaches.

##### Linux Users
If GPG is not installed on your Linux distro, you can use your package manager to install it or compile and install it from the [source code](https://www.gnupg.org/download/index.html).
