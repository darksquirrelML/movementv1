#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from pages import pickup_lorry_v3, Tipper_Truck, Machinery

st.set_page_config(page_title="Vehicle Movement Dashboard", layout="wide")
st.title("🚚 Vehicle Movement Dashboard")

# -------------------------
# Sidebar for page selection
# -------------------------
page = st.sidebar.selectbox(
    "Select Vehicle Type",
    ["Pick-up Lorry", "Tipper Truck", "Machinery"]
)

# -------------------------
# Render selected page
# -------------------------
if page == "Pick-up Lorry":
    pickup_lorry_v3.main()
elif page == "Tipper Truck":
    Tipper_Truck.main()
elif page == "Machinery":
    Machinery.main()

