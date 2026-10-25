import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# The "engine" is SQLAlchemy's connection to the database
engine = create_engine(os.environ["DATABASE_URL"])

RAW_DIR = Path("data/raw")


def table_name_from_file(path: Path) -> str:
    # "olist_order_items_dataset.csv" -> "order_items"
    name = path.stem                      # file name without .csv
    name = name.removeprefix("olist_")
    name = name.removesuffix("_dataset")
    return name


def is_date_column(col: str) -> bool:
    # Olist date columns end with _timestamp, _date or _at
    return col.endswith(("_timestamp", "_date", "_at"))


for csv_path in sorted(RAW_DIR.glob("*.csv")):
    table = table_name_from_file(csv_path)

    # utf-8-sig removes a hidden BOM character that some CSV files start with
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # Convert text dates into real timestamps
    for col in df.columns:
        if is_date_column(col):
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Create the table in Postgres (replace it if it already exists)
    df.to_sql(table, engine, if_exists="replace", index=False, chunksize=10_000)
    print(f"{table:40s} {len(df):>10,} rows")

# Double-check from the database side: which tables exist now?
with engine.connect() as conn:
    tables = conn.execute(text(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = 'public' ORDER BY table_name"
    )).all()
    print("\nTables in Postgres:", tables)