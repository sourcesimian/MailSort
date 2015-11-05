from mailsort.bases import CredsBase


class UserCreds(CredsBase):
    def hostname(self):
        # implement here to return your hostname
        raise NotImplementedError()

    def username(self):
        # implement here to return your username
        raise NotImplementedError()

    def password(self):
        # implement here to return your password
        raise NotImplementedError()

    def email(self):
        # implement here to return your email address
        raise NotImplementedError()
