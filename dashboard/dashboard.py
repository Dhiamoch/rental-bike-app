import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#load data
def load_data():
    day_df = pd.read_csv("day_df.csv")
    hour_df = pd.read_csv("hour_df.csv")
    
    #convert data dtedta ke datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df, 

day_df, hour_df = load_data()

#difine warna
colors = {'low': '#1f77b4', 'medium': '#ff7f0e', 'high': '#d62728'}

st.title("Dashboard Analisa Rental Sepeda pada tahun 2011-2012 🚲 ")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pengguna Rental Sepeda", f"{day_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Pengguna Harian", f"{day_df['cnt'].mean():.0f}")
with col3:
    st.metric("Pengguna Harian Tertinggi", f"{day_df['cnt'].max():,}")


day_hour_df = ( hour_df .groupby(['hr', 'weekday'])['cnt'] .mean() .unstack() .sort_index() ) 
day_hour_df.index = [f"{h:02d}:00" for h in day_hour_df.index] 

st.subheader("Permintaan Jasa Rental Sepeda per-Hari")
colors = {
    'Spring': '#77DD77',  
    'Summer': '#FFD700',   
    'Fall':   '#FF8C00',  
    'Winter': '#87CEEB'    
}
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(day_df['dteday'], day_df['cnt'], c=day_df['musim'].map(colors), s=10)

for seg, color in colors.items():
    ax.scatter([], [], c=color, label=seg, s=30)
ax.set_title('Permintaan Jasa Rental Sepeda per-Hari')
ax.set_xlabel('Tanggal', labelpad=10)
ax.set_ylabel('Pengguna', labelpad=10)
ax.legend(loc='upper left')
plt.tight_layout()

st.pyplot(fig)

# Markdown hasil anaslisa Permintaan Jasa Rental Sepeda per-Hari
with st.expander("📊 Hasil Analisa"):
    st.markdown("""
    - Terdapat peningkatan yang signifikan dari tahun **2011 ke 2012**  
    - Pola musiman terlihat jelas, dengan **permintaan tertinggi pada musim Fall** dan **terendah pada musim Spring**  
    """)


# Diagram heatmap 
st.subheader("Pola Aktivitas Pengguna Rental Sepeda per Hari dan Jam")
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(
    day_hour_df, 
    cmap='YlOrRd', 
    annot=False, 
    cbar_kws={'label': 'Rata-rata jumlah penyewaan','pad':0.05},
    ax=ax
)

ax.set_title('Pola Aktivitas Pengguna Rental Sepeda per Hari dan Jam', pad=10)
ax.set_ylabel('Jam', labelpad=10)
ax.set_xlabel('Hari (0-6 = Minggu–Sabtu)', labelpad=10)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
st.pyplot(fig)

# Markdown hasil anaslisa Permintaan Jasa Rental Sepeda per-Hari
with st.expander("📊 Hasil Analisa"):
    st.markdown("""
    - **Weekday (Senin–Jumat):**  
      * Terdapat dua puncak penggunaan: **pagi hari (08:00)** dan **sore hari (17:00–18:00)**  

    - **Weekend (Sabtu–Minggu):**  
      * Pola penggunaan lebih **merata sepanjang 10:00–18:00**  
    """)




st.subheader("Analisis Pengguna Rental Sepeda Berdasarkan Musim dan Tipe Pengguna")
col1, col2 = st.columns(2)

# Bar chart total pengguna per-musim
grouped_musim_day_sum = (
    day_df.groupby('musim')[['casual', 'registered','cnt']]
    .sum()
    .reindex(['Spring', 'Summer', 'Fall', 'Winter'])
)
with col1:
    musim = grouped_musim_day_sum.index

    fig1, ax1 = plt.subplots(figsize=(5, 5.4))
    ax1.bar(musim, grouped_musim_day_sum['cnt'], color='#66c2a5')
    ax1.set_title('Total Pengguna per Musim')
    ax1.set_ylabel('Jumlah Pengguna', labelpad=8)
    ax1.ticklabel_format(style='plain', axis='y')

    st.pyplot(fig1)

# Diagram pie chart distribusi pengguna berdasarkan tipe
with col2:
    user_types = ['Casual', 'Registered']

    fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
    ax2.pie(
        [day_df['casual'].sum(), day_df['registered'].sum()],
        labels=user_types,
        autopct='%1.1f%%',
        colors=['#66b3ff', '#99ff99'],
        startangle=90,
        wedgeprops={'edgecolor': 'white'}
    )
    ax2.set_title('Distribusi Pengguna Berdasarkan Tipe', pad=15)

    st.pyplot(fig2)

# Markdown hasil anaslisa Distribusi total pengguna per-musim & Pengguna Berdasarkan Tipe
with st.expander("📊 Hasil Analisa"):
    st.markdown("""
    - Total pengguna per musim menunjukkan pola yang jelas:  
      * **Tertinggi pada musim Fall**  
      * **Terendah pada musim Spring** 
    
    - Pengguna terbanyak berasal dari **pengguna Registered**  
 
    """)

#Diagram bar untuk total pengguna casual per-hari
st.subheader("Total Pengguna Casual per Hari")
grouped_hari_sum = (
    day_df.groupby('hari')[['casual', 'registered','cnt']]
    .sum()
    .reindex(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
)
hari = grouped_hari_sum.index
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(hari, grouped_hari_sum['casual'], color='#66c2a5')
ax.set_title('Total Pengguna Casual per Hari', pad=10)
ax.set_ylabel('Jumlah Pengguna', labelpad=8)
ax.ticklabel_format(style='plain', axis='y')  
st.pyplot(fig)



#Diagram bar untuk total pengguna registered per-hari
st.subheader("Total Pengguna Registered per Hari")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(hari, grouped_hari_sum['registered'], color='#fc8d62')
ax.set_title('Total Pengguna Registered per Hari', pad=10)
ax.set_ylabel('Jumlah Pengguna', labelpad=8)
ax.ticklabel_format(style='plain', axis='y')  
st.pyplot(fig)


#Diagram bar untuk total pengguna per-hari
st.subheader("Total Pengguna per Hari")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(hari, grouped_hari_sum['cnt'], color='#8da0cb')

ax.set_title('Total Pengguna per Hari', pad=10)
ax.set_ylabel('Jumlah Pengguna', labelpad=8)
ax.ticklabel_format(style='plain', axis='y')  

st.pyplot(fig)

# Markdown hasil anaslisa total pengguna per-hari pada casual, registred dan total pengguna
with st.expander("📊 Hasil Analisa"):
    st.markdown("""
    - Total pengguna **casual** harian **tinggi pada waktu weekend**  
    - Total pengguna **registered** menunjukkan pola yang **berbanding terbalik**,  
      di mana **permintaan tertinggi terjadi pada weekday**
    """)