gtime --verbose gpg -z 9 --batch --force-mdc --cipher-algo AES256 -o test.txt.crypt --passphrase test --symmetric large-pdf.pdf

gtime --verbose gpg --batch --force-mdc --cipher-algo AES256 -o test.txt.crypt --passphrase test --symmetric pdfcomp.pdf
