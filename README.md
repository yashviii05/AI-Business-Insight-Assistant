# AI-Powered Business Insight Assistant

Ask a business question in plain English — get back the SQL query used,
the data, and a plain-English summary. No SQL knowledge required to use it.

## How it works

```
User's question
      |
      v
Claude (writes SQL) --> PostgreSQL database (runs the query)
      |                          |
      v                          v
Safety check                Raw results
      |                          |
      +-----------+--------------+
                  |
                  v
        Claude (summarizes results)
                  |
                  v
        Plain-English answer shown to user
```

## Files

| File            | What it does                                              |
|-----------------|------------------------------------------------------------|
| `db.py`         | Connects to your PostgreSQL database                       |
| `schema_utils.py` | Reads your table/column names so the AI knows your data  |
| `nl_to_sql.py`  | Turns a plain-English question into SQL, then runs it       |
| `safety.py`     | Blocks any destructive SQL (only SELECT is allowed)         |
| `summarize.py`  | Turns raw query results into a plain-English answer         |
| `logger.py`     | Logs every question asked, for measuring accuracy later     |
| `app.py`        | The Streamlit website that ties everything together         |

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your real Anthropic API key
   and PostgreSQL credentials.
3. Test your database connection:
   ```
   python db.py
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```
5. Open the local URL Streamlit gives you (usually http://localhost:8501)
   in your browser.

## Results (fill this in after testing)

- Tested with __ questions
- Achieved __% valid SQL generation rate (run `python logger.py` to check)

## Resume line (example)

> Built an AI-powered natural language-to-SQL tool using the Claude API
> and PostgreSQL, achieving __% valid query generation across __ test
> questions, with plain-English summarization of results.
