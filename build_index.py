import os
import pandas as pd
from whoosh import index
from whoosh.fields import *
from utils import tokenize_chinese, parse_time

# Schema 定義（非常重要）
schema = Schema(
    id=ID(stored=True, unique=True),
    show=TEXT(stored=True),
    season=NUMERIC(stored=True),
    episode=NUMERIC(stored=True),
    time=TEXT(stored=True),
    time_sec=NUMERIC(stored=True),
    en=TEXT(stored=True),
    zh=TEXT(stored=True),
    zh_tokens=TEXT
)

# 建立 index 資料夾
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = index.create_in("indexdir", schema)
writer = ix.writer()

DATA_DIR = "data"

doc_id = 0

for show_name in os.listdir(DATA_DIR):
    show_path = os.path.join(DATA_DIR, show_name)

    for file in os.listdir(show_path):
        if file.endswith(".xlsx"):
            path = os.path.join(show_path, file)

            df = pd.read_excel(path)

            # 解析檔名
            parts = file.replace(".xlsx", "").split("_")
            season = int(parts[0][1:])
            episode = int(parts[1][1:])

            for _, row in df.iterrows():
                zh = str(row["Human Translation"])
                en = str(row["Subtitle"])
                time_str = str(row["Time"])

                zh_tokens = tokenize_chinese(zh)

                writer.add_document(
                    id=str(doc_id),
                    show=show_name,
                    season=season,
                    episode=episode,
                    time=time_str,
                    time_sec=parse_time(time_str),
                    en=en,
                    zh=zh,
                    zh_tokens=zh_tokens
                )

                doc_id += 1

writer.commit()
print("Index built!")