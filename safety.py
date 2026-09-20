"""
safety.py
---------
Phase 3, Steps 1-3: Make sure the SQL the AI writes can never
change or delete data — only read it.
"""

# Any query containing these words is rejected, no matter what.
FORBIDDEN_KEYWORDS = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]


def is_query_safe(sql_query: str) -> tuple[bool, str]:
    """
    Checks a SQL query before it's allowed to run.
    Returns (True, "") if safe, or (False, reason) if not.
    """
    upper_query = sql_query.upper()

    # Rule 1: must start with SELECT (a "read-only" query).
    if not upper_query.strip().startswith("SELECT"):
        return False, "Only SELECT (read-only) queries are allowed."

    # Rule 2: must not contain any destructive keywords anywhere.
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in upper_query:
            return False, f"Query contains a forbidden keyword: {keyword}"

    return True, ""


if __name__ == "__main__":
    # Quick manual tests
    tests = [
        "SELECT * FROM products;",
        "DELETE FROM products;",
        "UPDATE products SET price = 0;",
    ]
    for t in tests:
        print(t, "->", is_query_safe(t))
