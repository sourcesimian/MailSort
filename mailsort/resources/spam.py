from plugin import Filter, my_email


_spam = 'spam'


class Spam(Filter):
    priority = 101

    def handle(self, msg):
        if my_email in msg.bccs:
            return

        if len(msg.all_tos) == 0:
            return msg.move(_spam)

        to_set = (
            'comms_ww@example.com',
            'example_za_grp@example.com',
            'example_za@example.com',
            'sendmail_ww@example.com',
            'sendmail.ww@example.com',
        )
        if to_set in msg.tos:
            return msg.move(_spam)

        from_set = (
            'SalesXpress@example.com',
            'sendmail_ww@example.com',
            'no-auto-replies@example.com',
        )
        if from_set in msg.froms:
            return msg.move(_spam)
