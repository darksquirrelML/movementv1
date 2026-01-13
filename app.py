#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

st.set_page_config(
    page_title="Vehicle & Machinery Dashboard",
    layout="wide"
)

st.title("🚛 Vehicle & Machinery Status Dashboard")

page = st.sidebar.radio(
    "Select Module",
    [
        "Pick-up Lorry",
        "Tipper Truck",
        "Machinery"
    ]
)

if page == "Pick-up Lorry":
    import pickup_lorry_v3

elif page == "Tipper Truck":
    import Tipper_Truck

elif page == "Machinery":
    import Machinery

