import streamlit as st

class MultiPage:
    def __init__(self):
        self.apps = []
    
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.button("Load Data")
    
