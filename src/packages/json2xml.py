import json


NORM_PAD = " " * 2


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
            res.append("%s<%s>" % (pad, tag_name))
            res.append(json2xml(sub_obj, NORM_PAD + pad))
            res.append("%s</%s>" % (pad, tag_name))

        return "\n".join(res)

    return "%s%s" % (pad, json_obj)


main()
