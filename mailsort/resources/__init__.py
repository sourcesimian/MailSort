
def write_resource(resource, filename):
    from pkg_resources import Requirement, resource_stream

    with open(filename, 'wt') as fh:
        file = resource_stream(Requirement.parse("mailsort"), resource)
        fh.write(file.read())


def setup_user():
    import os

    did_setup = False

    config_root = os.path.expanduser('~/.config/mailsort/filters')
    if not os.path.exists(config_root):
        os.makedirs(config_root)
        did_setup = True
        print "* Config dir created: ~/.config/mailsort"

    creds_file = os.path.expanduser('~/.config/mailsort/creds.py')
    if not os.path.exists(creds_file):
        write_resource("mailsort/resources/creds.py", creds_file)
        did_setup = True
        print "* Default credentials script: ~/.config/mailsort/creds.py"
        print "   - You need to edit this to supply the required credentials"

    filters_file = os.path.expanduser('~/.config/mailsort/filters/spam.py')
    if not os.path.exists(filters_file):
        write_resource("mailsort/resources/spam.py", filters_file)
        did_setup = True
        print "* Example filter script: ~/.config/mailsort/filters/spam.py.example"
        print "   - This is where and what your filters should look like"

    if did_setup:
        exit(1)
