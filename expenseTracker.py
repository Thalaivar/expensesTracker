import streamlit as st
from cacheutils import Cache
from parsers import icici

def upload_files(cache):
    col1, col2 = st.columns(2)
    with col1:
        icici_file = st.file_uploader("Upload ICICI Statement:", type=[ "pdf"])
    with col2:
        dbs_file = st.file_uploader("Upload DBS statement:", type=["pdf"])

    if icici_file:
        df = icici.parse(icici_file)
        cache.add_to_raw(df)
    
    if dbs_file:
        df = icici.parse(dbs_file)
        cache.add_to_raw(df)

def run():
    st.title("Expense Tracker")
    st.markdown("---")
    if "cache" not in st.session_state:
        st.session_state["cache"] = Cache()
    cache = st.session_state["cache"]

    init_nrec = cache.n_rec
    upload_files(cache)
    cache.stats(init_nrec)

    st.markdown("---")
    cache.print_raw_table()
    
run()