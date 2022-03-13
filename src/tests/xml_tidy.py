""" XML tidy function
"""
# (c)2022  Henrique Moreira

# pylint: disable=missing-function-docstring

import sys

INPUT = "capa.xml"


def main():
    tidy_xml(sys.argv[1:])


def tidy_xml(args):
    for fname in args:
        if not fname.endswith(".xml"):
            print("Skipping:", fname)
        did = tidy_rewrite(fname)
        if did:
            print("Rewritten:", fname)


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
    with open(fname, "w", encoding="utf-8") as fdout:
        fdout.write(''.join(res))
    return True


if __name__ == "__main__":
    main()
