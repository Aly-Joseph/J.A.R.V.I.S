# internet.py — SAFE DUCKDUCKGO SEARCH

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None


def internet_search(query: str) -> str:
    if DDGS is None:
        return "Internet search module is not available."

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            answers = []
            for r in results:
                answers.append(r.get("body", ""))

            return " ".join(answers) if answers else "No results found."
    except Exception:
        return "Unable to fetch live internet data."
