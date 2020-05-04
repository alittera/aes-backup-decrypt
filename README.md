# aes-backup-decrypt
##Introduction
This tool was created mainly to automatically decrypt backups created by the qnap hbs3 software. The data is originally encrypted with aes256-cbc by the nas and then uploaded to a cloud storage service from which it can be manually recovered. The files are encrypted and subsequently decrypted one by one maintaining the same folder structure, but losing information on permissions and last modification date.

## Security warning
The machine on which the decryption is carried out must be considered safe as the algorithm does not guarantee the security of the password from attacks.

## Requirements
It will be necessary to have the openssl library installed and usable from the terminal
Python packages:subprocess,getpass,progressbar, multiprocessing, argparse, datetime

## Usage
> python3 aes-backup-decrypt.py in_folder out_folder [-h] [-m] [-v]

positional arguments:
  in_folder           path with encrypted files and folders
  out_folder          path to save decrypted files and folders

optional arguments:
  -h, --help          show this help message and exit
  -m, --multiprocess  increase output verbosity
  -v, --verbose       enable multiprocess execution
