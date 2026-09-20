"""
summarize.py
------------
Phase 3, Step 4: "Turn raw results into a plain-English answer."

This makes a SECOND call to the AI — not to write SQL this time,
but to look at the table of results and explain it in plain
English, like a business analyst would.
"""

import os
import time
import pandas as pd
from google import genai
from google.genai import errors as genai_errors
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.6-flash"

def _call_gemini_with_retry(prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
        except genai_errors.ServerError as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise

def summarize_results(question: str, results: pd.DataFrame) -> str:
    """
    Given the original question and the data that answered it,
    returns a 1-2 sentence plain-English summary.
    """
    # Convert the DataFrame to a small, readable text table.
    # (If it's a huge result, only show the first 20 rows to the AI.)
    data_preview = results.head(20).to_string(index=False)

    prompt = f"""A user asked this business question: "{question}"

Here is the data that answers it:
{data_preview}

Summarize the answer in 1-2 plain-English sentences, as if
explaining it to a non-technical business stakeholder. Mention
specific numbers or names from the data where relevant.
"""

    response = _call_gemini_with_retry(prompt)
    return response.text.strip()


if __name__ == "__main__":
    # Quick manual test with fake data
    sample_df = pd.DataFrame({
        "category": ["Dairy", "Snacks", "Beverages"],
        "stock_out_rate": [0.32, 0.21, 0.15],
    })
    print(summarize_results("Which category has the highest stock-out risk?", sample_df))
