import os
import datetime
import random


BASEDIR = os.path.join(os.path.expanduser("~"), "Documents",
                       "Progetti", "HTML-CSS", "ginger-output")

DOCUMENTS = 1000


def make_a_tag():
    choices = ["ua", "na", "ga"]
    temp_tag = ""
    while len(choices) > 0:
        temp_tag += random.choice(choices)
    return temp_tag


content_dir = os.path.join(BASEDIR, "_content")
if not os.path.exists(content_dir):
    os.mkdir(content_dir)
for index in range(DOCUMENTS):
    doc_name = "document{}.md".format(str(index).zfill(4))
    doc_file = os.path.join(BASEDIR, "_content", doc_name)
    actual_time = datetime.datetime.now().strftime("%Y-%M-%d %h:%m")
    temp = []
    temp.append("----")
    temp.append("Title: This is the document No. {}".format(index))
    temp.append("Date: {}".format(actual_time))
    temp.append("tags: {}".format(make_a_tag()))
    temp.append("----")
    temp.append("\r\n\r\n")
    temp.append("# Header of document no. {}".format(index))
    temp.append("\r\n")
    temp.append("*Hello*, this is the document **no. {}**. Thank you.".format(index))
    f = open(doc_file, "w")
    f.writelines(temp)
    f.close()
