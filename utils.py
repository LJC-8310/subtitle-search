import jieba

def tokenize_chinese(text):
    return " ".join(jieba.cut(text))


def parse_time(time_str):
    """
    將 '1:23' 或 '45s' 轉成秒數（方便排序）
    """
    if 's' in time_str:
        return int(time_str.replace('s', ''))

    if ':' in time_str:
        parts = time_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])

    return 0