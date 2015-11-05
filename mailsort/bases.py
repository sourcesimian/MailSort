class FilterBase(object):
    priority = 50

    def handle(self, msg):
        raise NotImplementedError()


class CredsBase(object):
    def hostname(self):
        raise NotImplementedError()

    def username(self):
        raise NotImplementedError()

    def password(self):
        raise NotImplementedError()

    def email(self):
        raise NotImplementedError()

    def mailbox(self):
        return 'INBOX'


