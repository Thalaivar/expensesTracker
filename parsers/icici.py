import hashlib
import pdfplumber
import pandas as pd
from hashlib import sha256

def extract_tables(fname):
    pdf = pdfplumber.open(fname)
    dfs = [pd.DataFrame(pag.extract_table()) for pag in pdf.pages]
    
    # first table has header
    header = dfs[0].iloc[0]
    dfs[0] = dfs[0][1:]

    for i, df in enumerate(dfs):
        df.columns = header
        dfs[i] = df

    df = pd.concat(dfs).reset_index(drop=True)
    return df
    
def parse(fname):
    df = extract_tables(fname)
    df["csum"] = df.apply(lambda x: sha256("##".join(x).encode("utf-8")).hexdigest(), axis=1)

    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    df["Amount"] = df["Amount"].astype(float)
    return df.set_index("csum")