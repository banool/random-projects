import sys

# This allows you to use the <private> and </private> tags to prevent
# things from being generated in the html.

ignore = False
for line in sys.stdin:
    line = line.strip()
    if line == '<private>' or line == '</private>':
        ignore = not ignore
        print('**Private section.**') if ignore else id(0)
    if ignore:
        pass
    else:
        print(line)
