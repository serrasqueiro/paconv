""" Functional xml to json, and backwards
"""
# (c)2022  Henrique Moreira

# pylint: disable=missing-function-docstring, line-too-long

import os.path
import json
import xmltodict
import uconverters.data2xml as data2xml

# export PYTHONPATH=~/retokenize/src/external/xmltodict:~/retokenize/src/external/paconv/src/packages

INPUT = "capa.xml"
OUTPUT = "capa.json"


def main():
    size = to_json(INPUT, OUTPUT)
    assert size != 0
    if size == -1:
        print("# Not re-written:", OUTPUT)
    jdata = json.loads(open(OUTPUT, "r", encoding="utf-8").read())
    #print(jdata)
    astr = data2xml.json2xml(jdata)
    print(astr)


def to_json(in_file:str, out_file:str) -> int:
    astr = open(in_file, "r").read()
    obj = xmltodict.parse(astr)
    new = json.dumps(obj, ensure_ascii=False, indent=2)
    if os.path.isfile(out_file):
        return -1
    with open(out_file, "w", encoding="utf-8") as fdout:
        bytes_written = fdout.write(new)
    return bytes_written


if __name__ == "__main__":
    main()
