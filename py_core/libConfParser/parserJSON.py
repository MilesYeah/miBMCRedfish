import json

from jsonpath import jsonpath

from py_core.handlerLogger import logger
from py_core.libConfParser.baseConfParser import BaseConfParser


def json_extractor(obj: dict, expr: str = '.') -> object:
    """
    根据表达式提取字典中的value，表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    :param obj :json/dict类型数据
    :param expr: 表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    $.0.1 提取字典中的第一个列表中的第二个的值
    """
    try:
        result = jsonpath(obj, expr)[0]
    except Exception as e:
        logger.error(f'{expr} - 提取不到内容，丢给你一个错误！{e}')
        result = expr
    return result


def str2json(s: str) -> dict:
    """
    :param s: 长得像字典的字符串
    return json格式的内容
    """
    try:
        if 'None' in s:
            s = s.replace('None', 'null')
        elif 'True' in s:
            s = s.replace('True', 'true')
        elif 'False' in s:
            s = s.replace('False', 'false')
        s = json.loads(s)
    except Exception as e:
        if 'null' in s:
            s = s.replace('null', 'None')
        elif 'true' in s:
            s = s.replace('true', 'True')
        elif 'false' in s:
            s = s.replace('false', 'False')
        s = eval(s)
    return s


class ParserJSON(BaseConfParser):
    def __init__(self, fpn, encoding="utf-8"):
        super().__init__(fpn, encoding="utf-8")


if __name__ == "__main__":
    a = ParserJSON('temp.json')
    v = a.get_group("a")
    v1 = a.get_group("z")

    pass
