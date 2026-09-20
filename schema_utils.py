"""
schema_utils.py
----------------
Phase 2, Step 1: "Teach the AI what your database looks like."

The AI has never seen your database, so before we ask it anything,
we pull the list of tables and columns out of Postgres and turn it
into a plain-text description we can hand to the AI in our prompt.
"""

from db import get_connection


def get_schema_text():
    """
    Returns a plain-text description of every table and column
    in the public schema, e.g.:

    Table: products
      - product_id (integer)
      - category (character varying)
      - price (numeric)
    """
    conn = get_connection()
    cursor = conn.cursor()

    # information_schema.columns is a built-in Postgres table that
    # already knows every table/column in your database.
    cursor.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    schema_by_table = {}
    for table_name, column_name, data_type in rows:
        schema_by_table.setdefault(table_name, []).append(f"{column_name} ({data_type})")

    lines = []
    for table_name, columns in schema_by_table.items():
        lines.append(f"Table: {table_name}")
        for col in columns:
            lines.append(f"  - {col}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Run "python schema_utils.py" to see your schema printed out.
    print(get_schema_text())
