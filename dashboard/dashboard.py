import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
all_df = pd.read_csv("/mount/src/analisis-data-penyewaan-sepeda/dashboard/all_data.csv")

# Convert date column to datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Sidebar Filters
st.sidebar.header("Filter")
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [all_df['dteday'].min(), all_df['dteday'].max()])

# Filter data based on selection
filtered_df = all_df[(all_df['dteday'] >= pd.to_datetime(date_range[0])) & (all_df['dteday'] <= pd.to_datetime(date_range[1]))]

# Navigation Header
st.markdown("# Dashboard Analisis Penyewaan Sepeda")
tabs = st.tabs(["Cuaca vs. Penyewaan Sepeda", "Hari Kerja vs Akhir Pekan"])

with tabs[0]:
    st.subheader("Cuaca vs. Penyewaan Sepeda")
    if filtered_df['weathersit_daily'].nunique() > 1:
        weather_counts = filtered_df.groupby('weathersit_daily')['cnt_daily'].sum()
        fig, ax = plt.subplots()
        weather_counts.plot(kind='bar', color=['blue', 'orange', 'red'], ax=ax)
        ax.set_xlabel("Cuaca")
        ax.set_ylabel("Jumlah Penyewaan Sepeda")
        ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
        st.pyplot(fig)
    else:
        st.write("Data tidak cukup untuk menampilkan grafik cuaca.")

with tabs[1]:
    st.subheader("Pola Penggunaan Sepeda: Hari Kerja vs Akhir Pekan")
    workday_trend = filtered_df.groupby('workingday_daily')['cnt_daily'].mean()
    if workday_trend.nunique() > 1:
        fig2, ax2 = plt.subplots()
        workday_trend.plot(kind='bar', color=['green', 'purple'], ax=ax2)
        ax2.set_xlabel("Hari")
        ax2.set_ylabel("Rata-rata Penyewaan Sepeda")
        ax2.set_title("Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan")
        ax2.set_xticklabels(["Akhir Pekan / Libur", "Hari Kerja"], rotation=0)
        st.pyplot(fig2)
    else:
        st.write("Data tidak cukup untuk menampilkan grafik hari kerja vs akhir pekan.")

# Footer
st.caption('(c) 2025 Yosua Adriel Tamba (MC299D5Y1421)')
