import os
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

class Cache:
    def __init__(self):
        if not os.path.isdir(".cache"):
            os.mkdir(".cache")

        self.raw, self.proc = None, None
        if os.path.exists(".cache/raw.csv"):
            self.raw = pd.read_csv(".cache/raw.csv")
            self.raw.set_index("csum", inplace=True)
            self.raw["Date"] = pd.to_datetime(self.raw["Date"])
            self.raw["Amount"] = self.raw["Amount"].astype(float)
            for col in "Description", "Type":
                self.raw[col] = self.raw[col].astype(str)

        if os.path.exists(".cache/proc.csv"):
            self.proc = pd.read_csv(".cache/proc.csv")

        self.n_rec = 0 if self.raw is None else len(self.raw)
        
    def add_to_raw(self, df):
        if self.raw is None:
            self.raw = df
        else:
            df = df.loc[df.index.difference(self.raw.index)]
            self.raw = pd.concat([self.raw, df])
        
        self.n_rec = len(self.raw)
        self.save_raw()

    def save_raw(self):
        self.raw.reset_index().to_csv(".cache/raw.csv", index=False)

    def stats(self, init_nrec=None):
        col_ul, col_ur = st.columns(2)
        col_ll, col_lr = st.columns(2)

        if init_nrec is None or self.n_rec - init_nrec == 0:
            col_ul.metric("Records", str(self.n_rec))
        else:
            col_ul.metric("Records", str(self.n_rec), str(self.n_rec - init_nrec))
        
        if self.raw is not None:
            min_date = self.raw["Date"].min().strftime("%d-%b-%Y")
            max_date = self.raw["Date"].max().strftime("%d-%b-%Y")
            col_ll.metric("Start", min_date)
            col_lr.metric("End", max_date)
        
            net_exp =  self.raw[self.raw["Type"] == "CR"]["Amount"].sum() - self.raw[self.raw["Type"] == "DR"]["Amount"].sum()
            
            if abs(net_exp) // 1e5 > 0:
                net_exp = round(net_exp / 1e5, 2)
                net_exp = str(net_exp) + " lk"
            else:
                net_exp = f"{net_exp:n}"

            col_ur.metric("Net Expenses", f"₹{net_exp}")
            
    def print_raw_table(self):
        gb = GridOptionsBuilder.from_dataframe(self.raw)

        gb.configure_pagination()
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
        gridOptions = gb.build()

        AgGrid(self.raw, gridOptions=gridOptions, enable_enterprise_modules=True, theme='dark', fit_columns_on_grid_load=False)