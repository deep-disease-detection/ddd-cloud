import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime

import os

PASSWORD = os.environ.get("PASSWORD")

conn = psycopg2.connect(
    host="34.89.42.213",
    database="postgres",
    user="postgres",
    password=PASSWORD)
cur = conn.cursor()
cur.execute("select * from classifications;")
df = pd.DataFrame(cur.fetchall(), columns=['Accuracy', 'label_virus', 'ts'])

def get_last_week(df):
    df["ts"] = pd.to_datetime(df["ts"])
    today = pd.Timestamp(datetime.now())
    last_week = pd.Timestamp('today') + pd.Timedelta(-7, unit='D')
    mask_last_week = df[(df['ts'] > last_week) & (df['ts'] <= today)]
    return mask_last_week


def get_today(df):
    df["ts"] = pd.to_datetime(df["ts"])
    today = pd.Timestamp(datetime.now()) - pd.Timedelta(12, unit="h")
    mask_today = df[(df['ts'] > today)]
    return mask_today


today = get_today(df)
prob_today= round((today["label_virus"]).mean(),2)
today.index = today["Accuracy"]
last_week = get_last_week(df)
prob_last_week= round((last_week["label_virus"]).mean(),2)
last_week.index = last_week["Accuracy"]

# ## DASHBOARD STATS
st.title("Tendencies")

#Daily
st.header("Today")
st.write(f"**Images Count of Today**: {len(today)}")
st.write(f'**Virus Most detected Daily**: {max(set(today["Accuracy"]))}')
chart_data_today = pd.DataFrame(today, columns=["label_virus"])
st.bar_chart(chart_data_today)

#Weekly
st.header("This Week")
st.write(f"**Images Count of Last Week**: {len(last_week)}")
st.write(f'**Virus Most detected Weekly**: {max(set(last_week["Accuracy"]))}')
chart_data_week = pd.DataFrame(last_week, columns=["label_virus"])
st.bar_chart(chart_data_week)
