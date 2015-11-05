#!/usr/bin/env python

import re
import imaplib
from email.parser import Parser
from email.utils import getaddresses
import dateutil.parser
import time


class ImapResultError(Exception):
    pass


def ImapResult(ret):
    result, data = ret
    if result != 'OK':
        raise ImapResultError(result)
    return data


class AddressField(object):
    def __init__(self, headers, fields):
        self.__names = set()
        self.__emails = set()
        self.__addresses = []

        if isinstance(fields, basestring):
            fields = (fields,)
        for field in fields:
            for i in getaddresses(headers.get_all(field, [])):
                if not i[0] and not i[1]:
                    continue
                self.__names.add(i[0].lower())
                self.__emails.add(i[1].lower())
                self.__addresses.append(i)

    def __contains__(self, items):
        if not isinstance(items, (list, tuple)):
            items = (items,)
        for item in items:
            if item.lower() in self.__emails:
                return True
            if item.lower() in self.__names:
                return True
        return False

    def __iter__(self):
        for name, email in self.__addresses:
            yield name, email

    def __len__(self):
        return len(self.__emails)

    def __str__(self):
        return ', '.join(['"%s" <%s>' % (n, e) for n, e in self.__addresses])


class Message(object):
    def __init__(self, imap, uid):
        self.__imap = imap
        self.__uid = uid
        self.__cache = {}

        data = ImapResult(self.__imap.uid('fetch', self.__uid, '(BODY.PEEK[HEADER])'))
        raw_headers = data[0][1]

        self.__header_size = len(raw_headers)
        self.__headers = Parser().parsestr(raw_headers)

    def print_headers(self):
            print '  subject:  %s' % (self.subject,)
            print '  from:     %s' % (self.froms,)
            print '  to:       %s' % (self.tos,)
            if self.ccs:
                print '  cc:       %s' % (self.ccs,)
            print '  date:     %s' % (self.date,)
#            print '  received: %s' % (repr(self.received),)
            print '  uid:      %s' % self.uid

    def raw_email(self):
        data = ImapResult(self.__imap.uid('fetch', self.__uid, '(RFC822.PEEK)'))
        raw_email = data[0][1]
        return raw_email

    def raw_body(self, part=None, skip=0, take=0):
        if part is None:
            skip = self.__header_size + skip
        if take == 0:
            span = '<%d.>' % (skip,)
        else:
            span = '<%d.%d>' % (skip, take)
        if part is None:
            part = ''
        else:
            part = '[%d]' % part
        expr = '(BODY.PEEK%s%s)' % (part, span)
        resp = ImapResult(self.__imap.uid('fetch', self.__uid, expr))
        response, data = resp[0]
        reLen = re.compile('.*<(?P<start>\d+)> \{(?P<len>\d+)\}.*')
        m = reLen.match(response)
        len = int(m.group('len'))
        return data

    #decorator
    def _cache(func):  # pylint: disable=E0213
        def _cache_(self, *args, **kwargs):
            if func.__name__ in self.__cache:
                return self.__cache[func.__name__]
            value = func(self, *args, **kwargs)  # pylint: disable=E1102
            self.__cache[func.__name__] = value
            return value
        return _cache_

    @property
    @_cache
    def subject(self):
        return self.__headers['subject'].replace('\r\n', ' ').replace('\n\r', ' ').replace('\n', ' ').replace('  ', ' ')

    @property
    @_cache
    def date(self):
        return dateutil.parser.parse(self.__headers['date'])

    @property
    def uid(self):
        return self.__uid

    @property
    @_cache
    def froms(self):
        return AddressField(self.__headers, 'from')

    @property
    @_cache
    def tos(self):
        return AddressField(self.__headers, 'to')

    @property
    @_cache
    def ccs(self):
        return AddressField(self.__headers, 'cc')

    @property
    @_cache
    def bccs(self):
        return AddressField(self.__headers, 'bcc')

    @property
    @_cache
    def all_tos(self):
        return AddressField(self.__headers, ('to', 'cc', 'bcc'))

    @property
    @_cache
    def received(self):
        t = self.__headers['received']
        if t:
            t = t.split(";", 1)[1]
            t = t.lstrip()
            d = dateutil.parser.parse(t)
            return time.mktime(d.timetuple())

        t = self.__headers['date']
        if t:
            d = dateutil.parser.parse(t)
            return time.mktime(d.timetuple())

        print self.__headers.as_string()
        raise Exception("Can't establish delivery time")

    def move(self, folder):
        try:
            print "  --> %s" % folder
            data = ImapResult(self.__imap.uid('COPY', self.__uid, folder))
            data = ImapResult(self.__imap.uid('STORE', self.__uid, '+FLAGS', '(\Deleted)'))
            self.__imap.expunge()
            return True
        except ImapResultError, e:
            import sys
            print >> sys.stderr, '! %s' % e


def iter_mailbox(hostname, username, password, mailbox, since=None):
    from datetime import datetime
    since = since or datetime.now()  # Default to today - IMAP does not do hours and minutes

    m = imaplib.IMAP4_SSL(hostname)
    m.login(username, password)
    try:

        ImapResult(m.select(mailbox))
        data = ImapResult(m.uid('search', "SENTSINCE", since.strftime('"%d-%b-%Y"')))
        #data = ImapResult(m.uid('search', None, "ALL"))

        for email_uid in data[0].split():
            try:
                yield Message(m, email_uid)
            except Exception, e:
                import traceback
                import sys
                sys.stderr.write('Exception loading message: %s\n' % email_uid)
                traceback.print_exc()
    finally:
        m.close()
        m.logout()
