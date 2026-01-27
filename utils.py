import re
import json



def clean_and_split(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # 将换行符当成句子的自然分界
    text = text.replace("\n", ". ")

    # 清洗：保留字母数字空格和句号/问号/感叹号
    text = re.sub(r"[^A-Za-z0-9\s\.\!\?]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # 分句：按 . ! ? 切分
    sentences = re.split(r'(?<=[\.!?])\s+', text)

    # 清理空句
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [re.sub(r'\.$', "", s) for s in sentences]
    
    return sentences

def normalize_s_code(name: str) -> str:
    """将 Sxx yyyyy Xxx 统一为 Sxx_yyyyy Xxx"""
    if not isinstance(name, str):
        return name
    name = name.strip()

    # 匹配：S20 03001..., S20_03001..., S2003001... 都兼容
    m = re.match(r"^(S\d{2})[ _]?(\d{5})(.*)$", name)
    if not m:
        return name
    prefix, code, rest = m.groups()

    return f"{prefix}_{code}{rest}".strip()


def fix_operations(data: dict) -> dict:
    """修正 JSON 中所有 operation_name 和 precedence"""
    for op in data.get("operations", []):
        # 修正 operation_name
        old_name = op.get("operation_name")
        new_name = normalize_s_code(old_name)
        op["operation_name"] = new_name

        # 修正 precedence
        prec = op.get("precedence")
        if prec is not None:
            op["precedence"] = normalize_s_code(prec)

    return data
