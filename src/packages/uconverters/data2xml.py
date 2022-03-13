""" uconverters.data2xml - universal converters, like json2xml()
"""
import json

# pylint: disable=missing-function-docstring

DEBUG = 1
STRCASE_SORT = False

NORM_PAD = " " * 4
VAR_DOMAIN = "$DOMAIN"


def main():
    an_encode = "ISO-8859-1"
    inp = open("a.json", "r", encoding=an_encode).read()
    json_obj = json.loads(inp)
    astr = json2xml(json_obj)
    print(astr)


def json2xml(json_obj, pad="", level=0):
    res = []
    json_obj_type = type(json_obj)
    if json_obj_type is list:
        for sub_elem in json_obj:
            res.append(json2xml(sub_elem, pad, level + 1))
        return "\n".join(res)
    if json_obj_type is dict:
        for tag_name in dict_sort(json_obj):
            sub_obj = json_obj[tag_name]
            res.extend(from_node(tag_name, sub_obj, pad, level, json_obj))
        return "\n".join(res)
    return f"{pad}{json_obj}"

def from_node(tag_name, sub_obj, pad, level, parent):
    """ Get string list from node """
    assert level < 100, "Too deep!"
    assert parent
    res = []
    if sub_obj is None:
        res = [f"{pad}<{tag_name}/>"]
        return res
    akind, alist = listed_resolve(tag_name, sub_obj, pad)
    if akind and alist:
        hprint("### akind:", akind, alist, end="<<<\n")
        if akind == "ST":
            res = alist
            return res
        assert akind == "NS", f"Uops, akind={akind}!"
        res = to_prop_namespace(tag_name, alist, pad)
        return res
    sub_str = json2xml(sub_obj, NORM_PAD + pad, level + 1)
    assert isinstance(sub_str, str)
    n_lines = sub_str.count("\n")
    if n_lines <= 0:
        left = sub_str.strip()
        res.append(f"{pad}<{tag_name}>{left}</{tag_name}>")
    else:
        res.append(f"{pad}<{tag_name}>")
        res.append(sub_str)
        new = f"{pad}</{tag_name}>"
        res.append(new)
    return res

def listed_resolve(tag_name, sub_obj, pad):
    assert tag_name
    assert isinstance(pad, str)
    if not isinstance(sub_obj, (list, tuple)):
        return None, None
    # If all elements of sub_obj are strings, unify them
    slist = []
    for item in sub_obj:
        if not isinstance(item, str):
            slist = []
            break
        slist.append(f"{pad}<{tag_name}>{item}</{tag_name}>")
    if slist:
        return "ST", slist
    try:
        alist = [(item["#text"], item) for item in sub_obj if item.get("#text") and [key for key in item if key.startswith("@xmlns:")]]
    except AttributeError:
        return None, None
    return "NS", alist

def to_prop_namespace(tag_name:str, alist, pad) -> list:
    res = []
    for left, right in alist:
        assert len(right) == 2, f"to_prop_namespace({tag_name}): {right}"
        atext = right["#text"]
        names = [key for key in right if key.startswith("@")]
        ns_eq = names[0][1:]
        assert ":" in ns_eq, f"Invalid: {ns_eq}"
        astr = f"<{tag_name} {ns_eq}='{VAR_DOMAIN}'>{left}</{tag_name}>"
        res.append(f"{pad}{astr}")
    return res

def dict_sort(json_obj):
    if not STRCASE_SORT:
        return json_obj.keys()
    return sorted(json_obj, key=str.casefold)

def hprint(*args, **kwargs):
    if DEBUG <= 0:
        return
    print(*args, **kwargs)


if __name__ == "__main__":
    main()
