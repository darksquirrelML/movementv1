#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sqlite3
import pandas as pd

# -------------------------
# Unified DB Path
# -------------------------
DB_PATH = os.path.join("data", "vehicle.db")

def get_connection():
    """Get a SQLite connection to the unified vehicle DB"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# -------------------------
# Table creation (if not exists)
# -------------------------
TABLES = {
    "pickup_schedule": [
        "truck_id TEXT",
        "plate_no TEXT",
        "driver TEXT",
        "current_location TEXT",
        "status TEXT",
        "remarks TEXT",
        "last_update TEXT"
    ],
    "tipper_schedule": [
        "truck_id TEXT",
        "plate_no TEXT",
        "driver TEXT",
        "current_location TEXT",
        "status TEXT",
        "remarks TEXT",
        "last_update TEXT"
    ],
    "machinery_schedule": [
        "machine_id TEXT",
        "machine_name TEXT",
        "operator TEXT",
        "current_location TEXT",
        "status TEXT",
        "remarks TEXT",
        "last_update TEXT"
    ]
}

def init_db():
    """Create all tables if they do not exist"""
    conn = get_connection()
    for table, columns in TABLES.items():
        cols_str = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {table} ({cols_str})"
        conn.execute(sql)
    conn.commit()
    conn.close()

# -------------------------
# Load table into DataFrame
# -------------------------
def load_table(table_name: str) -> pd.DataFrame:
    init_db()
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# -------------------------
# Save DataFrame back to DB
# -------------------------
def save_table(df: pd.DataFrame, table_name: str):
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

# -------------------------
# Seed table from Excel (one-time use)
# -------------------------
def seed_from_excel(table_name: str, excel_file: str):
    df = pd.read_excel(excel_file)
    save_table(df, table_name)

