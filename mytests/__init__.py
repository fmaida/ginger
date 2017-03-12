import os
import datetime
import random
import shutil


BASEDIR = os.path.join(os.path.expanduser("~"), "Documents",
                       "Progetti", "HTML-CSS", "ginger-output")

DOCUMENTS = 500
PREFIX = "element"


def make_a_tag():
    choices = ["ua", "na", "ga"]
    temp_tag = ""
    random.shuffle(choices)
    while len(choices) > 0:
        temp_tag += choices.pop()
    return temp_tag


def create(documents=DOCUMENTS):

    content_dir = os.path.join(BASEDIR, "_content")
    images_dir = os.path.join(BASEDIR, "_images")
    if os.path.exists(content_dir):
        shutil.rmtree(content_dir)
    os.mkdir(content_dir)
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)
    os.mkdir(images_dir)

    doclist = list(range(documents))
    for index in doclist:
        doc_name = "{}{}.md".format(PREFIX, str(index+1).zfill(4))
        doc_file = os.path.join(BASEDIR, "_content", doc_name)
        actual_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%m")
        temp = []
        temp.append("----")
        temp.append("Title: This is the element no. {}".format(index+1))
        temp.append("Date:  {}".format(actual_time))
        temp.append("Tags:  {}".format(make_a_tag()))
        temp.append("----")
        temp.append("\r\n")
        temp.append("# Header of element no. {}".format(index+1))
        temp.append("")
        temp.append("*{}*, this is the element **no. {}**. {}.".format(
            random.choice(["Hello", "Good day", "Greetings", "Hi"]),
            index+1,
            random.choice(["Thank you", "Thank you very much", "Goodbye"])))
        f = open(doc_file, "w")
        for linea in temp:
            f.write(linea + "\r\n")
        f.close()

    random.shuffle(doclist)
    doclist = doclist[:(documents//2)]
    for index in doclist:
        img_name = "{}{}.jpg".format(PREFIX, str(index + 1).zfill(4))
        img_file = os.path.join(BASEDIR, "_images", img_name)
        f = open(img_file, "wb")
        f.write(b".")
        f.close()

    doclist = doclist[:(documents//4)]
    for index in doclist:
        img_name = "{}{}--2.jpg".format(PREFIX, str(index + 1).zfill(4))
        img_file = os.path.join(BASEDIR, "_images", img_name)
        f = open(img_file, "wb")
        f.write(b".")
        f.close()

    doclist = doclist[:(documents//8)]
    for index in doclist:
        img_name = "{}{}--3.png".format(PREFIX, str(index + 1).zfill(4))
        img_file = os.path.join(BASEDIR, "_images", img_name)
        f = open(img_file, "wb")
        f.write(b".")
        f.close()

    img_name = "{}{}--999.png".format(PREFIX, str(1).zfill(4))
    f = open(img_file, "wb")
    f.write(b".")
    f.close()


