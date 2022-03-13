""" Functional json to json, and backwards
"""
# (c)2022  Henrique Moreira

# pylint: disable=missing-function-docstring

import sys
import os.path
import json
import uconverters.data2xml as data2xml

# export PYTHONPATH=~/retokenize/src/external/paconv/src/packages

INPUT = "capa.json"
OUTPUT = "capa.new.xml"


def main():
    run_script(sys.argv[1:])

def run_script(args):
    param = args
    if param:
        domain = param[0]
        del param[0]
    else:
        domain = ""
    size = to_xml(INPUT, OUTPUT, {"domain": domain})
    assert size != 0
    if size == -1:
        print("# Not re-written:", OUTPUT)


def to_xml(json_fname:str, out_file:str, opts:dict):
    jdata = json.loads(open(json_fname, "r", encoding="utf-8").read())
    astr = data2xml.json2xml(jdata)
    if os.path.isfile(out_file):
        return -1
    domain = opts["domain"]
    data = astr.replace(data2xml.VAR_DOMAIN, domain) if domain else astr
    with open(out_file, "wb") as fdout:
        bytes_written = fdout.write(data.encode("utf-8"))
    return bytes_written


if __name__ == "__main__":
    main()
