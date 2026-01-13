#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import pytz

st.set_page_config(page_title="Tipper Truck", layout="wide")
st.title("🚛 Tipper Truck Status")

DB_PATH = "data/tipper.db"
SG_TZ = pytz.timezone("Asia/Singapore")
now = datetime.now(SG_TZ).strftime("%Y-%m-%d %H:%M")

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM tipper_status", conn)
    conn.close()
    return df

def save_data(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("tipper_status", conn, if_exists="replace", index=False)
    conn.close()

# -------------------------
# Upload Excel
# -------------------------
st.subheader("📤 Upload Tipper Status (Excel)")

file = st.file_uploader("Upload Excel", type=["xlsx"])

if file:
    df_new = pd.read_excel(file)
    df_new["last_updated"] = now
    save_data(df_new)
    st.success("✅ Tipper truck status updated")

# -------------------------
# Display Table
# -------------------------
df = load_data()

st.subheader("📋 Current Tipper Truck Status")
st.dataframe(
    df[
        ["vehicle_id", "plate_no", "driver",
         "current_site", "status", "remarks", "last_updated"]
    ],
    use_container_width=True
)

