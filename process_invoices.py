import hashlib
import os
from time import sleep

LPT_OUTPUT_FILE = "invoice.txt"

def wait_for_change_to_file(filename):
    file_sig = file_signature(filename)
    while file_signature(filename) == file_sig:
        sleep(1)
        print "waiting for changes."
    print "found a change"
    return

def file_signature(filename):
    if not os.path.exists(filename):
        return "empty_file"
    else:
        return md5_of_file(filename)

def md5_of_file(filename):
    f = open(filename,'rb')
    m = hashlib.md5()
    while True:
        ## Don't read the entire file at once...
        data = f.read(10240)
        if len(data) == 0:
            break
        m.update(data)
    return m.hexdigest()

def dump_file(filename):
    try:
        with open(filename) as f:
            lines = []
            for line in f:
                lines.append(line)
            return lines
    except IOError as e:
        print 'An Error occured.'

def blank_file(filename):
    open(filename, 'w').close()

if __name__ == '__main__':
    blank_file(LPT_OUTPUT_FILE)
    wait_for_change_to_file(LPT_OUTPUT_FILE)
    dump_file(LPT_OUTPUT_FILE)
    blank_file(LPT_OUTPUT_FILE)

