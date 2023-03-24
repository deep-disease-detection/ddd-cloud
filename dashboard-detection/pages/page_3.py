import streamlit as st
import pandas as pd
import psycopg2
import os
from datetime import datetime

## DASHBOARD STATS
conn = psycopg2.connect(
    host="34.89.42.213",
    database="postgres",
    user="postgres",
    password=os.environ["DB_PASSWORD"])
cur = conn.cursor()
cur.execute("select * from object_detection;")
df = pd.DataFrame(cur.fetchall(), columns=['virus', 'virus_count', 'ts'])


def get_last_week(df):
    df["ts"] = pd.to_datetime(df["ts"])
    today = pd.Timestamp(datetime.now())
    last_week = pd.Timestamp('today') + pd.Timedelta(-7, unit='D')
    mask_last_week = df[(df['ts'] > last_week) & (df['ts'] <= today)]
    return mask_last_week


last_week = get_last_week(df)
last_week = last_week.loc[~last_week.virus.isin(["no virus found"])]



#do a group by virus and sum

# ## DASHBOARD STATS
st.title("Analytics 📊")

#Weekly
st.header("This Week")
st.write(f"Images Count of Last Week: **{len(last_week)}**")
chart_dataframe = last_week.groupby("virus").sum("virus_count")
st.bar_chart(chart_dataframe)
