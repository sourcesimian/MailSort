#!/usr/bin/env python

import os
import types

from pyplugin import PluginLoader

from imap import iter_mailbox
from bases import FilterBase, CredsBase

from mailsort.resources import setup_user


def mailsort():
    setup_user()

    creds = [cls() for cls in PluginLoader(CredsBase, os.path.expanduser('~/.config/mailsort/creds.py'))][0]

    vmodule = types.ModuleType('plugin')
    vmodule.Filter = FilterBase
    vmodule.my_email = creds.email()

    loader = PluginLoader(FilterBase, os.path.expanduser('~/.config/mailsort/filters/*.py'), vmodule)
    filters = [cls() for cls in loader]

    def by_priority(a, b):
        return cmp(b.priority, a.priority)

    filters.sort(by_priority)

    from datetime import datetime, timedelta
    since = datetime.now() - timedelta(days=5)

    for msg in iter_mailbox(creds.hostname(), creds.username(), creds.password(), creds.mailbox(), since):
        msg.print_headers()
        for p in filters:
            if p.handle(msg) is not None:
                break
        print
