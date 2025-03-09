import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

file_path = "https://github.com/yosel-tamba/analisis-data-penyewaan-sepeda/blob/4a1e665b46e14c9a5c557c51c5f09ae233b3a915/dashboard/all_data.csv"
df = pd.read_csv(file_path, on_bad_lines='skip')
df.rename(columns={"Dteday": "dteday"}, inplace=True)

df["dteday"] = pd.to_datetime(df["dteday"])

st.set_page_config(page_title="Bike Rental Dashboard", page_icon="🚲", layout="wide")
st.title("🚴 Bike Rental Dashboard")

st.sidebar.title("🔍 Filter Data")

start_date, end_date = st.sidebar.date_input("📅 Pilih Rentang Tanggal", [df["dteday"].min(), df["dteday"].max()])
time_filter = st.sidebar.radio("⏳ Pilih Data", ["Daily", "Hourly"], horizontal=True)
filtered_df = df[(df["dteday"] >= pd.Timestamp(start_date)) & (df["dteday"] <= pd.Timestamp(end_date))]

# Layout utama
col1, col2 = st.columns([2, 3])

# Total penyewaan berdasarkan filter
with col1:
    st.metric(label="🚲 Total Penyewaan", value=filtered_df["cnt_daily"].sum() if time_filter == "Daily" else filtered_df["cnt_hourly"].sum())

# Diagram penyewaan berdasarkan filter
with col2:
    st.write("### 📊 Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=filtered_df["dteday" if time_filter == "Daily" else "hr"], y=filtered_df["cnt_daily" if time_filter == "Daily" else "cnt_hourly"], ax=ax, palette="viridis")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Diagram penyewaan berdasarkan cuaca
st.write("### 🌦️ Penyewaan Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=filtered_df["weathersit_daily" if time_filter == "Daily" else "weathersit_hourly"], y=filtered_df["cnt_daily" if time_filter == "Daily" else "cnt_hourly"], ax=ax, palette="coolwarm")
ax.set_xlabel("Cuaca")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Customer Demographic
st.write("### 👥 Customer Demographic")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=["Weekday", "Holiday", "Workingday"], y=[filtered_df["weekday_daily" if time_filter == "Daily" else "weekday_hourly"].sum(), filtered_df["holiday_daily" if time_filter == "Daily" else "holiday_hourly"].sum(), filtered_df["workingday_daily" if time_filter == "Daily" else "workingday_hourly"].sum()], ax=ax, palette="magma")
ax.set_title("Penyewaan Berdasarkan Weekday, Holiday, dan Workingday")
st.pyplot(fig)

# RFM Analysis
st.write("### 🏆 Best Penyewaan Berdasarkan RFM Parameter")
col1, col2 = st.columns(2)

# Recency Diagram
with col1:
    st.write("#### ⏳ Recency (Days)")
    recency = (df["dteday"].max() - filtered_df.groupby("instant_daily" if time_filter == "Daily" else "instant_hourly")["dteday"].max()).dt.days
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(x=recency.index, y=recency, ax=ax, palette="Blues")
    ax.set_xlabel("Pelanggan")
    ax.set_ylabel("Hari Sejak Penyewaan Terakhir")
    st.pyplot(fig)

# Frequency Diagram
with col2:
    st.write("#### 🔄 Frequency")
    frequency = filtered_df.groupby("instant_daily" if time_filter == "Daily" else "instant_hourly")["cnt_daily" if time_filter == "Daily" else "cnt_hourly"].count()
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.barplot(x=frequency.index, y=frequency, ax=ax, palette="Greens")
    ax.set_xlabel("Pelanggan")
    ax.set_ylabel("Total Transaksi")
    st.pyplot(fig)

# Footer
st.caption('(c) 2025 Yosua Adriel Tamba (MC299D5Y1421)')
