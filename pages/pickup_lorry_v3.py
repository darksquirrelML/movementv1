#!/usr/bin/env python
# coding: utf-8

# import streamlit as st
# import pandas as pd
# from db import load_table, save_table, seed_from_excel
# 
# st.set_page_config(page_title="Pick-up Lorry", layout="wide")
# st.title("🚐 Pick-up Lorry Availability & Whereabout")
# 
# # -------------------------
# # Excel upload (Clerk-friendly)
# # -------------------------
# uploaded_file = st.file_uploader(
#     "Upload Pick-up Lorry Schedule (Excel)", type=["xlsx"]
# )
# if uploaded_file:
#     seed_from_excel("pickup_schedule", uploaded_file)
#     st.success("✅ Schedule uploaded successfully.")
# 
# # -------------------------
# # Load current schedule from DB
# # -------------------------
# df = load_table("pickup_schedule")
# 
# # -------------------------
# # Current time
# # -------------------------
# from datetime import datetime
# import pytz
# 
# sg_timezone = pytz.timezone("Asia/Singapore")
# now_time = datetime.now(sg_timezone).time()
# st.caption(f"🕒 Current Time (SG): {now_time.strftime('%H:%M')}")
# 
# # -------------------------
# # Available now
# # -------------------------
# st.subheader("🟢 Available Now")
# 
# # Ensure time columns are datetime.time
# df["time_start"] = pd.to_datetime(df.get("time_start", "00:00")).dt.time
# df["time_end"] = pd.to_datetime(df.get("time_end", "23:59")).dt.time
# 
# available_now = df[
#     (df["status"] == "Available") &
#     (df["time_start"] <= now_time) &
#     (df["time_end"] >= now_time)
# ]
# 
# if available_now.empty:
#     st.warning("No pick-up lorry available at this time.")
# else:
#     st.dataframe(
#         available_now[["truck_id","plate_no","driver","current_location","time_start","time_end","remarks"]],
#         use_container_width=True
#     )
# 
# # -------------------------
# # Today's schedule
# # -------------------------
# st.subheader("📅 Today's Pick-up Lorry Schedule")
# vehicle_filter = st.multiselect(
#     "Filter by Vehicle",
#     df["truck_id"].unique(),
#     default=df["truck_id"].unique()
# )
# filtered_df = df[df["truck_id"].isin(vehicle_filter)]
# st.dataframe(filtered_df.sort_values(["truck_id", "time_start"]), use_container_width=True)
# 
# # -------------------------
# # Driver Whereabout Update
# # -------------------------
# st.subheader("📍 Driver Whereabout Update (Auto-Save)")
# 
# with st.form("driver_update"):
#     vehicle = st.selectbox("Vehicle", df["truck_id"].unique())
#     location = st.text_input("Current Location / Site Code", placeholder="e.g. P201, P202, Dormitory")
#     status = st.selectbox("Status", ["Available", "Busy"])
#     remarks = st.text_input("Remarks")
#     submit = st.form_submit_button("Update Whereabout")
# 
# if submit:
#     # Update the DB
#     mask = df["truck_id"] == vehicle
#     if mask.any():
#         df.loc[mask, "current_location"] = location
#         df.loc[mask, "status"] = status
#         df.loc[mask, "remarks"] = remarks
#         df.loc[mask, "last_update"] = datetime.now(sg_timezone).strftime("%Y-%m-%d %H:%M")
#         save_table(df, "pickup_schedule")
#         st.success("✅ Whereabout updated and saved.")
# 

# In[ ]:


import streamlit as st
import pandas as pd
from db import load_table, save_table, seed_from_excel
from datetime import datetime
import pytz

st.set_page_config(page_title="Pick-up Lorry", layout="wide")
st.title("🚐 Pick-up Lorry Availability & Whereabout")

# -------------------------
# Excel upload
# -------------------------
uploaded_file = st.file_uploader(
    "Upload Pick-up Lorry Schedule (Excel)", type=["xlsx"]
)
if uploaded_file:
    seed_from_excel("pickup_schedule", uploaded_file)
    st.success("✅ Schedule uploaded successfully.")

# -------------------------
# Load data
# -------------------------
df = load_table("pickup_schedule")

if df.empty:
    st.info("No data found. Please upload schedule.")
    st.stop()

# -------------------------
# Current time (SG)
# -------------------------
sg_tz = pytz.timezone("Asia/Singapore")
now_time = datetime.now(sg_tz).time()
st.caption(f"🕒 Current Time (SG): {now_time.strftime('%H:%M')}")

# -------------------------
# Time conversion (SAFE)
# -------------------------
df["time_start"] = pd.to_datetime(df["time_start"], errors="coerce").dt.time
df["time_end"] = pd.to_datetime(df["time_end"], errors="coerce").dt.time

# -------------------------
# Available Now
# -------------------------
st.subheader("🟢 Available Now")

available_now = df[
    (df["status"] == "Available") &
    (df["time_start"] <= now_time) &
    (df["time_end"] >= now_time)
]

if available_now.empty:
    st.warning("No pick-up lorry available now.")
else:
    st.dataframe(
        available_now[
            ["truck_id", "plate_no", "driver",
             "current_location", "time_start", "time_end", "remarks"]
        ],
        use_container_width=True
    )

# -------------------------
# Full schedule
# -------------------------
st.subheader("📅 Today's Pick-up Lorry Schedule")

vehicle_filter = st.multiselect(
    "Filter by Vehicle",
    df["truck_id"].unique(),
    default=df["truck_id"].unique()
)

st.dataframe(
    df[df["truck_id"].isin(vehicle_filter)]
    .sort_values(["truck_id", "time_start"]),
    use_container_width=True
)

# -------------------------
# Whereabout update
# -------------------------
st.subheader("📍 Driver Whereabout Update")

with st.form("update_form"):
    vehicle = st.selectbox("Vehicle", df["truck_id"].unique())
    location = st.text_input("Current Location / Site Code")
    status = st.selectbox("Status", ["Available", "Busy"])
    remarks = st.text_input("Remarks")
    submit = st.form_submit_button("Update")

if submit:
    mask = df["truck_id"] == vehicle
    df.loc[mask, "current_location"] = location
    df.loc[mask, "status"] = status
    df.loc[mask, "remarks"] = remarks
    df.loc[mask, "last_update"] = datetime.now(sg_tz).strftime("%Y-%m-%d %H:%M")
    save_table(df, "pickup_schedule")
    st.success("✅ Updated successfully")

