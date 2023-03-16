import streamlit as st
import pandas as pd
import numpy as np

## DASHBOARD STATS
st.header("Tendencies of the day")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.bar_chart(chart_data)
st.write(f"**Average Probability**: {np.mean([0.90, 0.95])}")
st.write(f'**Most detected virus**: {max(set(["Ebola", "Ebola", "CCHP"]))}')
