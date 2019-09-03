import re

'''
特殊なタグを使用してフォーマットする。
「{」「}」との競合を防ぐ。

【書式】
[param(XXX)]
XXX部分に引数名を入力する。

【例】
str = "Hi, [param(name)]!"
print(formatText(str, {"name": "somewho"})

画面には「Hi, somewho!」と表示される。

'''

__start_tag = "@parentness_started@"
__finish_tag = "@parentness_finished@"

def startFormatting(data):
    tmp_data = data
    tmp_data = tmp_data.replace("{", __start_tag)
    tmp_data = tmp_data.replace("}", __finish_tag)
    return re.sub("\[param\((.+?)\)\]", "{\\1}", tmp_data)

def decodeParentness(data):
    return data.replace(__start_tag, "{").replace(__finish_tag, "}")

def formatText(raw, params):
    raw_encoded = startFormatting(raw)
    raw_encoded = raw_encoded.format(**params)
    return decodeParentness(raw_encoded)