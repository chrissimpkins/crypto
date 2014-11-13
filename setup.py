import os
import re
from setuptools import setup, find_packages


def docs_read(fname):
    return open(os.path.join(os.path.dirname(__file__), 'docs', fname)).read()

def version_read():
    settings_file = open(os.path.join(os.path.dirname(__file__), 'lib', 'crypto', 'settings.py')).read()
    major_regex = """major_version\s*?=\s*?["']{1}(\d+)["']{1}"""
    minor_regex = """minor_version\s*?=\s*?["']{1}(\d+)["']{1}"""
    patch_regex = """patch_version\s*?=\s*?["']{1}(\d+)["']{1}"""
    major_match = re.search(major_regex, settings_file)
    minor_match = re.search(minor_regex, settings_file)
    patch_match = re.search(patch_regex, settings_file)
    major_version = major_match.group(1)
    minor_version = minor_match.group(1)
    patch_version = patch_match.group(1)
    if len(major_version) == 0:
        major_version = 0
    if len(minor_version) == 0:
        minor_version = 0
    if len(patch_version) == 0:
        patch_version = 0
    return major_version + "." + minor_version + "." + patch_version


setup(
    name='crypto',
    version=version_read(),
    description='Simple symmetric GPG file encryption and decryption',
    long_description=(docs_read('README.rst')),
    url='https://github.com/chrissimpkins/crypto',
    license='MIT license',
    author='Christopher Simpkins',
    author_email='git.simpkins@gmail.com',
    platforms=['any'],
    entry_points = {
        'console_scripts': [
            'crypto = crypto.app:main',
            'decrypto = crypto.decryptoapp:main'
        ],
    },
    packages=find_packages("lib"),
    package_dir={'': 'lib'},
    install_requires=['Naked'],
    keywords='encryption,decryption,gpg,pgp,openpgp,cipher,AES256,crypto,cryptography,security,privacy',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Topic :: Security :: Cryptography',
        'Topic :: Security',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
)
