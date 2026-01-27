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
