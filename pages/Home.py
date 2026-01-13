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

Use the **sidebar** to navigate:
- 🚐 Pick-up Lorry
- 🚛 Tipper Truck
- 🏗 Machinery

This system helps:
- Track vehicle whereabouts
- Plan and book vehicles
- Upload daily schedules easily
""")

