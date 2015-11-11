# MailSort
IMAP mailbox sorting framework written in Python

## Install

    pip install https://github.com/sourcesimian/MailSort/tarball/v0.1.2#egg=mailsort-0.1.2 --process-dependency-links

## Setup

Implement `~/.config/mailsort/creds.py` to return the required values however you choose.

Using `~/.config/mailsort/filters/spam.py.example` implement as many filters as you like.
Split them up into whatever modules you like and store them in `~/.config/mailsort/filters/`


## Usage

    $ mailsort
