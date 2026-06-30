from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DB_URL")

engine = create_engine(
    db_url
)

def load_library(limit=1000):

    query = """
        SELECT
            id,
            name,
            smiles
        FROM structures
        WHERE smiles IS NOT NULL
    """

    if limit:
        query += f" LIMIT {limit}"

    return pd.read_sql(query, engine)