#!/usr/bin/env python
# coding: utf-8

# import streamlit as st
# import pandas as pd
# import sqlite3
# from datetime import datetime
# import pytz
# 
# st.set_page_config(page_title="Tipper Truck", layout="wide")
# st.title("🚛 Tipper Truck Status")
# 
# DB_PATH = "data/tipper.db"
# SG_TZ = pytz.timezone("Asia/Singapore")
# now = datetime.now(SG_TZ).strftime("%Y-%m-%d %H:%M")
# 
# def load_data():
#     conn = sqlite3.connect(DB_PATH)
#     df = pd.read_sql("SELECT * FROM tipper_status", conn)
#     conn.close()
#     return df
# 
# def save_data(df):
#     conn = sqlite3.connect(DB_PATH)
#     df.to_sql("tipper_status", conn, if_exists="replace", index=False)
#     conn.close()
# 
# # -------------------------
# # Upload Excel
# # -------------------------
# st.subheader("📤 Upload Tipper Status (Excel)")
# 
# file = st.file_uploader("Upload Excel", type=["xlsx"])
# 
# if file:
#     df_new = pd.read_excel(file)
#     df_new["last_updated"] = now
#     save_data(df_new)
#     st.success("✅ Tipper truck status updated")
# 
# # -------------------------
# # Display Table
# # -------------------------
# df = load_data()
# 
# st.subheader("📋 Current Tipper Truck Status")
# st.dataframe(
#     df[
#         ["truck_id", "plate_no", "driver",
#          "current_site", "status", "remarks", "last_updated"]
#     ],
#     use_container_width=True
# )
# 

# In[ ]:


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tipper Truck Status", layout="wide")

st.title("🚛 Tipper Truck Status")

st.markdown("""
Upload the **Tipper Truck Status Excel file (.xlsx)**.  
The table will update immediately after upload.
""")

uploaded_file = st.file_uploader(
    "Upload Tipper Truck Status (.xlsx)",
    type=["xlsx"]
)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        required_cols = {
            "truck_id",
            "driver",
            "status",
            "location",
            "remarks",
            "last_update"
        }

        if not required_cols.issubset(df.columns):
            st.error(
                f"Missing columns. Required columns:\n{', '.join(required_cols)}"
            )
        else:
            st.success("Tipper Truck status loaded successfully")

            # Optional filters
            col1, col2 = st.columns(2)

            with col1:
                status_filter = st.selectbox(
                    "Filter by Status",
                    ["All"] + sorted(df["status"].dropna().unique().tolist())
                )

            with col2:
                location_filter = st.selectbox(
                    "Filter by Location",
                    ["All"] + sorted(df["location"].dropna().unique().tolist())
                )

            filtered_df = df.copy()

            if status_filter != "All":
                filtered_df = filtered_df[filtered_df["status"] == status_filter]

            if location_filter != "All":
                filtered_df = filtered_df[filtered_df["location"] == location_filter]

            st.dataframe(
                filtered_df.sort_values("truck_id"),
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Failed to load Excel file: {e}")
else:
    st.info("Please upload a Tipper Truck Status Excel file.")

