from setuptools import setup
import os

setup(
    name="mailsort",
    version="0.1.1",
    description="Simple IMAP mailbox sorter",
    author="Source Simian",
    url='https://github.com/sourcesimian/MailSort',
    license='MIT',
    packages=['mailsort', 'mailsort.resources'],
    install_requires=['python-dateutil', 'pyplugin==0.1'],
    dependency_links=['https://github.com/sourcesimian/pyPlugin/tarball/v0.1#egg=pyplugin-0.1',],
    entry_points={
        "console_scripts": [
            "mailsort=mailsort.cli:mailsort",
        ]
    },
    download_url="https://github.com/sourcesimian/MailSort/tarball/master",
)
