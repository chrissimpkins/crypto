gtime --verbose gpg -z 7 --batch --force-mdc --cipher-algo AES256 -o test.txt.crypt --passphrase test --symmetric lorem.docx

gtime --verbose gpg --batch --force-mdc --cipher-algo AES256 -o test.txt.crypt --passphrase test --symmetric pdfcomp.pdf
