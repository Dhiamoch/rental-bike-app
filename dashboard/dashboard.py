import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")
#load data
def load_data():
    day_df = pd.read_csv("day_df.csv")
    hour_df = pd.read_csv("hour_df.csv")
    day_hour_df = pd.read_csv("day_hour_df.csv")
    
    #convert data dtedta ke datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df, day_hour_df

day_df, hour_df, day_hour_df = load_data()

#difine warna
colors = {'low': '#1f77b4', 'medium': '#ff7f0e', 'high': '#d62728'}

st.title("🚲 Dashboard Analisa Rental Sepeda")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pengguna Rental Sepeda", f"{day_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Pengguna Harian", f"{day_df['cnt'].mean():.0f}")
with col3:
    st.metric("Pengguna Harian Tertinggi", f"{day_df['cnt'].max():,}")

#Analisa tren pada rental sepeda
st.subheader("Tren Rental Sepeda Harian")
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.scatter(day_df['dteday'], day_df['cnt'], 
           c=day_df['demand_segment'].map(colors), 
           s=30, alpha=0.6)
ax1.set_xlabel("Date")
ax1.set_ylabel("Number of Rentals")
plt.xticks(rotation=45)
st.pyplot(fig1)

col1, col2 = st.columns(2)

#distribusi pengguna rental sepeda berdasarkan tipe pengguna
with col1:
    st.subheader("Distribusi Tipe Pengguna")
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    user_types = ['Casual', 'Registered']
    user_counts = [day_df['casual'].sum(), day_df['registered'].sum()]
    ax2.pie(user_counts, labels=user_types, autopct='%1.1f%%', 
            colors=['lightblue', 'lightgreen'])
    st.pyplot(fig2)

#distribusi pengguna rental sepeda berdasarkan permintaan
with col2:
    st.subheader("Distribusi Segmen Permintaan")
    order = ['low', 'medium', 'high']
    display_labels = {'low': 'Rendah', 'medium': 'Sedang', 'high': 'Tinggi'}
    segment_counts = day_df['demand_segment'].value_counts().reindex(order, fill_value=0)
    fig3, ax3 = plt.subplots(figsize=(9, 9.5))
    bars = ax3.bar([display_labels.get(k, k) for k in segment_counts.index],
                   segment_counts.values,
                   color=[colors.get(x, '#999999') for x in segment_counts.index])
    ax3.set_ylabel("Count")
    ax3.set_xlabel("")
    ax3.set_ylim(0, max(segment_counts.values.max() * 1.1, 1))
    plt.xticks(rotation=0)
    for bar in bars:
        height = bar.get_height()
        ax3.annotate(f'{int(height)}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom')
    st.pyplot(fig3)

#membuat digram heatmap untuk pengguna jasa rental sepeda
st.subheader("Rata-rata Pengguna Jasa Rental Sepeda per Jam Per-hari")
fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.heatmap(day_hour_df, cmap='YlOrRd', ax=ax4, 
            cbar_kws={'label': 'Rata-rata jumlah penyewaan','pad':0.05})
ax4.set_title('Rata-rata Pengguna Jasa Rental Sepeda per Jam dan Hari',pad=10)
ax4.set_ylabel('Jam',labelpad=10)
ax4.set_xlabel('Hari (0 = Minggu, 6 = Sabtu)')
st.pyplot(fig4)


