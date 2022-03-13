""" uconverters.data2xml - universal converters, like json2xml()
"""
import json

# pylint: disable=missing-function-docstring

NORM_PAD = " " * 4


def main():
    an_encode = "ISO-8859-1"
    inp = open("a.json", "r", encoding=an_encode).read()
    json_obj = json.loads(inp)
    astr = json2xml(json_obj)
    print(astr)


def json2xml(json_obj, pad=""):
    res = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            res.append(json2xml(sub_elem, pad))

        return "\n".join(res)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            sub_str = json2xml(sub_obj, NORM_PAD + pad)
            n_lines = sub_str.count("\n")
            if n_lines <= 0:
                left = sub_str.strip()
                res.append(f"{pad}<{tag_name}>{left}</{tag_name}>")
            else:
                res.append(f"{pad}<{tag_name}>")
                res.append(sub_str)
                res.append(f"{pad}</{tag_name}>")
        return "\n".join(res)

    return f"{pad}{json_obj}"


if __name__ == "__main__":
    main()
