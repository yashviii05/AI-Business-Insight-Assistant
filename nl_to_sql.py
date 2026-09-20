"""
nl_to_sql.py
------------
Phase 2, Steps 2-5:
  Step 2: Write the prompt (the instructions we send the AI)
  Step 3: Send that prompt to the AI
  Step 4: Clean up the AI's response
  Step 5: Run the resulting SQL against the real database
"""

import os
import re
import time
import pandas as pd
from google import genai
from google.genai import errors as genai_errors
from dotenv import load_dotenv

from db import get_connection
from schema_utils import get_schema_text
from safety import is_query_safe

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"  # fast, free-tier friendly model

def _call_gemini_with_retry(prompt: str, max_retries: int = 3):
    """
    Calls Gemini and automatically retries if the server is
    temporarily overloaded (a 503 error). Waits a bit longer
    between each retry (2s, 4s, 8s) before giving up.
    """
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
        except genai_errors.ServerError as e:
            if attempt < max_retries - 1:
                wait_seconds = 2 ** (attempt + 1)  # 2, 4, 8 seconds
                time.sleep(wait_seconds)
            else:
                raise

def generate_sql(question: str) -> str:
    """
    Step 2 + 3: Build the prompt and send it to Gemini.
    Returns the raw text Gemini replies with.
    """
    schema = get_schema_text()

    # This prompt is the most important part of the whole project —
    # it tells the AI exactly what data exists and exactly what
    # format we want its answer in.
    prompt = f"""You are a PostgreSQL expert.

Here is the database schema:
{schema}

Convert the following question into a single valid PostgreSQL SELECT query.
Only return the raw SQL query. Do not include explanations, comments,
or markdown code fences (no ```sql).

Question: {question}
"""
    response = _call_gemini_with_retry(prompt)
    return response.text   

def clean_sql(raw_text: str) -> str:
    """
    Step 4: Strip out any accidental markdown formatting the AI
    might add (like ```sql ... ```), leaving just the SQL itself.
    """
    cleaned = re.sub(r"```sql|```", "", raw_text)
    return cleaned.strip()


def run_query(sql_query: str) -> pd.DataFrame:
    """
    Step 5: Actually execute the SQL against Postgres and return
    the results as a pandas DataFrame (an easy-to-read table).
    """
    conn = get_connection()
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df


def ask_question(question: str):
    """
    Ties Steps 2-5 together. Given a plain-English question, returns:
      - the SQL that was generated
      - the resulting data (as a DataFrame), or an error message
    """
    raw_response = generate_sql(question)
    sql_query = clean_sql(raw_response)

    safe, reason = is_query_safe(sql_query)
    if not safe:
        return sql_query, None, f"Blocked for safety: {reason}"

    try:
        results = run_query(sql_query)
        return sql_query, results, None
    except Exception as e:
        return sql_query, None, f"Query failed: {e}"


if __name__ == "__main__":
    # Run "python nl_to_sql.py" to test this file on its own.
    sql, results, error = ask_question("Which 3 products have the highest discounts in all the categories")
    print("Generated SQL:\n", sql)
    if error:
        print("Error:", error)
    else:
        print(results)
