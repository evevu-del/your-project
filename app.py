import json

import requests
import streamlit as st


st.set_page_config(page_title="Streamlit + Requests Demo", layout="centered")
st.title("Streamlit + Requests")
st.caption("Fetch a URL and preview the response.")

url = st.text_input("URL", value="https://api.github.com", help="Try any public JSON endpoint.")
timeout = st.number_input("Timeout (seconds)", min_value=1, max_value=60, value=10)

col1, col2 = st.columns([1, 1])
with col1:
    fetch = st.button("Fetch", type="primary")
with col2:
    show_headers = st.checkbox("Show headers", value=False)

if fetch:
    try:
        resp = requests.get(url, timeout=float(timeout))
        st.write(f"Status: {resp.status_code}")

        if show_headers:
            st.json(dict(resp.headers))

        content_type = resp.headers.get("content-type", "")
        if "application/json" in content_type.lower():
            st.json(resp.json())
        else:
            try:
                parsed = json.loads(resp.text)
                st.json(parsed)
            except Exception:
                st.text(resp.text[:5000])
    except Exception as e:
        st.error(f"Request failed: {e}")
