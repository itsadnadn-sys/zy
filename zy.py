import sqlite3
import pandas as pd
import streamlit as st
import numpy as np
conn = sqlite3.connect('test.db')
conn.execute("""CREATE TABLE IF NOT EXISTS products (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT,category TEXT,created_at TEXT,notes TEXT);
                     """)
with st.form("input",clear_on_submit=True) :
    name = st.text_input("name")
    category = st.selectbox("cate",["目标","荣誉","作业","课程"])
    note = st.text_area("note")
    submit = st.form_submit_button('submit')
    if submit:
        sql = f"""
        INSERT INTO products (name,category,created_at,notes)
        VALUES ("{name}","{category}",datetime('now'),"{note}");
        """
        conn.execute(sql)
        conn.commit()
        st.success("成功提交")

sql = "SELECT * FROM products"
d = pd.read_sql(sql,conn)
st.write(d)
