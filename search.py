from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from utils import tokenize_chinese

ix = open_dir("indexdir")

def search_subtitles(query_str, mode="OR"):
    with ix.searcher() as searcher:

        zh_query = tokenize_chinese(query_str)

        parser = MultifieldParser(["en", "zh_tokens"], schema=ix.schema)

        query = parser.parse(query_str + " " + zh_query)

        results = searcher.search(query, limit=50)

        data = []
        for r in results:
            data.append({
                "show": r["show"],
                "season": r["season"],
                "episode": r["episode"],
                "time": r["time"],
                "en": r["en"],
                "zh": r["zh"]
            })

        # 排序
        data.sort(key=lambda x: (x["season"], x["episode"]))

        return data