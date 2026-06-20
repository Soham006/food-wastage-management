import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///food.db")

with engine.begin() as conn:
    with open("schema.sql", "r") as f:
        for statement in f.read().split(";"):
            if statement.strip():
                conn.execute(text(statement))

files = [
    ("providers",     "data/providers_data.csv"),
    ("receivers",     "data/receivers_data.csv"),
    ("food_listings", "data/food_listings_data.csv"),
    ("claims",        "data/claims_data.csv"),
]

for table, path in files:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into '{table}'")

print("\nDone. Database saved as food.db")