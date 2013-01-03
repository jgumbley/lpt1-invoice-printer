import hashlib
import os
from time import sleep
from reportlab.pdfgen import canvas
import uuid


LPT_OUTPUT_FILE = "C:\\mass-89\\invoice.txt"

def wait_for_change_to_file(filename):
    file_sig = file_signature(filename)
    while file_signature(filename) == file_sig:
        sleep(1)
        print "waiting for an invoice."
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


def make_invoice(file_content, filename):
    print "making a PDF"
    c = canvas.Canvas(filename)
    c.setFont("Courier", 11)
    x = 800
    for line in file_content:
        if "G" in line:
            c.setFont("Courier-Bold", 11)
        if "H" in line:
            c.setFont("Courier", 11)
        line = line.replace("G", "")
        line = line.replace("H", "")
        c.drawString(20,x,line[:-1])
        x = x - 12
    c.save()

def make_pdf_filename():
    return str(uuid.uuid1())[8:] + ".pdf"

def spawn_pdf_viewer(filename):
    os.system("start " + filename)

if __name__ == '__main__':
    while True:
        blank_file(LPT_OUTPUT_FILE)
        wait_for_change_to_file(LPT_OUTPUT_FILE)
        sleep(2) # make sure MASS89 has finished writing it
        file_content = dump_file(LPT_OUTPUT_FILE)
        pdf_filename = make_pdf_filename()
        make_invoice(file_content, pdf_filename)
        blank_file(LPT_OUTPUT_FILE)
        spawn_pdf_viewer(pdf_filename)

