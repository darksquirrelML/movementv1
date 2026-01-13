#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import pytz

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Machinery Status",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Machinery Status Dashboard")

# -------------------------
# DATABASE
# -------------------------
DB_PATH = "data/machinery.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def load_data():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM machinery_status", conn)
    conn.close()
    return df

def save_data(df):
    conn = get_conn()
    df.to_sql("machinery_status", conn, if_exists="replace", index=False)
    conn.close()

# -------------------------
# TIME (Singapore)
# -------------------------
SG_TZ = pytz.timezone("Asia/Singapore")
now_dt = datetime.now(SG_TZ)
now_str = now_dt.strftime("%Y-%m-%d %H:%M")

st.caption(f"🕒 Last refreshed (SG): **{now_str}**")

# -------------------------
# UPLOAD MACHINERY STATUS
# -------------------------
st.subheader("📤 Upload Machinery Status (Excel)")

uploaded_file = st.file_uploader(
    "Select Excel file (.xlsx)",
    type=["xlsx"],
    help="Required columns: machine_id, machine_type, site, status, operator, remarks"
)

if uploaded_file:
    try:
        new_df = pd.read_excel(uploaded_file)

        required_cols = [
            "machine_id",
            "machine_type",
            "site",
            "status",
            "operator",
            "remarks"
        ]

        missing = [c for c in required_cols if c not in new_df.columns]
        if missing:
            st.error(f"❌ Missing columns: {missing}")
        else:
            new_df["last_updated"] = now_str
            save_data(new_df)
            st.success("✅ Machinery status updated successfully")

    except Exception as e:
        st.error(f"Upload failed: {e}")

# -------------------------
# LOAD & DISPLAY DATA
# -------------------------
try:
    df = load_data()

    st.subheader("📋 Current Machinery Status")

    # Optional filter
    site_filter = st.multiselect(
        "Filter by Site",
        df["site"].unique(),
        default=df["site"].unique()
    )

    filtered_df = df[df["site"].isin(site_filter)]

    st.dataframe(
        filtered_df[
            [
                "machine_id",
                "machine_type",
                "site",
                "status",
                "operator",
                "remarks",
                "last_updated"
            ]
        ],
        use_container_width=True
    )

except Exception:
    st.info("No machinery data found. Please upload an Excel file.")

