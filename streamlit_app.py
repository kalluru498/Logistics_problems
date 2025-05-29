
# streamlit_app.py
import streamlit as st
import pandas as pd
from optimizer import optimize_loading
from utils import recommend_trailer

st.set_page_config(page_title="Door-to-Trailer Optimizer", layout="wide")
st.title("🚪📦 Door-to-Trailer Loading Optimizer")

st.sidebar.header("Upload Your Data")

# Upload doors CSV
doors_file = st.sidebar.file_uploader("Upload Door Data CSV", type=["csv"])
trailer_file = st.sidebar.file_uploader("Upload Trailer Data CSV (Optional)", type=["csv"])

# Load default data if not uploaded
if doors_file:
    doors_df = pd.read_csv(doors_file)
else:
    doors_df = pd.read_csv("data/door_specifications_home_depot.csv")

if trailer_file:
    trailer_df = pd.read_csv(trailer_file)
else:
    trailer_df = pd.read_csv("data/truck_trailer_specs.csv")

st.subheader("Uploaded Door Data")
st.dataframe(doors_df)

# Auto-recommend trailer if not specified
recommended_trailer = recommend_trailer(doors_df, trailer_df)
st.subheader("Recommended or Selected Trailer")
st.json(recommended_trailer)

# Run optimization
results = optimize_loading(doors_df, recommended_trailer)

st.subheader("📋 Loading Instructions")
for line in results['instructions']:
    st.markdown(line)

st.subheader("📊 Summary")
st.write(results['summary'])