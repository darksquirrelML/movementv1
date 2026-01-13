#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

st.set_page_config(
    page_title="Vehicle Movement Dashboard",
    layout="wide"
)

st.title("🚚 Vehicle Movement Dashboard")

st.markdown("""
### Welcome

Use the **sidebar on the left** to navigate:
- 🚐 Pick-up Lorry
- 🚛 Tipper Truck
- 🏗 Machinery

This system allows:
- Clerks to upload schedules (Excel)
- Drivers to update whereabouts
- Engineers to check availability in real-time
""")

