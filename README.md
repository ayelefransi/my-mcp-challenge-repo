# News Scraper

Plan (3 steps)
1. Implement fetch/parse/save functionality.
2. Provide a small CLI and list dependencies.
3. Add usage examples.

Install dependencies:

```bash
pip install -r requirements.txt
```

Quick usage:

```bash
python news_scraper.py https://example.com -o headlines.csv -n 20
```

Notes:
- Use `--selector` to tune which elements contain headlines.
- Set `-n 0` to disable the limit (careful on large pages).
