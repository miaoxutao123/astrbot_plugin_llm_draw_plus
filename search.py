from duckduckgo_search import DDGS

proxy = "http://43.131.5.106:3698"

try:
    ddgs = DDGS(proxy=proxy)
    keywords = "人工智能"
    results = ddgs.text(keywords, max_results=5)

    if results:
        print(f"搜索 '{keywords}' 的结果:")
        for i, r in enumerate(results):
            print(f"--- 结果 {i+1} ---")
            print(f"标题: {r['title']}")
            print(f"链接: {r['href']}")
            print(f"摘要: {r['body']}")
            print("-" * 20)
    else:
        print("没有找到任何结果。")

except Exception as e:
    print(f"发生错误: {e}")