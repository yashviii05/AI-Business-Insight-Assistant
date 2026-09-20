"""
fast_csv_load.py
------------------
A much faster alternative to pgAdmin's Import/Export tool.

pgAdmin's GUI importer inserts rows one at a time, which is slow
even for small files. This script uses PostgreSQL's native COPY
command instead, which loads the entire file in one bulk operation —
3,700 rows should take under a second.

Run it once:
    python fast_csv_load.py
"""

import os
from db import get_connection

# --- EDIT THESE LINES ---
CSV_PATH = "zepto_v2.csv"        # path to your CSV file
TABLE_NAME = "zepto"             # the table you want to load into

# Maps each CSV column (in the CSV's own order) to the matching
# table column. sku_id is deliberately left out — it's a SERIAL
# column, so Postgres auto-generates it for every row on its own.
CSV_COLUMNS = "category, name, mrp, discount_percent, avl_quantity, disc_sellingprice, weightingrams, outofstock, quantity"
# -----------------------------

conn = get_connection()
cursor = conn.cursor()

with open(CSV_PATH, "r", encoding="utf-8") as f:
    # copy_expert lets us run a COPY command and stream the file
    # directly into Postgres — this is the same mechanism \copy uses.
    # Specifying CSV_COLUMNS tells Postgres exactly which CSV column
    # maps to which table column, instead of guessing by position.
    cursor.copy_expert(
        f"COPY {TABLE_NAME} ({CSV_COLUMNS}) FROM STDIN WITH (FORMAT csv, HEADER true)",
        f,
    )

conn.commit()

# Confirm how many rows are now in the table
cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
row_count = cursor.fetchone()[0]

cursor.close()
conn.close()

print(f"Done. '{TABLE_NAME}' now has {row_count} rows.")
