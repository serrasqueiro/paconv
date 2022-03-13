""" XML tidy function
"""
# (c)2022  Henrique Moreira

# pylint: disable=missing-function-docstring

import sys
import os

INPUT = "capa.xml"  # default XML file to tidy


def main():
    success = tidy_xml(sys.argv[1:])
    if success is None:
        print(f"""Usage:
{__file__} [xml-file1 ...]
""")

def tidy_xml(args):
    if args:
        param = args
        if param[0].startswith(("-h", "--help")):
            return None
    else:
        param = [INPUT]
    for fname in param:
        if not fname.endswith(".xml"):
            print("Skipping:", fname)
        did = tidy_rewrite(fname)
        if did:
            print("Rewritten:", fname)
        else:
            print("Nothing changed:", fname)
    return True

def tidy_rewrite(fname:str):
    with open(fname, "r", encoding="utf-8") as fdin:
        lines = fdin.readlines()
    did, min_blk = False, 10 ** 6	# or sys.maxsize
    for num, line in enumerate(lines, 1):
        assert "\t" not in line, f"Tab not allowed, line {num}: {line}"
        assert len(line) >= 1, f"Empty line: {num}"
        for achr in line[:-1]:
            anum = ord(achr)
            assert achr >= ' ', f"Bad char (0x{anum:02x}={anum}d) in line {num}"
        left = line.lstrip(" ")
        diff = len(line) - len(left)
        if diff < min_blk:
            did = diff > 0
            min_blk = diff
    #print(min_blk, "; num lines:", num)
    if not did:
        return False
    fdin.close()
    res = [line[min_blk:] for line in lines]
    #print(''.join(res), end='')
    data = ''.join(res)
    with open(fname, "w", encoding="utf-8") as fdout:
        fdout.write(data)
    if os.name == "nt":
        fdout.close()
        with open(fname, "wb") as fdout:
            fdout.write(data.encode("utf-8"))
    return True


if __name__ == "__main__":
    main()
