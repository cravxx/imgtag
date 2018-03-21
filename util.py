import os

def write_tag(file,namespace="",tag=""):
    file.write((namespace + (":" if tag != "" else "") + str(tag) + os.linesep).encode("utf_8"))