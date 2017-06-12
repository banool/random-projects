import sys

# This allows you to use the <private> and </private> tags to prevent
# things from being generated in the html.

ignore_tags = ['<private>', '</private>', '<\\private>', '<secret>', '</secret>', '<\\secret>']

ignore = False
for line in sys.stdin:
    line = line.rstrip()
    if line in ignore_tags:
        ignore = not ignore
        print('**Private section.**') if ignore else id(0)
    if ignore:
        pass
    else:
        print(line)
